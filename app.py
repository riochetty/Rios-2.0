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
st.caption("SYSTEM STATUS: ONLINE | MECHANICAL ICT & PRICE ACTION ENGINE")

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

    if st.button("CALCULATE HIGH-PROBABILITY EXECUTION"):
        with st.spinner("ANALYZING CONFLUENCE & CALCULATING LIMIT ORDERS..."):
            
            sys_inst = """
            You are RIOS 2.0, an institutional-grade price action trading engine.
            
            CORE PROFITABILITY RULES:
            1. MULTI-TIMEFRAME CONFLUENCE: Read Image 1 (HTF) for market direction/trend and major Order Blocks. Read Image 2 (LTF) for Liquidity Sweeps, CHoCH, and entry triggers. NEVER trade against Image 1 trend.
            2. ENTRY MANDATE: Only generate LIMIT ORDER setups placed directly at Fair Value Gaps (FVG) or extreme Liquidity Sweep points.
            3. RISK PARAMETERS: Stop Loss must be 2-3 pips outside key swing wicks to clear market spread. Require minimum 1:3 Risk-to-Reward (R:R).
            4. TP DYNAMICS: 
               - TP1 (1:1.5 R:R): Take 50% partial profits and move SL to Breakeven.
               - TP2 (1:3+ R:R): Targeted at major external liquidity pools (Equal Highs/Lows).
            """

            user_prompt = """
            Analyze both uploaded charts. Output the exact execution format below in Markdown:

            ## ⚡ RIOS 2.0 EXECUTION SIGNAL
            **DIRECTION:** [🔵 BUY LIMIT / LONG or 🔴 SELL LIMIT / SHORT]
            **HTF BIAS:** [Bullish / Bearish based on Chart 1]

            ---

            ### 🎯 MECHANICAL TRADE PARAMETERS
            * **Limit Entry Zone:** [Exact Price / Range from Chart 2]
            * **Stop Loss (SL):** [Exact Price Level + Buffer]
            * **Take Profit 1 (TP1 - 50% Partial & BE):** [Exact Price Level]
            * **Take Profit 2 (TP2 - Full Target):** [Exact Price Level]
            * **Calculated R:R Ratio:** [e.g., 1:3.4]

            ---

            ### 📊 LIQUIDITY & STRUCTURE BREAKDOWN
            * **HTF Structure:** Key liquidity or POI swept/mitigated on Chart 1.
            * **LTF Trigger:** Liquidity Sweep and CHoCH details on Chart 2.
            * **Invalidation Condition:** Price movement that completely invalidates this structure.
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
