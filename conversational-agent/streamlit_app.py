import streamlit as st
from chatbot_logic import get_response

# Streamlit page config
st.set_page_config(
    page_title="Conversational AI",
    layout="centered",
    page_icon="🤖"
)

# 🎨 Inject custom CSS for beautiful UI
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #e0eafc, #cfdef3);
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-title {
        font-size: 2.4rem;
        color: #34495e;
        text-align: center;
        padding: 10px;
        margin-bottom: 30px;
        font-weight: 700;
        animation: fadeIn 2s ease-in;
    }
    .chat-bubble-user {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        padding: 14px;
        border-radius: 15px 15px 0 15px;
        margin: 10px 0;
        color: #2c3e50;
        text-align: right;
        font-weight: 500;
    }
    .chat-bubble-bot {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 14px;
        border-radius: 15px 15px 15px 0;
        margin: 10px 0;
        color: #2c3e50;
        text-align: left;
        font-weight: 500;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    <div class='chat-title'>🤖 Conversational AI Assistant</div>
""", unsafe_allow_html=True)

# 🧠 Sidebar info
with st.sidebar:
    st.markdown("### 💡 About")
    st.markdown("AI-powered contact center assistant built with:")
    st.markdown("- Sentence Transformers")
    st.markdown("- FAISS")
    st.markdown("- Streamlit")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat = []

# 🧠 Chat history state
if "chat" not in st.session_state:
    st.session_state.chat = []

# 💬 Chat display
for user_msg, bot_msg in reversed(st.session_state.chat):
    st.markdown(f"<div class='chat-bubble-user'>You: {user_msg}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble-bot'>Bot: {bot_msg}</div>", unsafe_allow_html=True)

# 📥 Chat input
user_input = st.chat_input("Type your question here...")

if user_input:
    bot_response = get_response(user_input)
    st.session_state.chat.append((user_input, bot_response))
