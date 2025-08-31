import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "https://personaai-backend-15h6.onrender.com/chat")  # backend URL

st.set_page_config(page_title="PersonaAI", page_icon="")
st.title("PersonaAI")
st.markdown(
    "This is an AI assistant that can answer personal questions and other common queries seamlessly."
)
# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history first, below the title
for sender, msg in st.session_state["messages"]:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Sudharsan:** {msg}")

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show loader while waiting for API response
    with st.spinner("Generating response..."):
        try:
            response = requests.post(API_URL, json={"message": user_input})
            response.raise_for_status()
            bot_reply = response.json().get("response", "Sorry, no response from backend.")
        except requests.exceptions.RequestException as e:
            bot_reply = f"Error contacting backend: {e}"

    # Save chat messages
    st.session_state["messages"].append(("You", user_input))
    st.session_state["messages"].append(("Sudharsan", bot_reply))

    # Refresh the chat display with new messages
    st.experimental_rerun()
