import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import streamlit as st
import os
from datetime import datetime, timedelta
import hashlib
import logging
import io
import uuid
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set page config
st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3
MAX_ROWS_DISPLAY = 1000
SIZE_LIMIT_MB = 190
DOWNLOAD_FOLDER = "downloads"
DOWNLOAD_EXPIRY_HOURS = 1  # Files will be deleted after this many hours
CHUNK_SIZE = 1024 * 1024  # 1 MB chunks

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

# Mock function for SQL generation (replace with actual implementation)
def generate_sql(question):
    return f"SELECT * FROM sample_table WHERE condition = '{question}';"

# Mock function for query execution (replace with actual implementation)
def execute_query(sql):
    n_rows = 10000000  # Increased for testing large datasets
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

# Update feedback
def update_feedback(feedback_type, question):
    for _ in range(MAX_RETRIES):
        try:
            data = pd.read_csv(CSV_FILE)
            if not data.empty:
                matching_rows = data[data['question'] == question]
                if not matching_rows.empty:
                    latest_index = matching_rows.index[-1]
                    data.loc[latest_index, feedback_type] = 1
                    data.to_csv(CSV_FILE, index=False)
                    logging.info(f"Updated {feedback_type} for question: {question}")
                    return True
                else:
                    logging.warning(f"No matching question found for feedback: {question}")
            else:
                logging.warning("CSV file is empty")
            return False
        except Exception as e:
            logging.error(f"Error updating feedback: {str(e)}")
    return False

# Function to clean up old download files
def cleanup_old_files():
    now = datetime.now()
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        if now - file_modified > timedelta(hours=DOWNLOAD_EXPIRY_HOURS):
            os.remove(file_path)

# Function to generate CSV file and return its file path
def generate_csv_file(result_df):
    filename = f"result_{uuid.uuid4().hex}.csv"
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    result_df.to_csv(file_path, index=False)
    return file_path

# Function to stream CSV file in chunks
def stream_csv(file_path):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            yield chunk

# Function to create a download button
def create_download_button(file_path):
    file_size = os.path.getsize(file_path)
    
    def file_download_callback():
        with st.spinner('Preparing download...'):
            with ThreadPoolExecutor() as executor:
                future = executor.submit(stream_csv, file_path)
                return future.result()

    st.download_button(
        label="Download full CSV",
        data=file_download_callback,
        file_name=os.path.basename(file_path),
        mime="text/csv",
        key=f"download_button_{uuid.uuid4().hex}"
    )
    st.info(f"File size: {file_size / (1024 * 1024):.2f} MB")

# Main app
def main():
    init_app()
    cleanup_old_files()  # Clean up old files at the start of each session

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

        user_input = st.text_area("Enter your question about the data:")

        button_column = st.columns(3)
        button_info = st.empty()

        with button_column[2]:
            if st.button("🚀 Generate SQL", key="generate_sql", use_container_width=True):
                if user_input:
                    user_input_placeholder.markdown(user_input)
                    try:
                        sql_response = generate_sql(user_input)
                        st.session_state['last_sql'] = sql_response
                        bot_response_1_placeholder.code(sql_response, language="sql")
                        
                        result_df = execute_query(sql_response)
                        
                        df_size = result_df.memory_usage(deep=True).sum() / (1024 * 1024)  # Size in MB
                        
                        limited_result = result_df.head(MAX_ROWS_DISPLAY)
                        bot_response_2_placeholder.dataframe(limited_result)
                        info_placeholder.info(f"Showing first {MAX_ROWS_DISPLAY} rows of {len(result_df)} total rows. Total size: {df_size:.2f} MB")
                        
                        # Generate CSV file and provide download button
                        csv_file_path = generate_csv_file(result_df)
                        if csv_file_path:
                            create_download_button(csv_file_path)
                        
                        result_response = f"Query executed successfully. {len(result_df)} rows returned."
                        handle_interaction(user_input, result_response)
                    except Exception as e:
                        logging.error(f"Error processing query: {str(e)}")
                        info_placeholder.error(f"An error occurred while processing your query: {str(e)}")

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
            "Show me the sales trend over the last year.",
            "Which products have the highest return rates?",
            "How many orders were placed in the last month?"
        ]
        
        for question in sample_questions:
            st.markdown(f"- {question}")

    # Load existing interactions (for display purposes or further processing)
    data = load_data()

    # Optionally display the data or perform additional operations
    st.markdown("### Interaction Log")
    st.dataframe(data)

if __name__ == "__main__":
    main()

