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

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3
MAX_ROWS_DISPLAY = 1000
ZIP_FOLDER = "zip_downloads"
SIZE_LIMIT_MB = 190

# Set page config
st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

# Initialize CSV file
def init_csv():
    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=['timestamp', 'question', 'result', 'upvote', 'downvote', 'session_id']).to_csv(CSV_FILE, index=False)

# Load CSV file
@st.cache_data
def load_data():
    try:
        if not os.path.exists(CSV_FILE):
            init_csv()
        return pd.read_csv(CSV_FILE)
    except Exception as e:
        logging.error(f"Error loading CSV: {str(e)}")
        return pd.DataFrame()

# Append data to CSV
def append_to_csv(new_data):
    try:
        with open(CSV_FILE, 'a', newline='') as f:
            new_data.to_csv(f, header=f.tell()==0, index=False)
        return True
    except Exception as e:
        logging.error(f"Error appending to CSV: {str(e)}")
        return False

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
    n_rows = 100  # Reduced for demo purposes
    return pd.DataFrame({
        'id': range(n_rows),
        'value': np.random.rand(n_rows),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_rows)
    })

# Handle user interaction
def handle_interaction(question, result):
    if not question:
        return
        
    new_data = pd.DataFrame({
        'timestamp': [datetime.now()],
        'question': [question.strip().replace('\n', ' ')],
        'result': [result.strip().replace('\n', ' ')],
        'upvote': [0],
        'downvote': [0],
        'session_id': [st.session_state.get('session_id', '')]
    })
    append_to_csv(new_data)

def process_query(question):
    if not question:
        return None
        
    try:
        # Generate SQL
        sql_response = generate_sql(question)
        
        # Execute query
        result_df = execute_query(sql_response)
        
        # Calculate size
        df_size = result_df.memory_usage(deep=True).sum() / (1024 * 1024)
        
        return {
            'sql': sql_response,
            'df': result_df,
            'df_size': df_size
        }
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        st.error(f"An error occurred while processing your query: {str(e)}")
        return None

def display_result(result):
    if not result:
        return
        
    # Display SQL
    st.code(result['sql'], language="sql")
    
    # Display results
    df = result['df']
    df_size = result['df_size']
    
    if df_size > SIZE_LIMIT_MB:
        st.dataframe(df.head(MAX_ROWS_DISPLAY))
        st.info(f"Showing first {MAX_ROWS_DISPLAY} rows of {len(df)} total rows. Total size: {df_size:.2f} MB")
    else:
        st.dataframe(df)
        st.info(f"Showing all {len(df)} rows. Total size: {df_size:.2f} MB")
    
    # Generate and display chart
    fig = generate_chart(df.head(1000))
    if fig:
        st.plotly_chart(fig, use_container_width=True)

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

def main():
    st.markdown('## NeuroFlake: AI-Powered Text-to-SQL for Snowflake')
    
    # Initialize session state
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = hashlib.md5(str(datetime.now()).encode()).hexdigest()
    if 'last_question' not in st.session_state:
        st.session_state['last_question'] = None
    if 'current_result' not in st.session_state:
        st.session_state['current_result'] = None

    # Input section
    user_input = st.text_area("Enter your question about the data:")

    # Button columns
    col1, col2, col3 = st.columns(3)
    
    with col3:
        if st.button("🚀 Generate SQL", use_container_width=True):
            st.session_state['current_result'] = process_query(user_input)
            if st.session_state['current_result']:
                st.session_state['last_question'] = user_input
                handle_interaction(user_input, "Query executed successfully")
                st.experimental_rerun()

    with col2:
        if st.button("👍 Upvote", use_container_width=True):
            if st.session_state.get('last_question'):
                if update_feedback('upvote', st.session_state['last_question']):
                    st.success("Thanks for your feedback!")

    with col1:
        if st.button("👎 Downvote", use_container_width=True):
            if st.session_state.get('last_question'):
                if update_feedback('downvote', st.session_state['last_question']):
                    st.warning("Thanks for your feedback!")

    # Display current result if exists
    if st.session_state.get('current_result'):
        with st.chat_message(name="assistant", avatar="assistant"):
            display_result(st.session_state['current_result'])

    # Sample questions
    st.markdown("##### Sample questions you can ask:")
    sample_questions = [
        "What is the total revenue for each product category?",
        "Who are the top 5 customers by sales volume?",
        "What's the average order value by month?",
        "Which regions have seen the highest growth in the last quarter?",
        "What's the distribution of customer segments across different product lines?"
    ]
    
    for i, question in enumerate(sample_questions):
        col1, col2 = st.columns([7,1])
        with col1:
            st.markdown(f"{question}")
        with col2:
            if st.button("Ask", key=f"ask_{i}", use_container_width=True):
                st.session_state['current_result'] = process_query(question)
                if st.session_state['current_result']:
                    st.session_state['last_question'] = question
                    handle_interaction(question, "Query executed successfully")
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
