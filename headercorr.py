import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import os
from datetime import datetime
import hashlib
import logging
import base64
import xml.etree.ElementTree as ET
import re

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set page config
st.set_page_config(page_title="NhanceBot", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3

def get_svg_content_and_background(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    
    # Try to extract background color from SVG
    background_color = '#FFFFFF'  # Default to white
    match = re.search(r'fill=["\']([^"\']+)["\']', content)
    if match:
        background_color = match.group(1)
    
    return base64.b64encode(content.encode("utf-8")).decode("utf-8"), background_color

# Load SVG files
header_svg, header_bg = get_svg_content_and_background("header.svg")
footer_svg, footer_bg = get_svg_content_and_background("footer.svg")

# [Rest of your existing code for SQLGenerator, init_csv, load_data, etc.]

# Main app
def main():
    init_app()

    # Custom CSS
    st.markdown(f"""
    <style>
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }}
        .stApp > header {{
            background-color: transparent;
        }}
        .stApp {{
            margin-top: -80px;
        }}
        .css-1544g2n {{
            padding-top: 0rem;
        }}
        .css-18e3th9 {{
            padding-top: 0rem;
            padding-bottom: 0rem;
        }}
        .css-1d391kg {{
            padding-top: 1rem;
        }}
        .logo-container {{
            margin-top: 1rem;
        }}
        .header, .footer {{
            position: fixed;
            left: 0;
            right: 0;
            height: 60px;
            z-index: 999;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }}
        .header {{
            top: 0;
            border-bottom: 1px solid #ddd;
            background-color: {header_bg};
        }}
        .footer {{
            bottom: 0;
            border-top: 1px solid #ddd;
            background-color: {footer_bg};
        }}
        .header img, .footer img {{
            height: 100%;
            width: auto;
            max-width: none;
        }}
        .content {{
            margin-top: 70px;
            margin-bottom: 70px;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div class="header">
        <img src="data:image/svg+xml;base64,{header_svg}" alt="Header SVG">
    </div>
    """, unsafe_allow_html=True)

    # Content
    st.markdown('<div class="content">', unsafe_allow_html=True)

    # Logo and Title
    col1, col2 = st.columns([0.2, 3])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image("logo.png", width=60)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("<h1 style='color: maroon; margin-bottom: 0;'>NhanceBot</h1>", unsafe_allow_html=True)

    # Main content
    st.markdown("""
    NhanceBot is an AI-powered Data Insight tool designed to help you interact with 
    your Snowflake data warehouse using natural language.
    """)

    # [Rest of your existing main content code]

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div class="footer">
        <img src="data:image/svg+xml;base64,{footer_svg}" alt="Footer SVG">
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333



import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import os
from datetime import datetime
import hashlib
import logging
import base64
import xml.etree.ElementTree as ET

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set page config
st.set_page_config(page_title="NhanceBot", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3

# Function to read and encode SVG files
def get_svg_content(file_path, square_size=48):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Get original dimensions
    width = int(root.attrib['width'])
    height = int(root.attrib['height'])
    
    # Calculate the starting x-coordinate for the square
    start_x = width - square_size
    
    # Create a new SVG with the extracted square
    new_svg = ET.Element('svg', {
        'width': str(square_size),
        'height': str(square_size),
        'viewBox': f"{start_x} 0 {square_size} {square_size}"
    })
    
    # Copy all elements from the original SVG
    for child in root:
        new_svg.append(child)
    
    # Convert to string and encode
    svg_str = ET.tostring(new_svg, encoding='unicode')
    return base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")

# Load SVG files
header_svg = get_svg_content("header.svg")
footer_svg = get_svg_content("footer.svg")

# ... (Keep all your other functions like SQLGenerator, init_csv, load_data, etc.)

# Main app
def main():
    init_app()

    # Custom CSS
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        .stApp > header {
            background-color: transparent;
        }
        .stApp {
            margin-top: -80px;
        }
        .css-1544g2n {
            padding-top: 0rem;
        }
        .css-18e3th9 {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
        .css-1d391kg {
            padding-top: 1rem;
        }
        .logo-container {
            margin-top: 1rem;
        }
        .header, .footer {
            position: fixed;
            left: 0;
            right: 0;
            height: 60px;
            z-index: 999;
            background-color: white;
            padding: 0;
            overflow: hidden;
        }
        .header {
            top: 0;
            border-bottom: 1px solid #ddd;
        }
        .footer {
            bottom: 0;
            border-top: 1px solid #ddd;
        }
        .header-bg, .footer-bg {
            width: 100%;
            height: 100%;
            background-repeat: repeat-x;
            background-size: auto 100%;
        }
        .content {
            margin-top: 70px;
            margin-bottom: 70px;
        }
    </style>

    <div class="header">
        <div class="header-bg" style="background-image: url(data:image/svg+xml;base64,{header_svg});"></div>
    </div>

    <div class="content">
    """, unsafe_allow_html=True)

    # Logo and Title
    col1, col2 = st.columns([0.2, 3])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image("logo.png", width=60)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("<h1 style='color: maroon; margin-bottom: 0;'>NhanceBot</h1>", unsafe_allow_html=True)

    # Main content
    st.markdown("""
    NhanceBot is an AI-powered Data Insight tool designed to help you interact with 
    your Snowflake data warehouse using natural language.
    """)

    left_column, right_column = st.columns(2, gap="large")

    with left_column:
        st.markdown("""
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

    with right_column:
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
                        result_df = execute_query(sql_response)
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
                        result_df = execute_query(sql_response)
                        bot_response_2_placeholder.dataframe(result_df)
                        handle_interaction(question, sql_response)
                        add_to_chat_history(question, sql_response, result_df)
                    except Exception as e:
                        logging.error(f"Error processing sample question: {str(e)}")
                        st.error("An error occurred while processing your query. Please try again.")

    st.markdown("""
    </div>

    <div class="footer">
        <div class="footer-bg" style="background-image: url(data:image/svg+xml;base64,{footer_svg});"></div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
