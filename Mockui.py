import streamlit as st
import pandas as pd
import logging
from datetime import date, timedelta

# Initialize session state
def init_app():
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'last_question' not in st.session_state:
        st.session_state['last_question'] = None

# Mock SQL generation function
def generate_sql(user_input):
    # Mock SQL generation logic based on the user_input
    return f"SELECT * FROM mock_table WHERE condition_based_on_input = '{user_input}'"

# Mock query execution function
def execute_query(sql_query):
    # Return a mock DataFrame to simulate SQL execution
    data = {
        'Column 1': [1, 2, 3],
        'Column 2': ['A', 'B', 'C'],
        'Column 3': [10.0, 20.0, 30.0]
    }
    return pd.DataFrame(data)

# Mock function to handle feedback and save it to CSV
def update_feedback(feedback_type, question):
    try:
        # Mock CSV feedback handling
        feedback_data = {'Question': question, 'Feedback': feedback_type}
        df = pd.DataFrame([feedback_data])
        df.to_csv('feedback.csv', mode='a', index=False, header=False)
        return True
    except Exception as e:
        logging.error(f"Error writing feedback to CSV: {str(e)}")
        return False

# Add interaction to chat history
def add_to_chat_history(question, sql_query, result):
    st.session_state['chat_history'].append({
        'question': question,
        'sql_query': sql_query,
        'result': result
    })
    st.session_state['last_question'] = question

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

    # Display the chat history
    for entry in st.session_state['chat_history']:
        with st.chat_message(name="user", avatar="user"):
            st.markdown(entry['question'])
        with st.chat_message(name="assistant", avatar="assistant"):
            st.code(entry['sql_query'], language="sql")
            st.dataframe(entry['result'])

    # Display sample questions as if they are from the assistant
    st.markdown("##### NhanceBot has some sample questions you can ask:")

    sample_questions = [
        "What is the total revenue for each product category?",
        "Who are the top 5 customers by sales volume?",
        "What's the average order value by month?",
        "Which regions have seen the highest growth in the last quarter?",
        "What's the distribution of customer segments across different product lines?"
    ]

    for i, question in enumerate(sample_questions):
        with st.chat_message(name="assistant", avatar="assistant"):
            st.markdown(f"**{question}**")
        if st.button(f"Ask", use_container_width=True, key=f'question{i}'):
            try:
                with st.spinner("Generating SQL..."):
                    sql_response = generate_sql(question)
                with st.chat_message(name="assistant", avatar="assistant"):
                    st.code(sql_response, language="sql")
                    result_df = execute_query(sql_response)
                    st.dataframe(result_df)
                add_to_chat_history(question, sql_response, result_df)
            except Exception as e:
                logging.error(f"Error processing sample question: {str(e)}")
                st.error("An error occurred while processing your query. Please try again.")

    # Chat input for user question
    user_input = st.chat_input("Enter your question about the data:")

    if user_input:
        with st.chat_message(name="user", avatar="user"):
            st.markdown(user_input)
        try:
            with st.spinner("Generating SQL..."):
                sql_response = generate_sql(user_input)
            with st.chat_message(name="assistant", avatar="assistant"):
                st.code(sql_response, language="sql")
                result_df = execute_query(sql_response)
                st.dataframe(result_df)
            add_to_chat_history(user_input, sql_response, result_df)
        except Exception as e:
            logging.error(f"Error processing query: {str(e)}")
            st.error("An error occurred while processing your query. Please try again.")

    # Buttons for Upvote, Downvote, and Clear Chat
    button_column = st.columns([1, 1, 1])
    button_info = st.empty()

    with button_column[0]:
        if st.button("👍 Upvote", key="upvote", use_container_width=True):
            if st.session_state.get('last_question'):
                if update_feedback('upvote', st.session_state['last_question']):
                    button_info.success("Thanks for your feedback! NhanceBot Memory updated")
                else:
                    button_info.error("Failed to update feedback. Please try again.")
            else:
                button_info.warning("No recent question to upvote.")

    with button_column[1]:
        if st.button("👎 Downvote", key="downvote", use_container_width=True):
            if st.session_state.get('last_question'):
                if update_feedback('downvote', st.session_state['last_question']):
                    button_info.warning("We're sorry the result wasn't helpful. Your feedback will help us improve!")
                else:
                    button_info.error("Failed to update feedback. Please try again.")
            else:
                button_info.warning("No recent question to downvote.")

    with button_column[2]:
        if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state['chat_history'] = []
            st.experimental_rerun()  # Refresh the app to clear chat history

if __name__ == "__main__":
    main()
