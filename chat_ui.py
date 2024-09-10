import streamlit as st
import pandas as pd
import json
from io import StringIO
import os
from chat_agent import get_user_respose

def load_data(file):
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension == 'csv':
        df = pd.read_csv(file)
    elif file_extension == 'xlsx':
        df = pd.read_excel(file)
    elif file_extension == 'json':
        df = pd.read_json(file)
    else:
        st.error("Unsupported file format. Please upload a CSV, Excel, or JSON file.")
        return None
    
    return df

def save_as_csv(df):
    return df.to_csv(index=False).encode('utf-8')

st.title("Data Q&A App with LLM Agent")

uploaded_file = st.file_uploader("Choose a file (CSV, Excel, or JSON)", type=['csv', 'xlsx', 'json'])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    if df is not None:
        st.write("Data Preview:")
        st.write(df.head())
        
        csv = save_as_csv(df)
        
        # Save the CSV file temporarily
        file_path = "temp_data.csv"
        with open(file_path, "wb") as f:
            f.write(csv)
        
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv",
        )
        
        st.write("Ask a question about the data:")
        user_input = st.text_input("Enter your question here")
        
        if user_input:
            if 'user_input' not in st.session_state:
                st.session_state.user_input = user_input
            
            response,paths = get_user_respose(st.session_state.user_input, file_path)
            st.markdown(response)
        
        # Clean up the temporary file