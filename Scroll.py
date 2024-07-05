def main():
    init_app()

    st.markdown('## NeuroFlake: AI-Powered Data Insights for Snowflake')

    # Add CSS for scrollable left container
    st.markdown("""
    <style>
    .left-container {
        height: 600px;
        overflow-y: auto;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    left_column, right_column = st.columns(2, gap="large")

    with left_column:
        # Wrap left column content in a scrollable container
        st.markdown('<div class="left-container">', unsafe_allow_html=True)
        
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

        # Close the scrollable container
        st.markdown('</div>', unsafe_allow_html=True)

    with right_column.container():
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

if __name__ == "__main__":
    main()
