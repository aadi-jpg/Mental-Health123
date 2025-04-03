import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Set up the Gemini API Key (Replace with your actual API Key)
API_KEY = "your_actual_api_key_here"  # Replace with your actual Gemini API Key

# Check if API Key is set
if not API_KEY:
    st.error("❌ Missing API Key! Please provide a valid Google Gemini API Key.")
else:
    # Configure Gemini AI
    genai.configure(api_key=API_KEY)

# Initialize Gemini Model
try:
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error(f"⚠️ Error initializing the model: {e}")

# Initialize chat history in session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Streamlit App Title
st.title("📊 Student Mental Health Rating Dashboard")

# Sidebar options
st.sidebar.header("Options")
if st.sidebar.button("Clear Chat"):
    st.session_state['messages'] = []

# Display chat history
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File uploader for Kaggle dataset (CSV format only)
uploaded_file = st.file_uploader("📂 Upload your Kaggle dataset on Student Mental Health (CSV format only)", type=["csv"])

if uploaded_file is not None:
    # Load the dataset
    data = pd.read_csv(uploaded_file)
    
    # Display first few rows
    st.write("### Dataset Overview:")
    st.dataframe(data.head())

    # Extract a random row
    random_row = data.sample(n=1)
    random_row_dict = random_row.to_dict(orient="records")[0]  # Convert to dictionary

    # Convert row to formatted string for prompt
    random_row_str = "\n".join([f"{key}: {value}" for key, value in random_row_dict.items()])

    # Create prompt for Gemini API
    prompt = f"""
    Analyze the following student mental health data and provide a mental health rating (1 to 100),
    where 1 indicates the lowest level of depression and anxiety, and 100 indicates the highest level:
    
    {random_row_str}
    """

    try:
        # Generate response from Gemini API
        response = model.generate_content(prompt)
        bot_response = response.text.strip() if response and response.text else "⚠️ Unable to generate a response."
    except Exception as e:
        bot_response = f"⚠️ Error: {str(e)}"

    # Append response to chat history
    st.session_state['messages'].append({"role": "assistant", "content": bot_response})

    # Display extracted data and AI-generated rating
    st.write("### Extracted Student Data:")
    st.text(random_row_str)
    
    st.write("### AI Mental Health Rating:")
    st.write(bot_response)

# Chat input box for user messages
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message to history
    st.session_state['messages'].append({"role": "user", "content": user_input})

    try:
        # Generate response using Gemini API
        response = model.generate_content(user_input)
        bot_response = response.text.strip() if response and response.text else "⚠️ I'm not sure how to respond."
    except Exception as e:
        bot_response = f"⚠️ Error: {str(e)}"

    # Append response to chat history
    st.session_state['messages'].append({"role": "assistant", "content": bot_response})

    # Display user and AI messages
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(bot_response)
