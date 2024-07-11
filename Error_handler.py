# error_handler.py

import re

def parse_snowflake_error(error_message, query):
    error_message = error_message.lower()
    
    error_types = {
        "object does not exist": "I couldn't find one of the tables or columns I thought you were asking about.",
        "invalid identifier": "There seems to be an issue with one of the names I used for tables or columns.",
        "syntax error": "I made a mistake in forming the query.",
        "insufficient privileges": "It looks like I don't have permission to access some of the data you're asking about.",
        "column not found": "One of the columns I tried to use doesn't seem to exist in the table.",
        "table not found": "I couldn't find one of the tables I thought you were asking about.",
        "schema not found": "I might have misunderstood which part of the database you're interested in.",
        "ambiguous column name": "I used a column name that could belong to multiple tables, causing confusion.",
    }

    for error_key, error_description in error_types.items():
        if error_key in error_message:
            return error_description

    return "I encountered an unexpected issue while trying to get your data."

def get_error_tips(error_message):
    general_tips = [
        "- Could you rephrase your question using different words?",
        "- Can you provide more context about what you're looking for?",
        "- If you mentioned specific names, could you double-check their spelling?",
        "- Would it help if we broke your question down into smaller parts?",
    ]

    specific_tips = {
        "object does not exist": [
            "- Can you confirm the names of the tables or columns you're interested in?",
            "- Are you sure this data exists in our system?",
        ],
        "invalid identifier": [
            "- Did I misunderstand any names you mentioned? Could you clarify them?",
            "- If you used any abbreviations, could you spell them out for me?",
        ],
        "column not found": [
            "- Could you list the specific pieces of information you're looking for?",
            "- Are you sure all these details are in the same table?",
        ],
        "table not found": [
            "- Can you tell me more about the kind of data you're looking for?",
            "- Is it possible you're asking about data from a different system?",
        ],
        "ambiguous column name": [
            "- I got confused about which table some information came from. Can you be more specific?",
            "- Could you tell me which aspects of the data are most important to you?",
        ],
    }

    error_lower = error_message.lower()
    for error_key, tips in specific_tips.items():
        if error_key in error_lower:
            return "\n".join(tips + general_tips)

    return "\n".join(general_tips)












# main.py

import streamlit as st
import logging
from datetime import datetime
import hashlib
from snowflake.connector.errors import ProgrammingError
from error_handler import parse_snowflake_error, get_error_tips

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Custom exception for Snowflake query errors
class SnowflakeQueryError(Exception):
    pass

def generate_sql(question):
    # This is a placeholder. Replace with your actual SQL generation logic
    return f"SELECT * FROM sample_table WHERE condition = '{question}';"

def execute_query(sql):
    # This is a placeholder. Replace with your actual Snowflake query execution logic
    # For demonstration, we'll raise an error
    raise ProgrammingError("Object 'SAMPLE_TABLE' does not exist or not authorized.")

def handle_interaction(question, result):
    # This is a placeholder. Replace with your actual interaction handling logic
    pass

def generate_session_id():
    return hashlib.md5(str(datetime.now()).encode()).hexdigest()

def main():
    st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = generate_session_id()

    st.markdown('## NeuroFlake: AI-Powered Text-to-SQL for Snowflake')

    user_input = st.text_area("What would you like to know about your data?")

    if st.button("🚀 Get Answer", key="generate_answer", use_container_width=True):
        if user_input:
            try:
                sql_response = generate_sql(user_input)
                result_response = execute_query(sql_response)
                st.success(result_response)
                handle_interaction(user_input, result_response)
            except ProgrammingError as e:
                error_message = parse_snowflake_error(str(e), sql_response)
                st.error(f"I'm sorry, I ran into a problem: {error_message}")
                st.info("Let me know if any of these help:")
                st.markdown(get_error_tips(error_message))
                st.markdown("If none of these help, feel free to ask your question in a different way!")
            except Exception as e:
                logging.error(f"Error processing query: {str(e)}")
                st.error("I'm having trouble understanding that. Could you try asking in a different way?")

if __name__ == "__main__":
    main()


