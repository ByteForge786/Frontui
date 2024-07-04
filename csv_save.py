import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import os

# Set page config
st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

# Initialize CSV file
csv_file = 'user_interactions.csv'
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=['question', 'result', 'upvote', 'downvote'])
    df.to_csv(csv_file, index=False)

# Load CSV file
@st.cache_data
def load_data():
    data = pd.read_csv(csv_file)
    return data

data = load_data()

# Custom CSS for dark mode and button hover effect
dark_mode_css = """
    <style>
        /* Overall app background */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #262730;
        }
        
        /* Text input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #262730;
            color: #FAFAFA;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #4F8BF9;
            color: #FAFAFA;
            transition: background-color 0.3s, color 0.3s; /* Added color transition */
        }
        
        .stButton > button:hover {
            background-color: #FF6347; /* Change to red on hover */
            color: #FAFAFA; /* Ensure text remains white on hover */
        }
        
        /* DataFrames */
        .css-1ujwg6k, .css-1u7ky9e {
            background-color: #262730;
            color: #FAFAFA;
        }
        
        /* Chat messages */
        .stChatMessage {
            background-color: #262730;
        }
        
        /* Custom text boxes */
        .mytext {
            border: 1px solid #4F8BF9;
            border-radius: 10px;
            padding: 10px;
            height: auto;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin-bottom: 15px;
            background-color: #262730;
            color: #FAFAFA;
        }
    </style>
"""

st.markdown(dark_mode_css, unsafe_allow_html=True)

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
            
            # Append the user interaction to the CSV
            new_data = pd.DataFrame({
                'question': [user_input.strip().replace('\n', ' ')],
                'result': [result_response.strip().replace('\n', ' ')],
                'upvote': [0],
                'downvote': [0]
            })
            new_data.to_csv(csv_file, mode='a', header=False, index=False)

    with button_column[1]:
        upvote_button = st.button("👍 Upvote", use_container_width=True)
        if upvote_button:
            button_info.success("Thanks for your feedback! NeuroFlake Memory updated")
            # Update the last entry in the CSV file to indicate an upvote
            data = pd.read_csv(csv_file)
            data.at[data.index[-1], 'upvote'] = 1
            data.to_csv(csv_file, index=False)

    with button_column[0]:
        downvote_button = st.button("👎 Downvote", use_container_width=True)
        if downvote_button:
            button_info.warning("We're sorry the result wasn't helpful. Your feedback will help us improve!")
            # Update the last entry in the CSV file to indicate a downvote
            data = pd.read_csv(csv_file)
            data.at[data.index[-1], 'downvote'] = 1
            data.to_csv(csv_file, index=False)

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
                
                # Append the user interaction to the CSV
                new_data = pd.DataFrame({
                    'question': [question],
                    'result': [result_response],
                    'upvote': [0],
                    'downvote': [0]
                })
                new_data.to_csv(csv_file, mode='a', header=False, index=False)

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

