import streamlit as st
import pandas as pd
import os
import sweetviz as sv
import re
from analysis_agent import get_analysis
from chat_agent import get_user_respose

# Set up directories for saving files and charts
DATA_DIR = "data"
CHARTS_DIR = "charts"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

# Function to convert uploaded file into a Pandas DataFrame
def save_uploaded_file(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1]
    file_path = os.path.join(DATA_DIR, uploaded_file.name)
    
    if file_extension == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_extension == 'json':
        df = pd.read_json(uploaded_file)
    elif file_extension == 'xlsx':
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV, JSON, or Excel file.")
        return None
    
    # Save the file locally in CSV format
    df.to_csv(file_path, index=False)
    return df, file_path

# Function to generate and clean Sweetviz report HTML
def generate_sweetviz_report(df, report_file_name="sweetviz_report.html"):
    report = sv.analyze(df)
    report.show_html(filepath=report_file_name, open_browser=False)
    
    with open(report_file_name, "r", encoding="utf-8") as file:
        report_html = file.read()
    
    # Modify the HTML to remove fixed width and allow full-width display
    modified_html = report_html.replace('<body>', '<body style="width: 100%; max-width: none; padding: 0; margin: 0;">')
    modified_html = modified_html.replace('div.content{', 'div.content{width: 100%; max-width: none; padding: 0; margin: 0;')
    
    with open(report_file_name, "w", encoding="utf-8") as file:
        file.write(modified_html)
    
    return modified_html, report_file_name




# In the main Streamlit UI section:

st.title("Analysis & Chat Agent")

# File uploader for CSV, JSON, Excel files
uploaded_file = st.file_uploader("Upload a file (CSV, JSON, Excel)", type=["csv", "json", "xlsx"])

# Check if a file has been uploaded and process it
if uploaded_file is not None:
    df, file_path = save_uploaded_file(uploaded_file)
    st.write("File successfully uploaded and saved as CSV.")
    st.dataframe(df.head())  # Display the first few rows of the uploaded file

    # Sweetviz Report Section
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            report_html, report_file_path = generate_sweetviz_report(df)
            st.success("Report generated!")
            st.markdown( """ <style> .stContainer > div { width: 95%; margin: auto; } </style> """, unsafe_allow_html=True )
            st.components.v1.html(report_html, width=1200, height=600, scrolling=True)
            
            # Provide download link for the report
            st.markdown(f"Download the full report: [Download Report]({report_file_path})")


# Define session state for caching chart analysis and chat history
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None  # Cache for analysis result (charts, etc.)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # Cache for chat history
    
if 'user_input' not in st.session_state:
    st.session_state.user_input = None

# Analysis Section
if st.button("Get Analysis"):
    if st.session_state.analysis_result is None:
        # Run the LLM analysis agent and generate charts
        with st.spinner("Running analysis..."):
            st.session_state.analysis_result = get_analysis(file_path)
    st.markdown("## Analysis Results:")
    st.markdown(st.session_state.analysis_result)


