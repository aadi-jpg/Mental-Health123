import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Securely fetch API key from environment variable
API_KEY = "AIzaSyDkjZdiR--evioaIRmO-NM4670sFhSo4zQ"
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Initialize chat history if not already
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title("Student Mental Health Rating Dashboard")

# Sidebar with options
st.sidebar.header("Options")
if st.sidebar.button("Clear Chat"):
    st.session_state['messages'] = []

# Display chat history
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File uploader for Kaggle datasets (CSV format only)
uploaded_file = st.file_uploader("Upload your Kaggle dataset on Student Mental Health (CSV format only)", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded dataset
    data = pd.read_csv(uploaded_file)
    
    # Display the first few rows of the dataset
    st.write("### Dataset Overview:")
    st.dataframe(data.head())
    
    # Extract a random row from the dataset
    random_row = data.sample(n=1)
    random_row_dict = random_row.to_dict(orient="records")[0]  # Convert to dictionary
    
    # Convert the random row to a formatted string for display
    random_row_str = "\n".join([f"{key}: {value}" for key, value in random_row_dict.items()])
    
    # Generate a prompt for the Gemini API to analyze the data
    prompt = f"""
    Given the following student mental health data, provide a mental health rating (1 to 100), 
    where 100 indicates the highest level of depression and anxiety:
    
    {random_row_str}
    """
    
    try:
        # Generate a response using the Gemini API
        response = model.generate_content(prompt)
        bot_response = response.text if response and response.text else "Unable to generate a response."
    except Exception as e:
        bot_response = f"Error: {str(e)}"
    
    # Append response to chat history
    st.session_state['messages'].append({"role": "assistant", "content": bot_response})
    
    # Display extracted data and rating
    st.write("### Extracted Student Data:")
    st.text(random_row_str)
    
    st.write("### Mental Health Rating:")
    st.write(bot_response)

# User input for chat messages
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message to history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Generate response using Gemini API
    try:
        response = model.generate_content(user_input)
        bot_response = response.text if response and response.text else "I'm not sure how to respond."
    except Exception as e:
        bot_response = f"Error: {str(e)}"
    
    # Append response to chat history
    st.session_state['messages'].append({"role": "assistant", "content": bot_response})
    
    # Display user and bot messages
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(bot_response)
