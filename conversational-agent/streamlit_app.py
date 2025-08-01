import streamlit as st
from chatbot_logic import get_response

st.set_page_config(page_title="Sunset Chatbot 🌇", layout="centered")

# === Inject Aurora Gradient + Advanced UI ===
st.markdown("""
    <style>
    html, body {
        background: linear-gradient(145deg, #ffecd2, #fcb69f);
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        padding: 0;
    }

    .chat-title {
        font-size: 2.7rem;
        text-align: center;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 25px;
        text-shadow: 0 2px 10px #ffffff88;
        animation: slideIn 1.3s ease-out;
    }

    .chat-box {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 25px;
        max-width: 750px;
        margin: auto;
        box-shadow: 0 12px 25px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }

    .chat-bubble-user {
        background-color: #ff6f61;
        color: #fff;
        padding: 14px 20px;
        border-radius: 20px 20px 0 20px;
        margin: 12px 0;
        text-align: right;
        max-width: 75%;
        margin-left: auto;
        font-weight: 500;
        animation: fadeIn 0.3s ease;
    }

    .chat-bubble-bot {
        background-color: #ffffffcc;
        color: #2c3e50;
        padding: 14px 20px;
        border-radius: 20px 20px 20px 0;
        margin: 12px 0;
        text-align: left;
        max-width: 75%;
        margin-right: auto;
        font-weight: 500;
        animation: fadeIn 0.3s ease;
    }

    .avatar-user, .avatar-bot {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 10px;
    }

    .clearfix::after {
        content: "";
        display: block;
        clear: both;
    }

    @keyframes slideIn {
        from { transform: translateY(-30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    </style>

    <div class='chat-title'>🌇 Sunset Support Chatbot</div>
    <div class='chat-box'>
""", unsafe_allow_html=True)

# === Sidebar (optional)
with st.sidebar:
    st.markdown("### 💡 About")
    st.markdown("This assistant uses:")
    st.markdown("- 🌐 FAISS vector search")
    st.markdown("- 🤖 Sentence Transformers")
    st.markdown("- ⚡ Streamlit for UI")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat = []

# === Chat Session
if "chat" not in st.session_state:
    st.session_state.chat = []

# === Render Chat History
for user_msg, bot_msg in reversed(st.session_state.chat):
    st.markdown(f"""
    <div class='clearfix'>
        <div style="display: flex; justify-content: flex-end; align-items: center;">
            <div class='chat-bubble-user'>You: {user_msg}</div>
            <img class='avatar-user' src='https://i.imgur.com/HZ5RZkP.png'>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='clearfix'>
        <div style="display: flex; justify-content: flex-start; align-items: center;">
            <img class='avatar-bot' src='https://i.imgur.com/VX3AVVl.png'>
            <div class='chat-bubble-bot'>Bot: {bot_msg}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# === Input
user_input = st.chat_input("Ask me anything...")

if user_input:
    bot_reply = get_response(user_input)
    st.session_state.chat.append((user_input, bot_reply))

# === Close box div
st.markdown("</div>", unsafe_allow_html=True)
