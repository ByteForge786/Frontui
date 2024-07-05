 import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import os
from datetime import datetime
import hashlib
import logging
from sql_generator import SQLGenerator

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set page config
st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3

# Initialize SQL Generator
@st.cache_resource
def get_sql_generator():
    return SQLGenerator()

sql_generator = get_sql_generator()

# Initialize CSV file
def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['timestamp', 'question', 'sql_query', 'upvote', 'downvote', 'session_id'])
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
    if 'chat' not in st.session_state:
        st.session_state['chat'] = {
            "user_input": None,
            "bot_response_1": None,
            "bot_response_2": None,
        }
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = generate_session_id()
    if 'last_question' not in st.session_state:
        st.session_state['last_question'] = None
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

# Generate SQL
def generate_sql(question):
    try:
        return sql_generator.generate_sql(question)
    except Exception as e:
        logging.error(f"Error generating SQL: {str(e)}")
        raise

# Mock function for Snowflake query execution
def execute_query(sql):
    # This is a mock function. Replace with actual Snowflake query execution.
    mock_data = {
        'Column1': [1, 2, 3, 4, 5],
        'Column2': ['A', 'B', 'C', 'D', 'E'],
        'Column3': [10.1, 20.2, 30.3, 40.4, 50.5]
    }
    # Simulating a Snowflake cursor result
    class MockCursor:
        def fetch_pandas_all(self):
            return pd.DataFrame(mock_data)
    return MockCursor()

# Handle user interaction
def handle_interaction(question, sql_query):
    new_data = pd.DataFrame({
        'timestamp': [datetime.now()],
        'question': [question.strip().replace('\n', ' ')],
        'sql_query': [sql_query.strip().replace('\n', ' ')],
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
def add_to_chat_history(question, sql_query, result_df):
    st.session_state['chat_history'].append({
        'question': question,
        'sql_query': sql_query,
        'result': result_df
    })
    auto_scroll_to_bottom()

# Auto-scroll function
def auto_scroll_to_bottom():
    js = """
    <script>
        var rightContainer = document.querySelector('.right-container');
        rightContainer.scrollTop = rightContainer.scrollHeight;
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)

# Main app
def main():
    init_app()

    st.markdown('## NeuroFlake: AI-Powered Data Insights for Snowflake')

    st.markdown("""
    <style>
    .right-container {
        height: 600px;
        overflow-y: auto;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    left_column, right_column = st.columns(2, gap="large")

    with left_column:
        st.markdown("""
        NhanceBot is an AI-powered Data Insight tool designed to help you interact with your Snowflake data warehouse using natural language.

        - **Ask in Plain English**: No need for complex query languages - just ask questions as you normally would.
        - **Instant Answers**: Get the information you need in seconds, without waiting for the IT department.
        - **User-Friendly for Everyone**: From executives to analysts, everyone can now access data insights easily.
        - **Save Time and Resources**: Focus on making decisions, not on figuring out how to get the data.
        - **NhanceBot Gets Smarter with Use**: The more you use NhanceBot, the better it understands your business needs.
        
        Let's explore your data together!
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

    with right_column:
        st.markdown('<div class="right-container">', unsafe_allow_html=True)

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
                        cursor_result = execute_query(sql_response)
                        result_df = cursor_result.fetch_pandas_all()
                        bot_response_2_placeholder.dataframe(result_df)
                        handle_interaction(user_input, sql_response)
                        add_to_chat_history(user_input, sql_response, result_df)
                    except Exception as e:
                        logging.error(f"Error processing query: {str(e)}")
                        st.error("An error occurred while processing your query. Please try again.")

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
                    try:
                        with st.spinner("Generating SQL..."):
                            sql_response = generate_sql(question)
                        bot_response_1_placeholder.code(sql_response, language="sql")
                        cursor_result = execute_query(sql_response)
                        result_df = cursor_result.fetch_pandas_all()
                        bot_response_2_placeholder.dataframe(result_df)
                        handle_interaction(question, sql_response)
                        add_to_chat_history(question, sql_response, result_df)
                    except Exception as e:
                        logging.error(f"Error processing sample question: {str(e)}")
                        st.error("An error occurred while processing your query. Please try again.")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
