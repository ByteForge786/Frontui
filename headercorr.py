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
    
    # Parse the SVG
    root = ET.fromstring(content)
    
    # Try to find a rectangle element that might be the background
    background_rect = root.find(".//rect")
    
    if background_rect is not None:
        # Extract fill color or gradient
        fill = background_rect.get('fill')
        if fill and fill.startswith('url(#'):
            # It's a gradient or pattern
            gradient_id = fill[5:-1]  # Remove 'url(#' and ')'
            gradient_element = root.find(f".//*[@id='{gradient_id}']")
            if gradient_element is not None:
                background_svg = ET.tostring(gradient_element).decode()
        else:
            # It's a solid color
            background_svg = f'<rect width="100%" height="100%" fill="{fill}"/>'
    else:
        # If no rectangle found, use the first child of the SVG as background
        background_svg = ET.tostring(root[0]).decode()
    
    # Create a new SVG with the original content centered and background extended
    new_svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="60">
        <defs>
            {background_svg}
        </defs>
        <rect width="100%" height="100%" fill="url(#background)"/>
        <g transform="translate(50%, 30) scale(1)">
            {content}
        </g>
    </svg>
    """
    
    return base64.b64encode(new_svg.encode("utf-8")).decode("utf-8")

# Load SVG files
header_svg = get_svg_content_and_background("header.svg")
footer_svg = get_svg_content_and_background("footer.svg")

# [Rest of your existing code for SQLGenerator, init_csv, load_data, etc.]

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
        .header img, .footer img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .content {
            margin-top: 70px;
            margin-bottom: 70px;
        }
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

    # [Your existing main content code]

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div class="footer">
        <img src="data:image/svg+xml;base64,{footer_svg}" alt="Footer SVG">
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
