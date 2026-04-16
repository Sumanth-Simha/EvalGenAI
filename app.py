import streamlit as st
from agent.router import route
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="EvalGenAI",
    page_icon="🔥",
    layout="wide"
)

# =========================
# 🎨 CUSTOM CSS
# =========================

st.markdown("""
<style>
body { background-color: #0f172a; }
.block-container { padding-top: 2rem; max-width: 900px; }

[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 12px;
    font-size: 15px;
}

[data-testid="stChatMessage"][data-testid="user"] {
    background-color: #1e293b;
}

[data-testid="stChatMessage"][data-testid="assistant"] {
    background-color: #020617;
}

textarea {
    background-color: #020617 !important;
    color: white !important;
}

[data-testid="stSidebar"] {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("🔥 EvalGenAI")
st.caption("Agent-Based Academic Intelligence System")

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.title("⚙️ Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 💡 Try:")
    st.write("• Explain IoT framework")
    st.write("• Explain OSI model with diagram")
    st.write("• Predict important questions")

# =========================
# SESSION MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# IMAGE HELPER 🔥
# =========================

def get_correct_image_path(img_path):
    if os.path.exists(img_path):
        return img_path

    filename = os.path.basename(img_path)

    possible_paths = [
        os.path.join("data", "iot", "mod1", "diagrams", filename),
        os.path.join("data", "iot", "mod1", "diagrams", "images", filename),
    ]

    for p in possible_paths:
        if os.path.exists(p):
            return p

    return None

# =========================
# DISPLAY CHAT
# =========================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg.get("diagrams"):
            st.subheader("🖼️ Diagrams")
            for d in msg["diagrams"]:
                path = get_correct_image_path(d.get("image_path", ""))

                if path:
                    st.image(path, caption=d.get("title", d.get("topic", "")), use_container_width=True)
                else:
                    st.warning(f"Image not found: {d.get('image_path')}")

# =========================
# INPUT BOX
# =========================

prompt = st.chat_input("Ask anything about IoT...")

# =========================
# PROCESS INPUT
# =========================

if prompt:
    # user msg
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # assistant
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = route(prompt)

            if isinstance(result, dict):
                answer = result.get("answer", "")
                diagrams = result.get("diagrams", [])
            else:
                answer = result
                diagrams = []

            st.markdown(answer)

            if diagrams:
                st.subheader("🖼️ Diagrams")
                for d in diagrams:
                    path = get_correct_image_path(d.get("image_path", ""))

                    if path:
                        st.image(path, caption=d.get("title", d.get("topic", "")), use_container_width=True)
                    else:
                        st.warning(f"Image not found: {d.get('image_path')}")

    # save chat
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "diagrams": diagrams
    })