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

# Sample questions grouped by table
SAMPLE_QUESTIONS = {
    "CUSTOMERS": {
        "Customer Demographics": [
            "What is the distribution of customer segments?",
            "How many customers do we have in each region?"
        ],
        "Customer Behavior": [
            "Who are our most active customers?",
            "What's the average customer lifetime value?"
        ]
    },
    "ORDERS": {
        "Order Analysis": [
            "What is the average order value by month?",
            "Which days of the week have the highest order volume?"
        ],
        "Order Trends": [
            "What's the month-over-month order growth?",
            "What's the distribution of order sizes?"
        ]
    },
    "PRODUCTS": {
        "Product Performance": [
            "What are our top-selling products?",
            "Which product categories have the highest profit margins?"
        ],
        "Product Analysis": [
            "What's the price distribution across categories?",
            "Which products are frequently bought together?"
        ]
    },
    "SALES": {
        "Sales Analysis": [
            "What's our total revenue by product category?",
            "Which regions have the highest sales growth?"
        ],
        "Sales Trends": [
            "What's our year-over-year sales growth?",
            "What's the seasonal pattern in our sales?"
        ]
    }
}

# Table schemas
TABLE_SCHEMAS = {
    "CUSTOMERS": ["customer_id", "name", "email", "segment", "region"],
    "ORDERS": ["order_id", "customer_id", "order_date", "total_amount"],
    "PRODUCTS": ["product_id", "name", "category", "price", "cost"],
    "SALES": ["sale_id", "product_id", "quantity", "revenue", "date"]
}

# Initialize CSV file
def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['timestamp', 'question', 'result', 'upvote', 'downvote', 'session_id', 'table'])
        df.to_csv(CSV_FILE, index=False)

# Other helper functions remain the same as in your original code
# [load_data, append_to_csv, generate_session_id functions remain unchanged]

# Initialize session state with table selection
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
    if 'selected_table' not in st.session_state:
        st.session_state['selected_table'] = None
    if 'question_groups_expanded' not in st.session_state:
        st.session_state['question_groups_expanded'] = {
            table: {group: False for group in questions.keys()}
            for table, questions in SAMPLE_QUESTIONS.items()
        }

# Handle user interaction with table information
def handle_interaction(question, result, table):
    new_data = pd.DataFrame({
        'timestamp': [datetime.now()],
        'question': [question.strip().replace('\n', ' ')],
        'result': [result.strip().replace('\n', ' ')],
        'upvote': [0],
        'downvote': [0],
        'session_id': [st.session_state['session_id']],
        'table': [table]
    })
    append_to_csv(new_data)
    st.session_state['last_question'] = question.strip().replace('\n', ' ')

# Toggle question group for specific table
def toggle_question_group(table, group):
    st.session_state['question_groups_expanded'][table][group] = not st.session_state['question_groups_expanded'][table][group]

# Process sample question with table context
def process_sample_question(question, table, user_input_placeholder, bot_response_1_placeholder, bot_response_2_placeholder):
    user_input_placeholder.markdown(f"Question about {table}: {question}")
    try:
        sql_response = generate_sql(question)  # You might want to modify this to include table context
        bot_response_1_placeholder.code(sql_response, language="sql")
        result_response = execute_query(sql_response)
        bot_response_2_placeholder.success(result_response)
        handle_interaction(question, result_response, table)
    except Exception as e:
        logging.error(f"Error processing sample question: {str(e)}")
        st.error("An error occurred while processing your query. Please try again.")

# Main app
def main():
    init_session_state()

    st.markdown('## NeuroFlake: AI-Powered Text-to-SQL for Snowflake')

    # Create columns for layout
    left_column, right_column = st.columns(2, gap="large")

    with right_column.container():
        # Table selection radio buttons
        selected_table = st.radio(
            "Select a table to query:",
            options=list(TABLE_SCHEMAS.keys()),
            horizontal=True
        )
        st.session_state['selected_table'] = selected_table

        # Chat interface
        with st.chat_message(name="user", avatar="user"):
            user_input_placeholder = st.empty()
        with st.chat_message(name="assistant", avatar="assistant"):
            bot_response_1_placeholder = st.empty()
            bot_response_2_placeholder = st.empty()

        user_input = st.text_area(f"Enter your question about the {selected_table} table:")

        # Buttons
        button_column = st.columns(3)
        button_info = st.empty()

        with button_column[2]:
            if st.button("🚀 Generate SQL", key="generate_sql", use_container_width=True):
                if user_input:
                    process_sample_question(user_input, selected_table, user_input_placeholder, 
                                         bot_response_1_placeholder, bot_response_2_placeholder)

        # Feedback buttons remain the same
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

        # Display sample questions for selected table
        st.markdown(f"##### Sample questions for {selected_table} table:")
        
        for group, questions in SAMPLE_QUESTIONS[selected_table].items():
            if st.button(f"📁 {group}", key=f"{selected_table}_{group}", use_container_width=True):
                toggle_question_group(selected_table, group)
            
            if st.session_state['question_groups_expanded'][selected_table][group]:
                for i, question in enumerate(questions):
                    question_columns = st.columns([7,1])
                    with question_columns[0]:
                        st.markdown(f"<div class='mytext'>{question}</div>", unsafe_allow_html=True)
                    with question_columns[1]:
                        if st.button("Ask", key=f"{selected_table}_{group}_question_{i}", use_container_width=True):
                            process_sample_question(question, selected_table, user_input_placeholder,
                                                 bot_response_1_placeholder, bot_response_2_placeholder)

    # Left column with schema information
    with left_column:
        st.markdown("""
        Welcome to NeuroFlake! 🧠❄️
        
        Select a table and ask questions about your data using natural language. The sample questions 
        will help you get started with common queries for each table.
        """)
        
        st.markdown(f'##### Schema for {selected_table}:')
        st.markdown(f"Columns: {', '.join(TABLE_SCHEMAS[selected_table])}")
        
        # Display full schema
        st.markdown('##### Full Database Schema:')
        data = {
            'Table': list(TABLE_SCHEMAS.keys()),
            'Columns': [', '.join(columns) for columns in TABLE_SCHEMAS.values()]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, height=500, use_container_width=True)

if __name__ == "__main__":
    main()
