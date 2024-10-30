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
    if 'chat' not in st.session_state:
        st.session_state['chat'] = {"user_input": None, "bot_response_1": None, "bot_response_2": None}
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = generate_session_id()
    if 'last_question' not in st.session_state:
        st.session_state['last_question'] = None
    if 'last_sql' not in st.session_state:
        st.session_state['last_sql'] = None
    if 'show_chart' not in st.session_state:
        st.session_state['show_chart'] = False
    if 'current_df' not in st.session_state:
        st.session_state['current_df'] = None
    # Add these new session states
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'current_result' not in st.session_state:
        st.session_state['current_result'] = None

# Toggle chart visibility without losing state
def toggle_chart():
    st.session_state['show_chart'] = not st.session_state['show_chart']

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

# Process query and update session state
def process_query(question):
    try:
        sql_response = generate_sql(question)
        st.session_state['last_sql'] = sql_response
        result_df = execute_query(sql_response)
        st.session_state['current_df'] = result_df
        
        df_size = result_df.memory_usage(deep=True).sum() / (1024 * 1024)
        
        # Store the current result in session state
        st.session_state['current_result'] = {
            'question': question,
            'sql': sql_response,
            'df': result_df,
            'df_size': df_size
        }
        
        result_response = f"Query executed successfully. {len(result_df)} rows returned."
        handle_interaction(question, result_response)
        
        return True
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        return False

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

# Create download button for zipped CSV
def create_download_button(file_path):
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download full CSV as ZIP",
                data=file,
                file_name=os.path.basename(file_path),
                mime="application/zip"
            )

# Display current result
def display_current_result(bot_response_1_placeholder, bot_response_2_placeholder, 
                         info_placeholder, download_placeholder, chart_container):
    if st.session_state['current_result']:
        result = st.session_state['current_result']
        bot_response_1_placeholder.code(result['sql'], language="sql")
        
        if result['df_size'] > SIZE_LIMIT_MB:
            limited_result = result['df'].head(MAX_ROWS_DISPLAY)
            bot_response_2_placeholder.dataframe(limited_result)
            info_placeholder.info(f"Showing first {MAX_ROWS_DISPLAY} rows of {len(result['df'])} total rows. Total size: {result['df_size']:.2f} MB")
        else:
            bot_response_2_placeholder.dataframe(result['df'])
            info_placeholder.info(f"Showing all rows. Total size: {result['df_size']:.2f} MB")
        
        zip_file_path = generate_zip_file()
        if zip_file_path:
            with download_placeholder:
                create_download_button(zip_file_path)
        
        with chart_container:
            if st.button("📊 Show/Hide Chart", on_click=toggle_chart):
                pass
            
            if st.session_state['show_chart']:
                fig = generate_chart(result['df'].head(1000))
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not generate chart for this data structure")

# Main app function
def main():
    init_app()

    st.markdown('## NeuroFlake: AI-Powered Text-to-SQL for Snowflake')

    left_column, right_column = st.columns(2, gap="large")

    with right_column.container():
        with st.chat_message(name="user", avatar="user"):
            user_input_placeholder = st.empty()
        with st.chat_message(name="assistant", avatar="assistant"):
            bot_response_1_placeholder = st.empty()
            bot_response_2_placeholder = st.empty()
            info_placeholder = st.empty()
            download_placeholder = st.empty()
            chart_container = st.empty()

        user_input = st.text_area("Enter your question about the data:")

        button_column = st.columns(3)
        button_info = st.empty()

        with button_column[2]:
            if st.button("🚀 Generate SQL", key="generate_sql", use_container_width=True):
                if user_input:
                    user_input_placeholder.markdown(user_input)
                    if process_query(user_input):
                        display_current_result(bot_response_1_placeholder, bot_response_2_placeholder,
                                            info_placeholder, download_placeholder, chart_container)
                    else:
                        info_placeholder.error("An error occurred while processing your query.")

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
                    user_input_placeholder.markdown(question)
                    if process_query(question):
                        display_current_result(bot_response_1_placeholder, bot_response_2_placeholder,
                                            info_placeholder, download_placeholder, chart_container)
                    else:
                        info_placeholder.error("An error occurred while processing your query.")

    st.markdown("<br><br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
