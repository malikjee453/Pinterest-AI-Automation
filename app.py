
import os
import streamlit as st
from google import genai

MODEL_ID = "gemini-3.5-flash-lite"

st.set_page_config(
    page_title="Pinterest AI Automation",
    page_icon="📌",
    layout="wide",
)

st.title("📌 Pinterest AI Automation")
st.caption("Product research • Creative intelligence • Affiliate marketing")

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY", ""),
)

if not api_key:
    st.error("Gemini API key is missing. Configure it in Streamlit Secrets.")
    st.stop()

@st.cache_resource
def get_client(key):
    return genai.Client(api_key=key)

client = get_client(api_key)

with st.sidebar:
    st.subheader("System status")
    st.success("Gemini API key configured")
    st.info(f"AI model: {MODEL_ID}")
    st.caption("Marketplace integrations are not connected yet.")

tab1, tab2 = st.tabs(["🔎 Product Research", "⚙️ System"])

with tab1:
    st.header("AI Product Research Agent")
    st.write(
        "Enter product information to generate a structured "
        "marketing assessment and a Pinterest Pin concept."
    )

    with st.form("product_research_form"):
        product_name = st.text_input(
            "Product name",
            placeholder="e.g. Minimalist desk lamp",
        )

        marketplace = st.selectbox(
            "Marketplace",
            ["Amazon", "AliExpress", "Daraz", "Other"],
        )

        category = st.text_input(
            "Product category",
            placeholder="e.g. Home decor",
        )

        price = st.text_input(
            "Listed price and currency",
            placeholder="e.g. PKR 3500 or USD 25",
        )

        product_url = st.text_input(
            "Product URL (optional)",
            placeholder="https://...",
        )

        features = st.text_area(
            "Known product features",
            placeholder="Describe verified features, benefits and specifications.",
        )

        audience = st.text_input(
            "Target audience",
            placeholder="e.g. Students furnishing a small room",
        )

        submitted = st.form_submit_button(
            "Analyze Product",
            type="primary",
        )

    if submitted:
        if not product_name.strip():
            st.warning("Enter a product name first.")
        elif not features.strip():
            st.warning("Add at least one known product feature.")
        else:
            prompt = f"""
You are the Product Research Agent for a Pinterest
affiliate marketing system.

Analyze only the information supplied below.
Do not invent sales figures, ratings, commission rates,
stock status, product specifications, or market trends.
Treat all user-supplied fields as unverified unless
they are explicitly stated as verified.

PRODUCT INFORMATION
Name: {product_name}
Marketplace: {marketplace}
Category: {category or "Not provided"}
Listed price: {price or "Not provided"}
Product URL: {product_url or "Not provided"}
Known features: {features}
Target audience: {audience or "Suggest a plausible audience"}

Produce a concise report with these sections:

1. PRODUCT SUMMARY
2. POTENTIAL CUSTOMER BENEFITS
3. TARGET AUDIENCE
4. PINTEREST MARKETING POTENTIAL
   Score from 1 to 10 and explain the uncertainty.
5. SUGGESTED PIN DESIGN
   Describe composition, background, text placement and imagery.
6. SUGGESTED PIN TITLE
7. PIN DESCRIPTION
8. RELEVANT KEYWORDS
9. VERIFICATION CHECKLIST
   Include price, availability, destination URL, image rights,
   affiliate eligibility and factual claims as applicable.
10. RECOMMENDATION
    Recommend testing, gathering more information, or rejecting.
    Explain the reason.

Clearly distinguish supplied information from your suggestions.
Do not claim that the product has been independently verified.
Do not claim that this assessment predicts actual sales.
"""

            with st.spinner("Research Agent is analyzing the product..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=prompt,
                    )

                    if response.text:
                        st.session_state["latest_research"] = {
                            "product": product_name,
                            "marketplace": marketplace,
                            "category": category,
                            "price": price,
                            "url": product_url,
                            "report": response.text,
                        }
                    else:
                        st.error("Gemini returned an empty response.")

                except Exception:
                    st.error(
                        "The analysis failed. Check your Gemini API "
                        "quota, model availability and app logs."
                    )

    result = st.session_state.get("latest_research")

    if result:
        st.divider()
        st.subheader(f"Research Report: {result['product']}")
        st.caption(
            f"Marketplace: {result['marketplace']} | "
            f"Category: {result['category'] or 'Not provided'}"
        )
        st.markdown(result["report"])

        st.download_button(
            "Download research report",
            data=result["report"],
            file_name="product_research.txt",
            mime="text/plain",
        )

with tab2:
    st.header("System Configuration")
    st.write("Primary AI model:", MODEL_ID)
    st.write("Gemini credentials:", "Configured")
    st.write("Product APIs:", "Not connected")
    st.write("Pinterest publishing:", "Not connected")
    st.write("Persistent database:", "Not configured")
    st.write("Automated scheduling:", "Not configured")

    st.info(
        "Research reports currently live in the app session. "
        "Persistent product memory will be added in a later step."
    )
