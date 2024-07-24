import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import streamlit as st
import os
from datetime import datetime, timedelta
import hashlib
import logging
import io
import uuid

# ... (keep all the previous imports and constants)

# Modify the generate_csv_file function
def generate_csv_file():
    if st.session_state['last_sql']:
        result_df = execute_query(st.session_state['last_sql'])
        filename = f"result_{uuid.uuid4().hex}.csv"
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        result_df.to_csv(file_path, index=False)
        return file_path
    return None

# Add a new function to create a download button
def create_download_button(file_path):
    with open(file_path, "rb") as file:
        btn = st.download_button(
            label="Download full CSV",
            data=file,
            file_name=os.path.basename(file_path),
            mime="text/csv"
        )

# Main app
def main():
    init_app()
    cleanup_old_files()  # Clean up old files at the start of each session

    # ... (keep the rest of the main function as is)

    with right_column.container():
        # ... (keep the existing code)

        with button_column[2]:
            if st.button("🚀 Generate SQL", key="generate_sql", use_container_width=True):
                if user_input:
                    user_input_placeholder.markdown(user_input)
                    try:
                        sql_response = generate_sql(user_input)
                        st.session_state['last_sql'] = sql_response
                        bot_response_1_placeholder.code(sql_response, language="sql")
                        
                        result_df = execute_query(sql_response)
                        
                        df_size = result_df.memory_usage(deep=True).sum() / (1024 * 1024)  # Size in MB
                        
                        limited_result = result_df.head(MAX_ROWS_DISPLAY)
                        bot_response_2_placeholder.dataframe(limited_result)
                        info_placeholder.info(f"Showing first {MAX_ROWS_DISPLAY} rows of {len(result_df)} total rows. Total size: {df_size:.2f} MB")
                        
                        # Generate CSV file and provide download button
                        csv_file_path = generate_csv_file()
                        if csv_file_path:
                            create_download_button(csv_file_path)
                        
                        result_response = f"Query executed successfully. {len(result_df)} rows returned."
                        handle_interaction(user_input, result_response)
                    except Exception as e:
                        logging.error(f"Error processing query: {str(e)}")
                        info_placeholder.error(f"An error occurred while processing your query: {str(e)}")

        # ... (keep the rest of the code as is)

        for i, question in enumerate(sample_questions):
            question_columns = st.columns([7,1])
            with question_columns[0]:
                st.markdown(f"<div class='mytext'>{question}</div>", unsafe_allow_html=True)
            with question_columns[1]:
                if st.button(f"Ask", use_container_width=True, key=f'question{i}'):
                    user_input_placeholder.markdown(question)
                    try:
                        sql_response = generate_sql(question)
                        st.session_state['last_sql'] = sql_response
                        bot_response_1_placeholder.code(sql_response, language="sql")
                        result_df = execute_query(sql_response)
                        
                        df_size = result_df.memory_usage(deep=True).sum() / (1024 * 1024)  # Size in MB
                        
                        limited_result = result_df.head(MAX_ROWS_DISPLAY)
                        bot_response_2_placeholder.dataframe(limited_result)
                        info_placeholder.info(f"Showing first {MAX_ROWS_DISPLAY} rows of {len(result_df)} total rows. Total size: {df_size:.2f} MB")
                        
                        # Generate CSV file and provide download button
                        csv_file_path = generate_csv_file()
                        if csv_file_path:
                            create_download_button(csv_file_path)
                        
                        result_response = f"Query executed successfully. {len(result_df)} rows returned."
                        handle_interaction(question, result_response)
                    except Exception as e:
                        logging.error(f"Error processing sample question: {str(e)}")
                        info_placeholder.error(f"An error occurred while processing your query: {str(e)}")

    # ... (keep the rest of the main function as is)

if __name__ == "__main__":
    main()
