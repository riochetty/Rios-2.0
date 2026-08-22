import streamlit as st
import time
from google import genai
from google.genai import types
from PIL import Image

st.set_page_config(page_title="RIOS 2.0 // INSTITUTIONAL TERMINAL", layout="wide")

# Neon Cyberpunk Styling
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #00f0ff; }
    h1 { color: #00f0ff !important; font-family: 'Courier New', monospace; text-shadow: 0 0 12px #00f0ff; }
    .stButton>button {
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 100%);
        color: #ffffff !important; font-weight: bold; border: none; border-radius: 8px; padding: 14px 28px;
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(112, 0, 255, 0.8);
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ RIOS 2.0 // QUANTUM TERMINAL")
st.caption("SYSTEM STATUS: ACTIVE | XAUUSD • US30 • NAS100 INSTITUTIONAL ENGINE")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("SYSTEM ERROR: GEMINI_API_KEY missing from Streamlit Secrets!")
    st.stop()

client = genai.Client(api_key=api_key)

# Top Bar Selection
col_asset, col_session = st.columns(2)

with col_asset:
    asset_choice = st.selectbox(
        "SELECT TRADING ASSET:",
        ["🥇 XAUUSD (Gold)", "📊 US30 (Dow Jones)", "💻 NAS100 (Nasdaq)"]
    )

with col_session:
    session_choice = st.selectbox(
        "SELECT CURRENT TRADING SESSION / KILLZONE:",
        ["⚡ London Open Killzone", "🔥 New York Open (AM Session)", "🌆 New York PM / Asian Session"]
    )

col1, col2 = st.columns(2)
with col1:
    htf_file = st.file_uploader("1. HTF CHART (1H / 4H - Structural Bias)", type=["png", "jpg", "jpeg"])
with col2:
    ltf_file = st.file_uploader("2. LTF CHART (1m / 15m - Trigger & Sweeps)", type=["png", "jpg", "jpeg"])

if htf_file and ltf_file:
    img_htf = Image.open(htf_file)
    img_ltf = Image.open(ltf_file)
    
    st.image([img_htf, img_ltf], caption=["HTF Structural Bias", "LTF Execution Trigger"], width=350)

    if st.button("RUN QUANTUM SIGNAL ENGINE"):
        with st.spinner("ANALYZING ICT LIQUIDITY, ORDER BLOCKS & SPREAD BUFFERS..."):
            
            sys_inst = f"""
            You are RIOS 2.0, an elite institutional price action algorithm designed for {asset_choice}.

            ASSET SPECIFIC BUFFER RULES:
            - If XAUUSD: Apply 2.0-3.0 point (20-30 pip) SL buffers outside key wicks.
            - If US30: Apply 25-40 point SL buffers to handle high volatility spread expansion.
            - If NAS100: Apply 15-25 point SL buffers to survive market maker wick sweeps.

            CORE EXECUTION MANDATES:
            1. MULTI-TIMEFRAME CONFLUENCE: Read Chart 1 (HTF) for overarching order flow and major Liquidity Pools/Order Blocks. Read Chart 2 (LTF) for Liquidity Sweeps, CHoCH, and entry triggers. NEVER trade against Chart 1 trend.
            2. SESSION CONTEXT: Current context is {session_choice}. Adjust aggressiveness accordingly.
            3. DUAL-ENTRY PARAMETERS:
               - OPTION A (Aggressive): Shallow FVG or Immediate Retest zone to capture explosive expansions.
               - OPTION B (Conservative Limit): Deep Liquidity Sweep / Extreme Discount Demand or Premium Supply zone for maximum Risk-to-Reward.
            4. MINIMUM RISK-TO-REWARD: Strictly calculate setups with a minimum of 1:2.5 R:R to 1:4+ R:R.
            """

            user_prompt = f"""
            Analyze both uploaded charts for {asset_choice} during {session_choice}. 
            Format the response strictly in Markdown as shown below:

            ## ⚡ RIOS 2.0 EXECUTION SIGNAL // [{asset_choice}]
            **DIRECTION:** [🔵 BUY / LONG or 🔴 SELL / SHORT]
            **SESSION VOLATILITY:** [High Volatility / Moderate / Ranging]

            ---

            ### 🎯 EXECUTION OPTIONS

            #### ⚡ Option A: Aggressive Entry (High Momentum)
            *Best for aggressive momentum expansions to prevent missing the trade.*
            * **Entry Zone:** [Price / Narrow Range]
            * **Stop Loss (SL):** [Exact Price Level + Asset Buffer]
            * **Take Profit 1 (TP1 - Partial & BE):** [Exact Price Level]
            * **Take Profit 2 (TP2 - Target):** [Exact Price Level]
            * **Calculated R:R:** [e.g., 1:2.8]

            #### 🎯 Option B: Conservative Limit (Deep Pullback)
            *Best for deep discount/premium retracements into key POIs.*
            * **Limit Entry Zone:** [Exact Price Level]
            * **Stop Loss (SL):** [Exact Price Level + Asset Buffer]
            * **Take Profit 1 (TP1 - Partial & BE):** [Exact Price Level]
            * **Take Profit 2 (TP2 - Target):** [Exact Price Level]
            * **Calculated R:R:** [e.g., 1:3.8]

            ---

            ### 📊 LIQUIDITY & STRUCTURE BREAKDOWN
            * **HTF Liquidity / POI:** Sweeps or mitigation levels identified on Chart 1.
            * **LTF Trigger:** CHoCH/BOS details and swept liquidity pools on Chart 2.
            * **Invalidation Condition:** Exact price movement that invalidates this setup.
            """

            # Auto-Retry Loop for 503 Server Demand Spikes
            max_retries = 3
            success = False
            
            for attempt in range(max_retries):
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
                    success = True
                    break
                except Exception as e:
                    if "503" in str(e) and attempt < max_retries - 1:
                        time.sleep(2)  # Wait 2 seconds before retrying
                        continue
                    else:
                        st.error(f"Execution Error: {e}")
                        break
