import streamlit as st
from datetime import date, timedelta

# Get today's date
today = date.today()

# Create the start date input
start_date = st.date_input("Start Date", 
                           value=today,
                           max_value=today)

# Calculate the maximum allowed start date (2 months before today)
max_start_date = today - timedelta(days=60)

# Create the end date input (always set to today)
end_date = st.date_input("End Date", 
                         value=today,
                         min_value=start_date,
                         max_value=today,
                         disabled=True)

# Check if the date range is valid
if start_date < max_start_date:
    st.error("The start date cannot be more than 2 months before the end date.")
else:
    st.success(f"Selected date range: {start_date} to {end_date}")
