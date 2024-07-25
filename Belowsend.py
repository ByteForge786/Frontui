if st.button("🚀 Generate SQL", key="generate_sql", use_container_width=True):
    if user_input:
        user_input_placeholder.markdown(user_input)
        try:
            with st.spinner("Generating SQL..."):
                sql_response = generate_sql(user_input)
            bot_response_1_placeholder.code(sql_response, language="sql")
            result_df = execute_query(sql_response)
            bot_response_2_placeholder.dataframe(result_df)
            handle_interaction(user_input, sql_response)
            add_to_chat_history(user_input, sql_response, result_df)
            # Clear the input box
            st.session_state.user_input = ""
        except ProgrammingError as e:
            error_message, error_type = parse_snowflake_error(str(e), sql_response)
            bot_response_2_placeholder.error(f"I'm sorry, I ran into a problem: {error_message}")
            bot_response_2_placeholder.info("Here are some tips that might help:")
            tips = get_error_tips(error_type)
            for tip in tips:
                bot_response_2_placeholder.markdown(tip)
            if error_type == "unknown_error":
                bot_response_2_placeholder.markdown(f"For reference, the full error message was: {str(e)}")
            bot_response_2_placeholder.markdown("If none of these help, feel free to ask your question in a different way!")
        except Exception as e:
            logging.error(f"Error processing query: {str(e)}")
            bot_response_2_placeholder.error("I'm having trouble understanding that. Could you try asking in a different way?")
            bot_response_2_placeholder.info("Here are some general tips that might help:")
            tips = get_error_tips("unknown_error")
            for tip in tips:
                bot_response_2_placeholder.markdown(tip)
