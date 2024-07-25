 import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import os
from datetime import datetime, date, timedelta
import hashlib
import logging
from snowflake.connector.errors import ProgrammingError

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set page config
st.set_page_config(page_title="NhanceBot", layout="wide", initial_sidebar_state="collapsed")

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3

# Initialize CSV file
def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['timestamp', 'question', 'result', 'upvote', 'downvote', 'session_id'])
        df.to_csv(CSV_FILE, index=False)

# Load CSV file
@st.cache_data
def load_data():
    for _ in range(MAX_RETRIES):
        try:
            data = pd.read_csv(CSV_FILE)
            return data
        except pd.errors.EmptyDataError:
            logging.warning(f"CSV file {CSV_FILE} is empty. Initializing with header.")
            init_csv()
        except Exception as e:
            logging.error(f"Error loading CSV: {str(e)}")
    return pd.DataFrame()  # Return empty DataFrame if all retries fail

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
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = generate_session_id()
    if 'last_question' not in st.session_state:
        st.session_state['last_question'] = None

# Mock function for SQL generation (replace with actual implementation)
def generate_sql(question):
    return f"SELECT * FROM sample_table WHERE condition = '{question}';"

# Mock function for query execution (replace with actual implementation)
def execute_query(sql):
    # This is a mock implementation. Replace with actual query execution.
    raise ProgrammingError("Object 'SAMPLE_TABLE' does not exist or not authorized.")

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

# Add to chat history
def add_to_chat_history(question, sql_query, result):
    st.session_state['chat_history'].append({
        'question': question,
        'sql_query': sql_query,
        'result': result
    })

# Main app
def main():
    init_app()

    # Date selection
    today = date.today()
    default_start = today - timedelta(days=7)
    min_start_date = today - timedelta(days=60)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                   value=default_start,
                                   min_value=min_start_date,
                                   max_value=today,
                                   format="DD/MM/YYYY")

    with col2:
        max_end_date = min(start_date + timedelta(days=60), today)
        end_date = st.date_input("End Date", 
                                 value=today,
                                 min_value=start_date,
                                 max_value=max_end_date,
                                 format="DD/MM/YYYY")

    if (end_date - start_date).days > 60:
        st.error("The difference between start and end date cannot exceed 2 months.")
        return

    if not start_date or not end_date:
        st.warning("Please select both start and end dates to begin.")
        return

    # Logo and title
    col1, col2 = st.columns([0.2, 1.5])
    with col1:
        st.image("logo.png", width=60)
    with col2:
        st.markdown("<h1 style='color: maroon; margin-bottom: 0;'>NhanceBot</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    NhanceBot is an AI-powered Data Insight tool designed to help you 
    interact with your Snowflake data warehouse using natural language.
    
    Selected date range: {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}
    """)

    st.markdown('##### Sample Data Schema:')
    data = {
        'Table': ['CUSTOMERS', 'ORDERS', 'PRODUCTS', 'SALES'],
        'Columns': [
            'customer_id, name, email, segment',
            'order_id, customer_id, order_date, total_amount',
            'product_id, name, category, price',
            'sale_id, product_id, quantity, revenue'
        ]
    }
    df = pd.DataFrame(data)
    
    st.dataframe(df, height=500, use_container_width=True)

    # Display chat history
    for entry in st.session_state['chat_history']:
        with st.chat_message(name="user", avatar="user"):
            st.markdown(entry['question'])
        with st.chat_message(name="assistant", avatar="assistant"):
            st.code(entry['sql_query'], language="sql")
            st.dataframe(entry['result'])

    with st.chat_message(name="user", avatar="user"):
        user_input_placeholder = st.empty()
    with st.chat_message(name="assistant", avatar="assistant"):
        bot_response_1_placeholder = st.empty()
        bot_response_2_placeholder = st.empty()

    user_input = st.text_area("Enter your question about the data:")

    button_column = st.columns(3)
    button_info = st.empty()

    with button_column[2]:
        if st.button("🚀 Generate SQL", key="generate_sql", use_container_width=True):
            if user_input:
                user_input_placeholder.markdown(user_input)
                try:
                    with st.spinner("Generating SQL..."):
                        sql_response = generate_sql(user_input)
                    bot_response_1_placeholder.code(sql_response, language="sql")
                    result_df = execute_query(sql_response)
                    bot_response_2_placeholder.dataframe(result_df)
                    handle_interaction(user_input, sql_response)
                    add_to_chat_history(user_input, sql_response, result_df)
                except ProgrammingError as e:
                    error_message, error_type = parse_snowflake_error(str(e), sql_response)
                    st.error(f"I'm sorry, I ran into a problem: {error_message}")
                    st.info("Here are some tips that might help:")
                    tips = get_error_tips(error_type)
                    for tip in tips:
                        st.markdown(tip)
                    if error_type == "unknown_error":
                        st.markdown(f"For reference, the full error message was: {str(e)}")
                    st.markdown("If none of these help, feel free to ask your question in a different way!")
                except Exception as e:
                    logging.error(f"Error processing query: {str(e)}")
                    st.error("I'm having trouble understanding that. Could you try asking in a different way?")
                    st.info("Here are some general tips that might help:")
                    tips = get_error_tips("unknown_error")
                    for tip in tips:
                        st.markdown(tip)

    with button_column[1]:
        if st.button("👍 Upvote", key="upvote", use_container_width=True):
            if st.session_state.get('last_question'):
                if update_feedback('upvote', st.session_state['last_question']):
                    button_info.success("Thanks for your feedback! NhanceBot Memory updated")
                else:
                    button_info.error("Failed to update feedback. Please try again.")
            else:
                button_info.warning("No recent question to upvote.")

    with button_column[0]:
        if st.button("👎 Downvote", key="downvote", use_container_width=True):
            if st.session_state.get('last_question'):
                if update_feedback('downvote', st.session_state['last_question']):
                    button_info.warning("We're sorry the response didn't meet your expectations. Your feedback helps us improve.")
                else:
                    button_info.error("Failed to update feedback. Please try again.")
            else:
                button_info.warning("No recent question to downvote.")

if __name__ == "__main__":
    main()

