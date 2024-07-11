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
