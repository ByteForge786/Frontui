# Function to create download button with custom styling
def create_download_button(file_path):
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as file:
            # Add the download button with a custom id
            st.download_button(
                label="Download full CSV as ZIP",
                data=file,
                file_name=os.path.basename(file_path),
                mime="application/zip",
                key="download_button"
            )
        
        # Inject custom CSS for the download button
        st.markdown(
            """
            <style>
            #download_button {
                background-color: #4CAF50; /* Green */
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
            }
            #download_button:hover {
                background-color: #45a049;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

