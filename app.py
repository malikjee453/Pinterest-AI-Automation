
import streamlit as st
import os
from google import genai

st.set_page_config(
    page_title="Pinterest AI Automation",
    page_icon="📌",
    layout="wide",
)

st.title("📌 Pinterest AI Automation")
st.caption("AI-powered product research, creative design and affiliate marketing")

st.info(
    "Welcome! This is the initial dashboard. "
    "We'll connect the AI agents and Pinterest publishing in later steps."
)

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

st.subheader("Gemini AI Connection")

if not api_key:
    st.warning(
        "Gemini API key is not configured yet. "
        "We'll add it securely after deployment."
    )
else:
    if st.button("Test Gemini Connection"):
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents="Reply with: Gemini connection successful."
            )
            st.success("Gemini responded successfully.")
            st.write(response.text)
        except Exception as e:
            st.error(f"Gemini connection failed: {e}")

st.divider()

st.subheader("System Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔎 Product Research")
    st.write("Discover and evaluate eligible affiliate products.")

with col2:
    st.markdown("### 🎨 Creative Agent")
    st.write("Generate and evaluate original Pinterest Pin designs.")

with col3:
    st.markdown("### 📊 Learning Agent")
    st.write("Track performance and improve future recommendations.")

st.caption("Publishing and automated scheduling will be configured in later steps.")
