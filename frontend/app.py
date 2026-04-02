# app.py - Simple Streamlit chat interface
import streamlit as st
import requests

st.set_page_config(page_title="AI Product Chatbot", page_icon="🛒")
st.title("🛒 AI Product Chatbot")
st.caption("Ask anything! It knows our product database + general chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI backend
    try:
        api_response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"question": prompt},
            timeout=30
        )
        api_response.raise_for_status()
        bot_reply = api_response.json()["response"]
    except Exception as e:
        bot_reply = f"❌ Sorry, couldn't connect to backend: {str(e)}"

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)