import os
from datetime import datetime, timedelta
import uuid

# ... (keep your existing imports and constants)

DOWNLOAD_FOLDER = "downloads"
DOWNLOAD_EXPIRY_HOURS = 1  # Files will be deleted after this many hours

# ... (keep your existing functions)

# Function to clean up old download files
def cleanup_old_files():
    now = datetime.now()
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        if now - file_modified > timedelta(hours=DOWNLOAD_EXPIRY_HOURS):
            os.remove(file_path)

# Function to generate CSV file and return its path
def generate_csv_file():
    if st.session_state['last_sql']:
        result_df = execute_query(st.session_state['last_sql'])
        filename = f"result_{uuid.uuid4().hex}.csv"
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        result_df.to_csv(file_path, index=False)
        return file_path
    return None

# Modify the main function
def main():
    init_app()
    cleanup_old_files()  # Clean up old files at the start of each session

    # ... (keep your existing code)

    with right_column.container():
        # ... (keep your existing code)

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
                    
                    # Generate CSV file and provide download link
                    csv_file_path = generate_csv_file()
                    if csv_file_path:
                        download_url = f"<a href='file://{csv_file_path}' download>Download full CSV</a>"
                        download_placeholder.markdown(download_url, unsafe_allow_html=True)
                    
                    result_response = f"Query executed successfully. {len(result_df)} rows returned."
                    handle_interaction(user_input, result_response)
                except Exception as e:
                    logging.error(f"Error processing query: {str(e)}")
                    info_placeholder.error(f"An error occurred while processing your query: {str(e)}")

    # ... (keep the rest of your code)

if __name__ == "__main__":
    main()
