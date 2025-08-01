import streamlit as st
from chatbot_logic import get_response

st.set_page_config(page_title="AI Chat Assistant", layout="wide", page_icon="🤖")

# 🎨 Custom Animated Background + Glowing UI
st.markdown("""
    <style>
    body {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Segoe UI', sans-serif;
        color: #ffffff;
    }

    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .chat-title {
        font-size: 3rem;
        color: #ffffff;
        text-align: center;
        text-shadow: 0 0 15px #00000066;
        animation: glowText 2s ease-in-out infinite alternate;
        margin-bottom: 2rem;
    }

    @keyframes glowText {
        from {
            text-shadow: 0 0 10px #00f5ff, 0 0 20px #00f5ff;
        }
        to {
            text-shadow: 0 0 20px #00e0ff, 0 0 40px #00e0ff;
        }
    }

    .chat-bubble-user {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(14px);
        padding: 14px;
        border-radius: 15px 15px 0 15px;
        margin: 10px 0;
        color: #ffffff;
        text-align: right;
        border: 1px solid #ffffff44;
    }

    .chat-bubble-bot {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        padding: 14px;
        border-radius: 15px 15px 15px 0;
        margin: 10px 0;
        color: #ffffff;
        text-align: left;
        border: 1px solid #ffffff33;
    }

    ::placeholder {
        color: #ffffffaa;
    }
    </style>

    <div class='chat-title'>💬 AI Conversational Assistant</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧠 About This App")
    st.markdown("A modern AI-powered contact center chatbot built using:")
    st.markdown("- Sentence Transformers")
    st.markdown("- FAISS")
    st.markdown("- Streamlit")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat = []

# Session storage for chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Show chat history
for user_input, bot_reply in reversed(st.session_state.chat):
    st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 You: {user_input}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble-bot'>🤖 Bot: {bot_reply}</div>", unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    bot_reply = get_response(user_input)
    st.session_state.chat.append((user_input, bot_reply))
