import streamlit as st
from chatbot_logic import get_response

st.set_page_config(page_title="ChatBot AI 🤖", layout="centered")

# Inject custom CSS for animations & layout
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #2c3e50, #3498db);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .typing-title {
        font-size: 36px;
        white-space: nowrap;
        overflow: hidden;
        border-right: 4px solid #fff;
        width: 0;
        animation: typing 3s steps(30, end) forwards, blink 0.75s step-end infinite;
        margin-bottom: 30px;
    }
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    @keyframes blink {
        from, to { border-color: transparent }
        50% { border-color: white; }
    }
    .chat-bubble-user {
        background-color: #1abc9c;
        padding: 12px;
        border-radius: 12px;
        margin: 10px 0;
        color: white;
        text-align: right;
    }
    .chat-bubble-bot {
        background-color: #34495e;
        padding: 12px;
        border-radius: 12px;
        margin: 10px 0;
        color: white;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# Animated typing title
st.markdown("<div class='typing-title'>🤖 Conversational Contact AI</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🌟 About This App")
    st.info("Ask any question related to your service center.")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat = []

# Chat session
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat
for user, bot in reversed(st.session_state.chat):
    st.markdown(f"<div class='chat-bubble-user'>You: {user}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble-bot'>Bot: {bot}</div>", unsafe_allow_html=True)

# Input field
user_input = st.chat_input("Type your message here...")

if user_input:
    response = get_response(user_input)
    st.session_state.chat.append((user_input, response))
