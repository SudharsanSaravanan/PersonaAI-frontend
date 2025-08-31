import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API URL from .env
API_URL = os.getenv("API_URL")
if not API_URL:
    st.error("API_URL not set in environment variables!")
    st.stop()

st.set_page_config(page_title="PersonaAI", page_icon="")
st.title("PersonaAI")

# Optional: description below title
st.markdown(
    "This is an AI assistant that can answer personal questions and other common queries seamlessly. "
    "If the response is taking a moment, the AI is setting up—please wait a little."
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    try:
        # Show loader while waiting for response
        with st.spinner("Generating response..."):
            # Send request to backend
            response = requests.post(API_URL, json={"message": user_input})
            response.raise_for_status()  # Raise error if request failed
            bot_reply = response.json().get("response", "Sorry, no response from backend.")

    except requests.exceptions.RequestException as e:
        bot_reply = f"Error contacting backend: {e}"

    # Save chat messages
    st.session_state["messages"].append(("You", user_input))
    st.session_state["messages"].append(("Sudharsan", bot_reply))

# Display chat history
for sender, msg in st.session_state["messages"]:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Sudharsan:** {msg}")