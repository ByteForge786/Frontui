import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import streamlit as st
import os
from datetime import datetime
import hashlib
import logging
import uuid
import zipfile
import plotly.express as px

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set page config
st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3
MAX_ROWS_DISPLAY = 1000
ZIP_FOLDER = "zip_downloads"
SIZE_LIMIT_MB = 190

# Initialize CSV file
def init_csv():
    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=['timestamp', 'question', 'result', 'upvote', 'downvote', 'session_id']).to_csv(CSV_FILE, index=False)

# Load CSV file
@st.cache_data
def load_data():
    for _ in range(MAX_RETRIES):
        try:
            return pd.read_csv(CSV_FILE)
        except pd.errors.EmptyDataError:
            init_csv()
        except Exception as e:
            logging.error(f"Error loading CSV: {str(e)}")
    return pd.DataFrame()

# Append data to CSV
def append_to_csv(new_data):
    for _ in range(MAX_RETRIES):
        try:
            with open(CSV_FILE, 'a', newline='') as f:
                new_data.to_csv(f, header=f.tell()==0, index=False)
            return True
        except Exception as e:
            logging.error(f"Error appending to CSV: {str(e)}")
    return False

# Generate a session ID
def generate_session_id():
    return hashlib.md5(str(datetime.now()).encode()).hexdigest()

# Initialize app
def init_app():
    init_csv()
    
    # Initialize basic session state variables
    if 'chat' not in st.session_state:
        st.session_state['chat'] = {
            "history": [],  # List to store chat history
            "current_question": None,
            "current_sql": None,
            "current_df": None,
        }
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = generate_session_id()
    if 'last_question' not in st.session_state:
        st.session_state['last_question'] = None
    if 'last_sql' not in st.session_state:
        st.session_state['last_sql'] = None
    if 'chart_states' not in st.session_state:
        st.session_state['chart_states'] = {}  # Dictionary to store chart visibility states

def toggle_chart(message_id):
    if message_id in st.session_state['chart_states']:
        st.session_state['chart_states'][message_id] = not st.session_state['chart_states'][message_id]
    else:
        st.session_state['chart_states'][message_id] = True

# Generate chart based on data
def generate_chart(df):
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if len(numeric_cols) > 0 and len(categorical_cols) > 0:
            fig = px.box(df, x=categorical_cols[0], y=numeric_cols[0], 
                        title=f"{numeric_cols[0]} by {categorical_cols[0]}")
        elif len(numeric_cols) > 0:
            fig = px.histogram(df, x=numeric_cols[0], 
                             title=f"Distribution of {numeric_cols[0]}")
        elif len(categorical_cols) > 0:
            value_counts = df[categorical_cols[0]].value_counts()
            fig = px.bar(x=value_counts.index, y=value_counts.values, 
                        title=f"Count of {categorical_cols[0]}")
        else:
            return None
            
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        logging.error(f"Error generating chart: {str(e)}")
        return None

# Mock function for SQL generation
def generate_sql(question):
    return f"SELECT * FROM sample_table WHERE condition = '{question}';"

# Mock function for query execution
def execute_query(sql):
    n_rows = 10000000
    return pd.DataFrame({
        'id': range(n_rows),
        'value': np.random.rand(n_rows),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_rows)
    })

# Handle user interaction
def handle_interaction(question, result):
    new_data = pd.DataFrame({
        'timestamp': [datetime.now()],
        'question': [question.strip().replace('\n', ' ')],
        'result': [result.strip().replace('\n', ' ')],
        'upvote': [0],
        'downvote': [0],
        'session_id': [st.session_state['session_id']]
    })
    append_to_csv(new_data)
    st.session_state['last_question'] = question.strip().replace('\n', ' ')

# Generate a zip file containing the CSV file
def generate_zip_file():
    if st.session_state['last_sql']:
        result_df = execute_query(st.session_state['last_sql'])
        filename = f"result_{uuid.uuid4().hex}.csv"
        zip_filename = f"result_{uuid.uuid4().hex}.zip"
        temp_file_path = os.path.join(ZIP_FOLDER, filename)
        os.makedirs(ZIP_FOLDER, exist_ok=True)

        result_df.to_csv(temp_file_path, index=False)

        zip_file_path = os.path.join(ZIP_FOLDER, zip_filename)
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            zipf.write(temp_file_path, arcname=filename)

        os.remove(temp_file_path)
        return zip_file_path
    return None

def update_feedback(feedback_type, question):
    try:
        df = pd.read_csv(CSV_FILE)
        mask = df['question'] == question
        if feedback_type == 'upvote':
            df.loc[mask, 'upvote'] += 1
        else:
            df.loc[mask, 'downvote'] += 1
        df.to_csv(CSV_FILE, index=False)
        return True
    except Exception as e:
        logging.error(f"Error updating feedback: {str(e)}")
        return False

def process_and_display_query(question):
    # Generate unique message ID
    message_id = str(len(st.session_state.chat['history']))
    
    try:
        # Generate and store SQL
        sql_response = generate_sql(question)
        st.session_state['last_sql'] = sql_response
        
        # Execute query and store results
        result_df = execute_query(sql_response)
        
        # Calculate size
        df_size = result_df.memory_usage(deep=True).sum() / (1024 * 1024)
        
        # Store the interaction in chat history
        chat_item = {
            'id': message_id,
            'question': question,
            'sql': sql_response,
            'df': result_df,
            'df_size': df_size,
            'timestamp': datetime.now()
        }
        st.session_state.chat['history'].append(chat_item)
        
        result_response = f"Query executed successfully. {len(result_df)} rows returned."
        handle_interaction(question, result_response)
        
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        st.error(f"An error occurred while processing your query: {str(e)}")

def display_chat_history():
    for chat_item in st.session_state.chat['history']:
        message_id = chat_item['id']
        
        # Display user message
        with st.chat_message(name="user", avatar="user"):
            st.markdown(chat_item['question'])
        
        # Display assistant response
        with st.chat_message(name="assistant", avatar="assistant"):
            # Display SQL
            st.code(chat_item['sql'], language="sql")
            
            # Display results
            df = chat_item['df']
            df_size = chat_item['df_size']
            
            if df_size > SIZE_LIMIT_MB:
                st.dataframe(df.head(MAX_ROWS_DISPLAY))
                st.info(f"Showing first {MAX_ROWS_DISPLAY} rows of {len(df)} total rows. Total size: {df_size:.2f} MB")
            else:
                st.dataframe(df)
                st.info(f"Showing all rows. Total size: {df_size:.2f} MB")
            
            # Download button
            zip_file_path = generate_zip_file()
            if zip_file_path:
                with open(zip_file_path, "rb") as file:
                    st.download_button(
                        label="Download full CSV as ZIP",
                        data=file,
                        file_name=os.path.basename(zip_file_path),
                        mime="application/zip"
                    )
            
            # Chart toggle and display
            st.button(
                "📊 Show/Hide Chart",
                key=f"chart_toggle_{message_id}",
                on_click=toggle_chart,
                args=(message_id,)
            )
            
            if st.session_state['chart_states'].get(message_id, False):
                fig = generate_chart(df.head(1000))
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not generate chart for this data structure")

# Main app function
def main():
    init_app()

    st.markdown('## NeuroFlake: AI-Powered Text-to-SQL for Snowflake')

    # Display chat history
    display_chat_history()

    # Input section
    user_input = st.text_area("Enter your question about the data:")

    button_column = st.columns(3)
    button_info = st.empty()

    with button_column[2]:
        if st.button("🚀 Generate SQL", key="generate_sql", use_container_width=True):
            if user_input:
                process_and_display_query(user_input)

    with button_column[1]:
        if st.button("👍 Upvote", key="upvote", use_container_width=True):
            if st.session_state.get('last_question'):
                if update_feedback('upvote', st.session_state['last_question']):
                    button_info.success("Thanks for your feedback! NeuroFlake Memory updated")
                else:
                    button_info.error("Failed to update feedback. Please try again.")
            else:
                button_info.warning("No recent question to upvote.")

    with button_column[0]:
        if st.button("👎 Downvote", key="downvote", use_container_width=True):
            if st.session_state.get('last_question'):
                if update_feedback('downvote', st.session_state['last_question']):
                    button_info.warning("We're sorry the result wasn't helpful. Your feedback will help us improve!")
                else:
                    button_info.error("Failed to update feedback. Please try again.")
            else:
                button_info.warning("No recent question to downvote.")

    st.markdown("##### Sample questions you can ask:")
    sample_questions = [
        "What is the total revenue for each product category?",
        "Who are the top 5 customers by sales volume?",
        "What's the average order value by month?",
        "Which regions have seen the highest growth in the last quarter?",
        "What's the distribution of customer segments across different product lines?"
    ]
    
    for i, question in enumerate(sample_questions):
        question_columns = st.columns([7,1])
        with question_columns[0]:
            st.markdown(f"<div class='mytext'>{question}</div>", unsafe_allow_html=True)
        with question_columns[1]:
            if st.button(f"Ask", use_container_width=True, key=f'question{i}'):
                process_and_display_query(question)

if __name__ == "__main__":
    main()
