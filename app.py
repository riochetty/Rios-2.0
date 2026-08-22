import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

st.set_page_config(page_title="RIOS 2.0 // TERMINAL", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #00f0ff; }
    h1 { color: #00f0ff !important; font-family: 'Courier New', monospace; text-shadow: 0 0 10px #00f0ff; }
    .stButton>button {
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 100%);
        color: #ffffff !important; font-weight: bold; border: none; border-radius: 8px; padding: 12px 24px;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ RIOS 2.0 // QUANTUM EXECUTION ENGINE")
st.caption("SYSTEM STATUS: ONLINE | DUAL-ENTRY XAUUSD & INDEX ALGORITHM")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing! Configure GEMINI_API_KEY in secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

col1, col2 = st.columns(2)
with col1:
    htf_file = st.file_uploader("1. HTF CHART (1H / 4H - For Trend/Bias)", type=["png", "jpg", "jpeg"])
with col2:
    ltf_file = st.file_uploader("2. LTF CHART (1m / 15m - For Entry Trigger)", type=["png", "jpg", "jpeg"])

if htf_file and ltf_file:
    img_htf = Image.open(htf_file)
    img_ltf = Image.open(ltf_file)
    
    st.image([img_htf, img_ltf], caption=["HTF Bias Chart", "LTF Entry Chart"], width=350)

    if st.button("RUN DUAL-ENTRY ANALYSIS"):
        with st.spinner("CALCULATING AGGRESSIVE & CONSERVATIVE EXECUTION LEVELS..."):
            
            sys_inst = """
            You are RIOS 2.0, an institutional-grade price action trading engine specializing in Gold (XAUUSD) and Stock Indices.
            
            DUAL-ENTRY EXECUTION LOGIC:
            1. MULTI-TIMEFRAME CONFLUENCE: Read Image 1 (HTF) for market trend/bias. Read Image 2 (LTF) for entry triggers. NEVER trade against Image 1 trend.
            2. SOLVE MISSING TREND EXPANSIONS: Gold frequently leaves deep limit orders behind during strong expansions. You MUST provide TWO distinct entry options:
               - AGGRESSIVE ENTRY: Shallow FVG / Immediate BOS Retest for high-momentum moves.
               - CONSERVATIVE LIMIT: Deep FVG / Demand mitigation zone for deep pullbacks.
            3. RISK PARAMETERS: Stop Loss must be 2.0-3.0 pts (20-30 pips on Gold) behind structural invalidation wicks. Minimum 1:2.5 Risk-to-Reward.
            """

            user_prompt = """
            Analyze both uploaded charts. Output the exact execution format below in Markdown:

            ## ⚡ RIOS 2.0 EXECUTION SIGNAL
            **DIRECTION:** [🔵 BUY / LONG or 🔴 SELL / SHORT]
            **MOMENTUM STATE:** [Strong Momentum Expansion / Ranging / Pullback Phase]

            ---

            ### 🎯 EXECUTION OPTIONS

            #### ⚡ Option A: Aggressive Entry (High Momentum)
            *Use this if price is expanding rapidly and unlikely to pull back deep.*
            * **Entry Level:** [Shallow FVG / Immediate Retest Price]
            * **Stop Loss (SL):** [Exact Price Level]
            * **Take Profit 1 (TP1 - Partial & BE):** [Exact Price Level]
            * **Take Profit 2 (TP2 - Target):** [Exact Price Level]
            * **Calculated R:R:** [Ratio]

            #### 🎯 Option B: Conservative Limit (Deep Pullback)
            *Use this if price shows signs of heavy retracement into discount/premium zones.*
            * **Limit Entry Level:** [Deep FVG / Extreme Order Block Price]
            * **Stop Loss (SL):** [Exact Price Level]
            * **Take Profit 1 (TP1 - Partial & BE):** [Exact Price Level]
            * **Take Profit 2 (TP2 - Target):** [Exact Price Level]
            * **Calculated R:R:** [Ratio]

            ---

            ### 📊 LIQUIDITY & STRUCTURE LOGIC
            * **HTF Structure:** Key liquidity or POI swept/mitigated on Chart 1.
            * **LTF Trigger:** Liquidity Sweep and CHoCH details on Chart 2.
            * **Invalidation Condition:** Price movement that completely invalidates this trade idea.
            """

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[img_htf, img_ltf, user_prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=sys_inst,
                        temperature=0.1
                    )
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Execution Error: {e}")
