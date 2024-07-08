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


import xml.etree.ElementTree as ET

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

header_svg = get_svg_content("header.svg")
footer_svg = get_svg_content("footer.svg")

def main():
    init_app()

    # Custom CSS
    st.markdown("""
    <style>
        /* ... other styles ... */
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
        /* ... other styles ... */
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div class="header">
        <div class="header-bg" style="background-image: url(data:image/svg+xml;base64,{header_svg});"></div>
    </div>
    """, unsafe_allow_html=True)

    # Content
    st.markdown('<div class="content">', unsafe_allow_html=True)

    # ... Your existing content code ...

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div class="footer">
        <div class="footer-bg" style="background-image: url(data:image/svg+xml;base64,{footer_svg});"></div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
