 # Function to create download button with custom styling
def create_download_button(file_path):
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as file:
            # Create the download button
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
            .stDownloadButton > button {
                background-color: #4CAF50; /* Green background */
                color: white; /* White text */
                padding: 10px 24px; /* Padding */
                font-size: 16px; /* Font size */
                border-radius: 5px; /* Rounded corners */
                border: none; /* Remove borders */
                cursor: pointer; /* Pointer cursor on hover */
            }
            .stDownloadButton > button:hover {
                background-color: #45a049; /* Darker green on hover */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
