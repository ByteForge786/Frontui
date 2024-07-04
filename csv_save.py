import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import csv
from datetime import datetime

# Function to load data from CSV
def load_data():
    try:
        return pd.read_csv('interactions.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['timestamp', 'user_input', 'sql_response', 'query_result', 'feedback'])

# Function to save data to CSV
def save_data(df):
    df.to_csv('interactions.csv', index=False)

# Set page config with dark theme
st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for dark mode
dark_mode_css = """
    <style>
        /* Overall app background */
        .stApp {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #262730 !important;
        }
        
        /* Text input fields */
        .stTextInput > div > div > input {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #4F8BF9 !important;
            color: #FAFAFA !important;
        }
        
        /* DataFrames */
        .dataframe {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Chat messages */
        .stChatMessage {
            background-color: #262730 !important;
        }
        
        /* Custom text boxes */
        .mytext {
            border: 1px solid #4F8BF9 !important;
            border-radius: 10px !important;
            padding: 10px !important;
            height: auto !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            margin-bottom: 15px !important;
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
    </style>
"""

st.markdown(dark_mode_css, unsafe_allow_html=True)

# Load existing data
data = load_data()

if 'chat' not in st.session_state:
    st.session_state['chat'] = {
        "user_input": None,
        "bot_response_1": None,
        "bot_response_2": None,
    }

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = None

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
        send_button = st.button("🚀 Generate SQL", use_container_width=True)
        if send_button and len(user_input) != 0:
            user_input_placeholder.markdown(user_input)
            # Here you would typically process the user input and generate SQL
            sql_response = f"SELECT * FROM sample_table WHERE condition = 'example';"
            bot_response_1_placeholder.code(sql_response, language="sql")
            # Here you would typically execute the SQL and show results
            result_response = "Query executed successfully. 5 rows returned."
            bot_response_2_placeholder.success(result_response)
            
            # Save interaction to dataframe
            new_row = pd.DataFrame({
                'timestamp': [datetime.now()],
                'user_input': [user_input],
                'sql_response': [sql_response],
                'query_result': [result_response],
                'feedback': ['']
            })
            data = pd.concat([data, new_row], ignore_index=True)
            save_data(data)

    with button_column[1]:
        upvote_button = st.button("👍 Upvote", use_container_width=True)
        if upvote_button:
            button_info.success("Your feedback has been recorded. Thanks for helping improve NeuroFlake!")
            data.loc[data.index[-1], 'feedback'] = 'upvote'
            save_data(data)

    with button_column[0]:
        downvote_button = st.button("👎 Downvote", use_container_width=True)
        if downvote_button:
            button_info.warning("We're sorry the result wasn't helpful. Your feedback will help us improve!")
            data.loc[data.index[-1], 'feedback'] = 'downvote'
            save_data(data)

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
            if st.button("Ask", use_container_width=True, key=f'question{i}'):
                user_input_placeholder.markdown(question)
                # Here you would generate and execute SQL based on the question
                sql_response = f"SELECT * FROM relevant_table WHERE condition = 'example';"
                bot_response_1_placeholder.code(sql_response, language="sql")
                result_response = "Query executed successfully. Results would be displayed here."
                bot_response_2_placeholder.success(result_response)
                
                # Save interaction to dataframe
                new_row = pd.DataFrame({
                    'timestamp': [datetime.now()],
                    'user_input': [question],
                    'sql_response': [sql_response],
                    'query_result': [result_response],
                    'feedback': ['']
                })
                data = pd.concat([data, new_row], ignore_index=True)
                save_data(data)

with left_column:
    st.markdown("""
    ### Welcome to NeuroFlake! 🧠❄️
    
    Transform the way you interact with your Snowflake data warehouse:
    
    - **Natural Language Queries**: Ask questions in plain English
    - **Instant SQL Generation**: Get accurate SQL queries in seconds
    - **No SQL Expertise Required**: Empower all team members to access data
    - **Time-Saving**: Focus on insights, not query writing
    - **Continuous Learning**: NeuroFlake improves with every interaction
    
    Start exploring your data effortlessly today!
    """)
    
    st.markdown('##### Sample Table Preview:')
    # This would typically be fetched from your Snowflake database
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
