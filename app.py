import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Rios 2.0 Co-Pilot", layout="centered")
st.title("Rios 2.0 Chart Analyzer 📈")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please configure GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

trade_type = st.radio("Select Strategy Mode:", ["15m XAUUSD London Scalp", "1H/4H Swing Trade"])

uploaded_file = st.file_uploader("Upload Chart Screenshot...", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_container_width=True)
    
    if st.button("Analyze Setup"):
        with st.spinner("Analyzing market structure against Rios 2.0 rules..."):
            prompt = f"""
            You are the Rios 2.0 technical co-pilot. Analyze this chart image for a {trade_type}.
            
            Evaluate against these rules:
            1. Market Structure & Trend (Higher Highs / Lower Lows).
            2. Liquidity Sweep or Change of Character (CHoCH / BOS).
            3. Risk Parameters: Invalidation level (Stop Loss) and minimum 1:2 Risk-to-Reward setup.
            
            Always start your response with EXACTLY ONE of these dot signals on line 1:
            - 🔵 Blue Dot: Valid, rules-compliant setup ready for execution.
            - 🟡 Yellow Dot: Caution. Potential setup but missing confirmation/waiting for pull-back.
            - 🔴 Red Dot: Invalid setup or high risk. Do not enter.
            
            Follow with 3 concise bullet points breaking down why.
            """
            
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[image, prompt]
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error during analysis: {e}")
