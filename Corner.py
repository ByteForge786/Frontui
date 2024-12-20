import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import os
from datetime import datetime
import hashlib
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set page config
st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3

# Sample questions grouped
SAMPLE_QUESTIONS = {
    "Revenue Analysis": [
        "What is the total revenue for each product category?",
        "What's the average order value by month?"
    ],
    "Customer Insights": [
        "Who are the top 5 customers by sales volume?",
        "What's the distribution of customer segments across different product lines?"
    ],
    "Regional Performance": [
        "Which regions have seen the highest growth in the last quarter?",
        "What's the year-over-year growth by region?"
    ]
}

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

# Initialize session state
def init_session_state():
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
    if 'question_groups_expanded' not in st.session_state:
        st.session_state['question_groups_expanded'] = {group: False for group in SAMPLE_QUESTIONS.keys()}

# Mock function for SQL generation
def generate_sql(question):
    return f"SELECT * FROM sample_table WHERE condition = '{question}';"

# Mock function for query execution
def execute_query(sql):
    return "Query executed successfully. 5 rows returned."

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

# Toggle question group
def toggle_question_group(group):
    st.session_state['question_groups_expanded'][group] = not st.session_state['question_groups_expanded'][group]

# Process sample question
def process_sample_question(question, user_input_placeholder, bot_response_1_placeholder, bot_response_2_placeholder):
    user_input_placeholder.markdown(question)
    try:
        sql_response = generate_sql(question)
        bot_response_1_placeholder.code(sql_response, language="sql")
        result_response = execute_query(sql_response)
        bot_response_2_placeholder.success(result_response)
        handle_interaction(question, result_response)
    except Exception as e:
        logging.error(f"Error processing sample question: {str(e)}")
        st.error("An error occurred while processing your query. Please try again.")

# Main app
def main():
    init_session_state()

    st.markdown('## NeuroFlake: AI-Powered Text-to-SQL for Snowflake')

    left_column, right_column = st.columns(2, gap="large")

    with right_column.container():
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
                    process_sample_question(user_input, user_input_placeholder, 
                                         bot_response_1_placeholder, bot_response_2_placeholder)

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
        
        # Display grouped sample questions with expandable sections
        for group, questions in SAMPLE_QUESTIONS.items():
            if st.button(f"📁 {group}", key=f"group_{group}", use_container_width=True):
                toggle_question_group(group)
            
            if st.session_state['question_groups_expanded'][group]:
                for i, question in enumerate(questions):
                    question_columns = st.columns([7,1])
                    with question_columns[0]:
                        st.markdown(f"<div class='mytext'>{question}</div>", unsafe_allow_html=True)
                    with question_columns[1]:
                        if st.button("Ask", key=f"{group}_question_{i}", use_container_width=True):
                            process_sample_question(question, user_input_placeholder,
                                                 bot_response_1_placeholder, bot_response_2_placeholder)

    with left_column:
        st.markdown("""
        Welcome to NeuroFlake! 🧠❄️
        
        NeuroFlake is an AI-powered text-to-SQL tool designed to help you interact with your Snowflake data warehouse using natural language. Here's how it works:

        1. **Ask a Question**: Type your question about your data in plain English.
        2. **Generate SQL**: NeuroFlake will interpret your question and generate the appropriate SQL query.
        3. **View Results**: The query will be executed on your Snowflake database, and the results will be displayed.
        4. **Iterate**: Refine your question or ask follow-up questions to dive deeper into your data.

        You can use the sample questions provided or create your own. NeuroFlake is here to make data analysis accessible to everyone, regardless of their SQL expertise.

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

if __name__ == "__main__":
    main()
