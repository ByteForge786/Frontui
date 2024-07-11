
# error_handler.py

import re

def parse_snowflake_error(error_message, query):
    error_message = error_message.lower()
    
    error_types = {
        "object does not exist or not authorized": "I couldn't find one of the tables or columns I thought you were asking about, or I don't have permission to access it.",
        "invalid identifier": "There seems to be an issue with one of the names I used for tables or columns.",
        "syntax error": "I made a mistake in forming the query.",
        "insufficient privileges": "It looks like I don't have permission to access some of the data you're asking about.",
        "database does not exist": "The database I tried to query doesn't seem to exist.",
        "schema does not exist": "I might have misunderstood which part of the database you're interested in.",
        "ambiguous column name": "I used a column name that could belong to multiple tables, causing confusion.",
        "warehouses do not exist": "The compute resources needed to run the query are not available.",
        "invalid data type": "I tried to use a data type that doesn't match what's in the database.",
        "division by zero": "The query attempted to divide by zero, which isn't allowed in mathematics.",
        "numeric value out of range": "A number in the query was too large or too small for the system to handle.",
        "invalid date/timestamp/timespan": "There was an issue with a date, time, or duration in the query.",
        "invalid argument": "One of the arguments I used in a function or operation was not valid.",
        "data exception": "There was a problem with the data values in the query or in the database.",
        "integrity constraint violation": "The query tried to insert or modify data in a way that violates database rules.",
        "serialization failure": "There was a conflict with another operation happening at the same time.",
        "statement timeout": "The query took too long to execute and was stopped.",
        "internal error": "There was an unexpected problem within Snowflake itself.",
        "resource limit exceeded": "The query exceeded the allowed resource usage (like memory or time).",
        "compilation error": "There was a problem in converting the SQL into executable code.",
        "network error": "There was an issue with the network connection to Snowflake.",
        "account suspended": "The Snowflake account is currently suspended and can't be used.",
        "feature not supported": "The query tried to use a feature that isn't available in this version of Snowflake.",
        "invalid object type": "I tried to perform an operation on an object type that doesn't support it.",
        "invalid union": "There was an issue combining results from different SELECT statements.",
        "transaction aborted": "The database operation was rolled back due to an error or manual intervention.",
        "invalid parameter": "One of the parameters passed to a stored procedure or function was invalid.",
    }

    for error_key, error_description in error_types.items():
        if error_key in error_message:
            return error_description, error_key

    return "I encountered an unexpected issue while trying to get your data.", "unknown_error"

def get_error_tips(error_type):
    general_tips = [
        "- Could you rephrase your question using different words?",
        "- Can you provide more context about what you're looking for?",
        "- If you mentioned specific names, could you double-check their spelling?",
        "- Would it help if we broke your question down into smaller parts?",
    ]

    specific_tips = {
        "object does not exist or not authorized": [
            "- Can you confirm the names of the tables or columns you're interested in?",
            "- Are you sure this data exists in our system and that you have permission to access it?",
        ],
        "invalid identifier": [
            "- Did I misunderstand any names you mentioned? Could you clarify them?",
            "- If you used any abbreviations, could you spell them out for me?",
            "- Are you sure the column or table name you're asking about exists in the database?",
        ],
        "syntax error": [
            "- Could you simplify your question or break it down into smaller parts?",
            "- Are there any specific terms or phrases you used that might be causing confusion?",
        ],
        "insufficient privileges": [
            "- Are you sure you have access to all the data you're asking about?",
            "- Could we rephrase the question to focus on data you know you have access to?",
        ],
        "database does not exist": [
            "- Can you confirm which database you're trying to query?",
            "- Is it possible you're asking about data from a different system?",
        ],
        "schema does not exist": [
            "- Could you specify which part of the database you're interested in?",
            "- Are you sure the schema name you're using is correct?",
        ],
        "ambiguous column name": [
            "- I got confused about which table some information came from. Can you be more specific?",
            "- Could you tell me which aspects of the data are most important to you?",
        ],
        "warehouses do not exist": [
            "- The system might be experiencing resource issues. Could we try a simpler query?",
            "- Would it be okay to try this request again in a few minutes?",
        ],
        "invalid data type": [
            "- Could you clarify the type of data you're looking for (e.g., numbers, dates, text)?",
            "- Are you trying to compare different types of data that might not be compatible?",
        ],
        "division by zero": [
            "- It looks like we're trying to divide by zero somewhere. Can you rephrase your question to avoid this?",
            "- Are you asking for a ratio or percentage? If so, could you provide more context?",
        ],
        "numeric value out of range": [
            "- The numbers involved seem to be very large or very small. Could you provide a different range?",
            "- Are you looking for an exact value, or would an approximation be helpful?",
        ],
        "invalid date/timestamp/timespan": [
            "- Could you clarify the date or time range you're interested in?",
            "- Are you using any specific date formats I should be aware of?",
        ],
        "invalid argument": [
            "- I might have misunderstood part of your request. Could you rephrase it?",
            "- Are there any specific calculations or comparisons you're trying to make?",
        ],
        "data exception": [
            "- There might be some unexpected data in the database. Could we try a more general query?",
            "- Are you looking for specific values, or more general trends?",
        ],
        "integrity constraint violation": [
            "- It seems like the operation would break some rules in the database. Can we rephrase the question?",
            "- Are you trying to modify data, or just retrieve it?",
        ],
        "serialization failure": [
            "- There might be a lot of activity in the database right now. Could we try again in a moment?",
            "- Would it help to focus on a smaller subset of the data?",
        ],
        "statement timeout": [
            "- The query is taking too long. Could we simplify it or focus on a smaller dataset?",
            "- Would it be helpful to break this question into smaller parts?",
        ],
        "internal error": [
            "- There seems to be an issue with the database itself. Should we try a simpler query?",
            "- Would it be okay to attempt this request again in a few minutes?",
        ],
        "resource limit exceeded": [
            "- The query is using too many resources. Can we simplify it or focus on less data?",
            "- Would it be helpful to break this question into smaller parts?",
        ],
        "compilation error": [
            "- There's an issue with how the query is structured. Could you rephrase your question?",
            "- Are there any complex calculations or conditions in your request we could simplify?",
        ],
        "network error": [
            "- There seems to be a connection issue. Could we try your request again in a moment?",
            "- Is it possible to rephrase your question to require less data transfer?",
        ],
        "account suspended": [
            "- It looks like there's an account-level issue. You might need to contact your database administrator.",
            "- In the meantime, is there a different data source we could use to answer your question?",
        ],
        "feature not supported": [
            "- I tried to use a feature that's not available. Could we rephrase the question to use simpler operations?",
            "- Are there alternative ways you could express what you're looking for?",
        ],
        "invalid object type": [
            "- I might have misunderstood the type of data you're asking about. Could you clarify?",
            "- Can you provide more context about the specific information you need?",
        ],
        "invalid union": [
            "- I'm having trouble combining different sets of data. Could we focus on one type of data at a time?",
            "- Can you break down your question into smaller, more specific parts?",
        ],
        "transaction aborted": [
            "- The operation was cancelled. Could we try a simpler version of your request?",
            "- Would it be okay to attempt this request again in a few minutes?",
        ],
        "invalid parameter": [
            "- One of the values I used wasn't correct. Could you double-check any specific values you mentioned?",
            "- Can you provide more details about the exact information you're looking for?",
        ],
        "unknown_error": [
            "- The error I encountered is not one I'm specifically trained to handle. Can you double-check your request?",
            "- Is there any additional information you can provide about the data you're looking for?",
            "- If you're using any technical terms or jargon, could you explain them in simpler terms?",
            "- Would it be helpful if we approached this question from a different angle?",
        ]
    }

    return specific_tips.get(error_type, []) + general_tips










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
                error_message, error_type = parse_snowflake_error(str(e), sql_response)
                st.error(f"I'm sorry, I ran into a problem: {error_message}")
                st.info("Here are some tips that might help:")
                tips = get_error_tips(error_type)
                for tip in tips:
                    st.markdown(tip)
                if error_type == "unknown_error":
                    st.markdown(f"For reference, the full error message was: {str(e)}")
                st.markdown("If none of these help, feel free to ask your question in a different way!")
            except Exception as e:
                logging.error(f"Error processing query: {str(e)}")
                st.error("I'm having trouble understanding that. Could you try asking in a different way?")
                st.info("Here are some general tips that might help:")
                tips = get_error_tips("unknown_error")
                for tip in tips:
                    st.markdown(tip)

if __name__ == "__main__":
    main()
