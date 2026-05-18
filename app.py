import streamlit as st
from groq import Groq

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AZHAR AI CHATBOT ULTRA VIP",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# ULTRA VIP CSS
# ==============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
}

.main-box {
    text-align:center;
    padding:20px;
    border-radius:20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    box-shadow: 0 0 40px rgba(139,92,246,0.4);
    margin-bottom:20px;
}

.title {
    font-size:48px;
    font-weight:900;
    background: linear-gradient(90deg,#00f5ff,#8b5cf6,#ec4899);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle {
    color:#94a3b8;
    font-size:14px;
}

.stChatInput {
    position: fixed;
    bottom: 20px;
}

.stButton>button {
    background: linear-gradient(90deg,#8b5cf6,#ec4899);
    color:white;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# VIP LOGO HEADER
# ==============================
st.markdown("""
<div class="main-box">
    <div class="title">🤖 AZHAR AI CHATBOT</div>
    <div class="subtitle">ULTRA VIP Multi-Persona Intelligence System</div>
</div>
""", unsafe_allow_html=True)

# ==============================
# API KEY
# ==============================
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Enter Groq API Key", type="password")

client = Groq(api_key=api_key) if api_key else None

# ==============================
# PERSONAS
# ==============================
PERSONAS = {
    "🧠 Strategic Advisor": "You are a world-class Strategic Advisor...",
    "📘 Expert Teacher": "You are a friendly expert teacher...",
    "💼 Corporate Coach": "You are a high-level corporate coach..."
}

# ==============================
# SESSION MEMORY
# ==============================
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {p: [] for p in PERSONAS}

# ==============================
# SIDEBAR
# ==============================
st.sidebar.markdown("## 🤖 AZHAR AI CHATBOT ULTRA VIP")
selected_persona = st.sidebar.selectbox("🎭 Select Persona", list(PERSONAS.keys()))

if st.sidebar.button("🗑 Clear Memory"):
    st.session_state.chat_histories[selected_persona] = []
    st.sidebar.success("Memory Cleared!")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("⚙ Model: **llama-3.3-70b-versatile**")

model_name = "llama-3.3-70b-versatile"

# ==============================
# CHAT DISPLAY
# ==============================
history = st.session_state.chat_histories[selected_persona]

for msg in history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# CHAT INPUT
# ==============================
if prompt := st.chat_input(f"Talk to {selected_persona}..."):

    if not client:
        st.error("⚠ Please enter API key")
        st.stop()

    # USER MESSAGE
    with st.chat_message("user"):
        st.markdown(prompt)

    history.append({"role": "user", "content": prompt})

    # SYSTEM + HISTORY
    messages = [{"role": "system", "content": PERSONAS[selected_persona]}]
    messages += history[-10:]

    try:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""

            stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=4096,
                stream=True
            )

            for chunk in stream:
                text = chunk.choices[0].delta.content
                if text:
                    full += text
                    placeholder.markdown(full + "▌")

            placeholder.markdown(full)

        history.append({"role": "assistant", "content": full})

    except Exception as e:
        st.error(f"🚨 API Error: {str(e)}")