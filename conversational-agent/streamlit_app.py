import streamlit as st
from chatbot_logic import get_response

st.set_page_config(page_title="Virtual Support Assistant", layout="centered")

# === Custom CSS: Real-World Premium UI ===
st.markdown("""
    <style>
    body {
        background: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
    }

    .header {
        font-size: 2.8rem;
        font-weight: bold;
        color: #34495e;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease-in-out;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .chat-container {
        max-width: 700px;
        margin: auto;
        padding: 30px;
        background: #ffffffdd;
        border-radius: 18px;
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.1);
    }

    .chat-bubble-user {
        background-color: #007bff;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 0 18px;
        margin: 12px 0;
        text-align: right;
        margin-left: 100px;
        animation: fadeIn 0.3s ease-in;
    }

    .chat-bubble-bot {
        background-color: #ecf0f1;
        color: #2c3e50;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 0;
        margin: 12px 0;
        text-align: left;
        margin-right: 100px;
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }

    .avatar-user {
        float: right;
        margin-left: 10px;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        object-fit: cover;
    }

    .avatar-bot {
        float: left;
        margin-right: 10px;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        object-fit: cover;
    }

    .clearfix::after {
        content: "";
        display: block;
        clear: both;
    }
    </style>

    <div class='header'>🤖 Virtual Support Assistant</div>
    <div class='chat-container'>
""", unsafe_allow_html=True)

# Sidebar (for branding/info)
with st.sidebar:
    st.markdown("### 🌐 About the Assistant")
    st.markdown("Built with:")
    st.markdown("- Sentence Transformers")
    st.markdown("- FAISS for semantic search")
    st.markdown("- Streamlit for UI")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat = []

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = []

# === Display chat bubbles
for user_msg, bot_msg in reversed(st.session_state.chat):
    st.markdown(f"""
    <div class='clearfix'>
        <img src='https://i.imgur.com/HZ5RZkP.png' class='avatar-user'>
        <div class='chat-bubble-user'>You: {user_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='clearfix'>
        <img src='https://i.imgur.com/VX3AVVl.png' class='avatar-bot'>
        <div class='chat-bubble-bot'>Bot: {bot_msg}</div>
    </div>
    """, unsafe_allow_html=True)

# === Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    bot_reply = get_response(user_input)
    st.session_state.chat.append((user_input, bot_reply))

# Close the container
st.markdown("</div>", unsafe_allow_html=True)
