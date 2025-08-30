# Import the necessary libraries
import streamlit as st  # For creating the web app interface
from google import genai  # For interacting with the Google Gemini API

# --- 1. Page Configuration and Title ---

# Set the title and a caption for the web page
st.title("💬 Gemini Chatbot")
st.caption("A simple and friendly chat using Google's Gemini Flash model")

# --- 2. Sidebar for Settings ---

with st.sidebar:
    st.subheader("Settings")
    reset_button = st.button("Reset Conversation", help="Clear all messages and start fresh")

# --- 3. API Key and Client Initialization ---

# API key langsung ditaruh di sini (hardcoded)
API_KEY = "AIzaSyB3SsFgikJG27FZ469qBYcpgzC1vyZXTkk"  # <<=== Ganti dengan API Key Anda

# Tidak perlu input key dari user lagi
google_api_key = API_KEY  

if ("genai_client" not in st.session_state) or (getattr(st.session_state, "_last_key", None) != google_api_key):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state._last_key = google_api_key
        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
    except Exception as e:
        st.error(f"Invalid API Key: {e}")
        st.stop()

# --- 4. Chat History Management ---

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.genai_client.chats.create(model="gemini-2.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

# --- 5. Display Past Messages ---

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. Handle User Input and API Communication ---

prompt = st.chat_input("Type your message here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        if hasattr(response, "text"):
            answer = response.text
        else:
            answer = str(response)
    except Exception as e:
        answer = f"An error occurred: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
