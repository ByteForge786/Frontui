import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st

st.set_page_config(page_title="TableLLM", layout="wide")

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

st.markdown('## TableLLM: Single Table Operation')

left_column, right_column = st.columns(2, gap="large")

with right_column.container():
    with st.chat_message(name="user", avatar="user"):
        user_input_placeholder = st.empty()
    with st.chat_message(name="assistant", avatar="assistant"):
        bot_response_1_placeholder = st.empty()
        bot_response_2_placeholder = st.empty()

    user_input = st.text_area("Enter your query:")

    button_column = st.columns(3)
    button_info = st.empty()
    with button_column[2]:
        send_button = st.button("✉️ Send", use_container_width=True)
        if send_button and len(user_input) != 0:
            user_input_placeholder.markdown(user_input)
            # Here you would typically process the user input and generate a response
            # For this example, we'll just echo the input
            bot_response = f"You said: {user_input}"
            bot_response_1_placeholder.markdown(bot_response)

    with button_column[1]:
        upvote_button = st.button("👍 Upvote", use_container_width=True)
        if upvote_button:
            # Here you would typically handle the upvote action
            button_info.success("Your upvote has been recorded")

    with button_column[0]:
        downvote_button = st.button("👎 Downvote", use_container_width=True)
        if downvote_button:
            # Here you would typically handle the downvote action
            button_info.success("Your downvote has been recorded")

    st.markdown("##### Possible questions to ask:")
    sample_questions = [
        "What is the average age in the table?",
        "How many people are from New York?",
        "What is the highest salary?",
        "Can you summarize the data in the table?",
        "Who is the youngest person in the table?"
    ]
    
    for i, question in enumerate(sample_questions):
        question_columns = st.columns([7,1])
        with question_columns[0]:
            st.markdown(f"<div class='mytext'>{question}</div>", unsafe_allow_html=True)
        with question_columns[1]:
            if st.button("Send", use_container_width=True, key=f'question{i}'):
                user_input_placeholder.markdown(question)
                # Here you would typically process the question and generate a response
                bot_response = f"Response to: {question}"
                bot_response_1_placeholder.markdown(bot_response)

with left_column:
    st.markdown('- We will provide you a table and a list of possible questions to ask.\n\n- You can choose one of the provided questions or create your own question to have a conversation with the table.')
    
    # Sample data for the table
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 28, 22],
        'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Boston'],
        'Salary': [50000, 75000, 80000, 65000, 55000]
    }
    df = pd.DataFrame(data)
    
    st.markdown('##### Provided table:')
    st.dataframe(df, height=500, use_container_width=True)
