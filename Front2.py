import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st

st.set_page_config(page_title="NeuroFlake", layout="wide")

if 'chat' not in st.session_state:
    st.session_state['chat'] = {
        "user_input": None,
        "bot_response_1": None,
        "bot_response_2": None,
    }

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = None

text_style = """
    <style>
        .mytext {
            border:1px solid black;
            border-radius:10px;
            border-color: #D6D6D8;
            padding:10px;
            height:auto;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin-bottom: 15px;
        }
    </style>
"""
st.markdown(text_style, unsafe_allow_html=True)

st.markdown('## NeuroFlake: AI-Powered Text-to-SQL for Snowflake')
st.markdown('#### Unlock the power of your data with natural language queries!')

left_column, right_column = st.columns(2, gap="large")

with right_column.container():
    with st.chat_message(name="user", avatar="user"):
        user_input_placeholder = st.empty()
    with st.chat_message(name="assistant", avatar="assistant"):
        bot_response_1_placeholder = st.empty()
        bot_response_2_placeholder = st.empty()

    user_input = st.text_area("Ask NeuroFlake about your data:")

    button_column = st.columns(3)
    button_info = st.empty()
    with button_column[2]:
        send_button = st.button("🚀 Generate SQL", use_container_width=True)
        if send_button and len(user_input) != 0:
            user_input_placeholder.markdown(user_input)
            # Here you would typically process the user input and generate SQL
            bot_response = f"Generated SQL: SELECT * FROM table WHERE condition = '{user_input}'"
            bot_response_1_placeholder.code(bot_response, language='sql')

    with button_column[1]:
        upvote_button = st.button("👍 Helpful", use_container_width=True)
        if upvote_button:
            button_info.success("Thanks for your feedback! We're constantly improving NeuroFlake.")

    with button_column[0]:
        downvote_button = st.button("👎 Not Helpful", use_container_width=True)
        if downvote_button:
            button_info.info("We appreciate your feedback. We'll work on making NeuroFlake better!")

    st.markdown("##### Example queries you can try:")
    sample_questions = [
        "What is the total revenue for each product category?",
        "Who are our top 5 customers by purchase volume?",
        "What's the average order value by month?",
        "Show me the sales trend for the last 12 months",
        "Which regions have the highest customer retention rate?"
    ]
    
    for i, question in enumerate(sample_questions):
        question_columns = st.columns([7,1])
        with question_columns[0]:
            st.markdown(f"<div class='mytext'>{question}</div>", unsafe_allow_html=True)
        with question_columns[1]:
            if st.button("Try", use_container_width=True, key=f'question{i}'):
                user_input_placeholder.markdown(question)
                # Here you would typically process the question and generate a response
                bot_response = f"Generated SQL for: {question}\n\nSELECT * FROM relevant_table WHERE condition = 'example'"
                bot_response_1_placeholder.code(bot_response, language='sql')

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

st.sidebar.markdown("### About NeuroFlake")
st.sidebar.info(
    "NeuroFlake is revolutionizing data analysis by bridging the gap between natural language and SQL. "
    "Our AI-powered solution allows anyone to query complex Snowflake databases using simple, conversational language. "
    "Say goodbye to the days of complex SQL queries and hello to instant data insights!"
)
