import streamlit as st
from google import genai
from google.genai import types

# 1. Page Config
st.set_page_config(page_title="Vesta AI Concierge", layout="wide")

# 2. Luxury Assets
VESTA_IMG = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRueUGg-BJ-C1N2eIYsabxDRQQv6iSoXS9tiA&s"
USER_ICON = "⚫"

# 3. Setup AI Client using Streamlit Secrets
try:
    # This pulls the key from the 'Advanced Settings' you filled in
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("API Key missing! Go to Streamlit Settings > Secrets and add GEMINI_API_KEY.")
    st.stop()

# Custom CSS for Premium Look
st.markdown(f"""
    <style>
    .main {{ background-color: #fcfcfc; }}
    .stChatMessage {{ border-radius: 10px; margin-bottom: 10px; border: 1px solid #f0f0f0; }}
    .stButton>button {{ background-color: #000; color: white; border-radius: 4px; font-weight: 600; }}
    .stButton>button:hover {{ background-color: #d4af37; color: black; }}
    h1 {{ font-family: serif; font-weight: 400; }}
    </style>
    """, unsafe_allow_html=True)

# 4. Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image(VESTA_IMG, width=100)
with col2:
    st.title("VESTA HOME")
    st.write("### *Elite AI Property Concierge*")

st.divider()

# 5. The Consultation Sidebar
with st.sidebar:
    st.image(VESTA_IMG, use_container_width=True)
    st.markdown("---")
    st.markdown("### 🏛️ Professional Inquiry")
    with st.form("inquiry_form", clear_on_submit=True):
        name = st.text_input("Client Name")
        email = st.text_input("Contact Email")
        msg = st.text_area("Property Details")
        if st.form_submit_button("SEND REQUEST"):
            if name and email:
                st.success(f"Inquiry received for {name}.")
            else:
                st.error("Please provide details.")

# 6. Load Knowledge Base
try:
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        kb_content = f.read()
except:
    kb_content = "Vesta Home: Luxury staging in NYC."

# 7. Chat Interface Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    avatar = VESTA_IMG if msg["role"] == "assistant" else USER_ICON
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("How may I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_ICON):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=VESTA_IMG):
        try:
            # INTEGRATED BRAIN: No 'requests.post' needed anymore!
            config = types.GenerateContentConfig(
                system_instruction=f"You are the Vesta Home Luxury AI. Context: {kb_content}. Tone: Elite NYC."
            )
            response = client.models.generate_content(
            model="gemini-2.0-flash", 
           contents=prompt,
           config=config
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI Error: {str(e)}")

