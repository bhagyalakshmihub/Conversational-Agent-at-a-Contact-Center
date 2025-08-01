# streamlit_app.py

import streamlit as st
from chatbot_logic import get_response

st.set_page_config(page_title="Conversational Contact Center", page_icon="🤖")

st.title("🤖 Conversational Contact Center AI")
st.markdown("Ask any question, and I’ll fetch the best matching answer.")

# Chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# User input
user_input = st.text_input("You:", "")

if user_input:
    response = get_response(user_input)
    st.session_state.chat.append((user_input, response))

# Display chat
for user_msg, bot_msg in reversed(st.session_state.chat):
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"🧠 **Bot:** {bot_msg}")
