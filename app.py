import streamlit as st
from google import genai
from PIL import Image

# Futuristic Page Config
st.set_page_config(page_title="RIOS 2.0 // TERMINAL", layout="wide", initial_sidebar_state="expanded")

# Custom Neon/Futuristic CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #00f0ff;
    }
    h1 {
        color: #00f0ff !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px #00f0ff, 0 0 20px #00f0ff;
        letter-spacing: 2px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 100%);
        color: #ffffff !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(112, 0, 255, 0.8);
        transform: scale(1.02);
    }
    .stRadio label {
        color: #00f0ff !important;
        font-family: 'Courier New', monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Header & Branding
st.title("⚡ RIOS 2.0 // CO-PILOT TERMINAL")
st.caption("SYSTEM STATUS: ONLINE | QUANTUM PRICE ACTION ENGINE")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("SYSTEM ERROR: API Key missing! Configure GEMINI_API_KEY in secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Strategy & Timeframe Selector
tf_choice = st.radio(
    "SELECT EXECUTION TIMEFRAME:",
    [
        "⚡ 1m / 5m Hyper-Scalp Mode",
        "🎯 15m Scalp & Intraday Mode",
        "🌊 1H / 4H Swing Mode"
    ]
)

uploaded_file = st.file_uploader("UPLOAD CHART SCREENSHOT [PNG/JPG]", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="// ACTIVE CHART STREAM", use_container_width=True)

    if st.button("RUN QUANTUM ANALYSIS"):
        with st.spinner("PROCESSING LIQUIDITY SWEEPS & STRUCTURE..."):
            prompt = f"""
            You are RIOS 2.0, a top-tier institutional price action execution tool.

            Timeframe Mode Selected: {tf_choice}

            Instructions:
            1. You MUST generate an actionable trade setup immediately. Do NOT recommend waiting or give neutral calls.
            2. Scan for Liquidity Sweeps, Change of Character (CHoCH), and Break of Structure (BOS).
            3. Always calculate specific numeric price values directly from the chart axes for Entry, Stop Loss (SL), and Take Profit (TP).

            Output format must be exact and strictly formatted in Markdown like this:

            ## ⚡ RIOS 2.0 EXECUTION SIGNAL
            **DIRECTION:** [🔵 BUY / LONG or 🔴 SELL / SHORT]
            **TIMEFRAME:** {tf_choice}

            ---

            ### 🎯 TRADE PARAMETERS
            * **Entry Zone:** [Specific Price / Zone]
            * **Stop Loss (SL):** [Specific Price Level]
            * **Take Profit (TP):** [Specific Price Level]
            * **Risk-to-Reward Ratio:** [Minimum 1:2 R:R]

            ---

            ### 📊 PRICE ACTION LOGIC
            * **Liquidity & Sweeps:** Brief breakdown of recent sweeps or liquidity pools targeted.
            * **Structure:** Status of CHoCH / BOS.
            * **Execution Reason:** Why this precise setup holds high probability right now.
            """

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[image, prompt]
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Execution Error: {e}")
