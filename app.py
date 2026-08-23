import streamlit as st
import yfinance as yf
import time
from google import genai
from google.genai import types
from PIL import Image

# 1. Page Config
st.set_page_config(
    page_title="RIOS 2.0 // QUANTUM TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Sleek Glassmorphism CSS Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'JetBrains Mono', monospace;
        background-color: #080B11 !important;
        color: #E2E8F0;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #10192D 0%, #080B11 75%);
    }

    /* Header Glow */
    .title-text {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00F0FF, #7000FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(0, 240, 255, 0.3);
        margin-bottom: 0px;
    }
    
    .sub-text {
        font-size: 0.85rem;
        color: #64748B;
        letter-spacing: 2px;
        margin-bottom: 25px;
    }

    /* Glassmorphic Metric Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .price-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00F0FF;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }

    /* Custom Streamlit Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00F0FF 0%, #7000FF 100%);
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 10px;
        padding: 16px 24px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        transition: all 0.3s ease-in-out;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 35px rgba(112, 0, 255, 0.8);
        transform: translateY(-2px);
    }

    /* File Uploader Custom Styling */
    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.4);
        border: 1px dashed rgba(0, 240, 255, 0.3);
        border-radius: 12px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header & Branding
st.markdown("<div class='title-text'>⚡ RIOS 2.0 // QUANTUM EXECUTION TERMINAL</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>INSTITUTIONAL ICT ORDER FLOW ENGINE • MULTI-ASSET PRECISION SYSTEM</div>", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("SYSTEM CRITICAL: GEMINI_API_KEY is missing from Streamlit Secrets!")
    st.stop()

client = genai.Client(api_key=api_key)

ASSET_MAP = {
    "🥇 XAUUSD (Gold)": "GC=F",
    "📊 US30 (Dow Jones)": "^DJI",
    "💻 NAS100 (Nasdaq)": "^IXIC"
}

# 4. Top Control Bar
col_asset, col_sess, col_live = st.columns([2, 2, 2])

with col_asset:
    asset_choice = st.selectbox("SELECT TARGET ASSET:", list(ASSET_MAP.keys()))

with col_sess:
    session_choice = st.selectbox(
        "SESSION / KILLZONE:",
        ["⚡ London Open Killzone", "🔥 New York Open (AM Session)", "🌆 New York PM / Asian Session"]
    )

ticker_symbol = ASSET_MAP[asset_choice]

def get_live_price(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d", interval="1m")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
    except:
        return None
    return None

live_price = get_live_price(ticker_symbol)

with col_live:
    price_display = f"{live_price}" if live_price else "SYNCING..."
    st.markdown(
        f"""
        <div class='glass-card'>
            <div style='font-size: 0.75rem; color: #94A3B8;'>LIVE TICKER FEED</div>
            <div class='price-value'>{price_display}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# 5. Dual Chart Upload Section
col1, col2 = st.columns(2)
with col1:
    htf_file = st.file_uploader("1. HTF BIAS CHART (1H / 4H Structure)", type=["png", "jpg", "jpeg"])
with col2:
    ltf_file = st.file_uploader("2. LTF TRIGGER CHART (1m / 15m Execution)", type=["png", "jpg", "jpeg"])

if htf_file and ltf_file:
    img_htf = Image.open(htf_file)
    img_ltf = Image.open(ltf_file)
    
    st.image([img_htf, img_ltf], caption=["Higher Timeframe Bias", "Lower Timeframe Execution Trigger"], use_container_width=True)

    if st.button("RUN QUANTUM PRECISION ANALYSIS"):
        with st.spinner("CALCULATING OPTIMAL TRADE ENTRIES (OTE) & LIQUIDITY POOLS..."):
            
            sys_inst = f"""
            You are RIOS 2.0, the world's most precise institutional trading execution engine. You specialize in ICT concepts (Buyside/Sellside Liquidity Sweeps, Change of Character, Break of Structure, Fair Value Gaps, and Order Blocks) for {asset_choice}.

            REAL-TIME MARKET CONTEXT:
            - Asset: {asset_choice}
            - Session Context: {session_choice}
            - Live Market Reference Price: {live_price if live_price else 'Refer to chart scale'}

            STRICT EXECUTION PROTOCOL:
            1. MULTI-TIMEFRAME ALIGNMENT:
               - Read Chart 1 (HTF) for core narrative, dominant trend, and unmitigated Supply/Demand POIs.
               - Read Chart 2 (LTF) for recent Liquidity Sweeps (BSL/SSL), CHoCH, and entry triggers.
               - NEVER generate a signal that contradicts the HTF Chart 1 trend.

            2. ASSET SPECIFIC SPREAD & BUFFER RULES:
               - Gold (XAUUSD): 2.0 - 3.0 point (20-30 pip) buffer beyond invalidation wicks.
               - US30: 25 - 40 point buffer to account for index volatility.
               - NAS100: 15 - 25 point buffer.

            3. DUAL-ENTRY ARCHITECTURE:
               - OPTION A (Aggressive Retest): Targets nearest 5M/15M FVG or immediate BOS retest for high-momentum moves.
               - OPTION B (Conservative OTE Limit): Targets deep discount/premium liquidity sweeps or extreme Order Blocks (0.618 - 0.79 Fibonacci OTE levels) for high R:R setups.

            4. MANDATORY RISK METRICS: Minimum 1:3 Risk-to-Reward ratio. Always provide explicit numerical values for Entry, Stop Loss, TP1 (Partial & Breakeven), and TP2 (Final Target).
            """

            user_prompt = f"""
            Analyze both uploaded charts. Format the output in clean Markdown using this structure:

            ## ⚡ RIOS 2.0 PRECISION SIGNAL // [{asset_choice}]
            **DIRECTION:** [🔵 BUY / LONG or 🔴 SELL / SHORT]
            **LIVE REFERENCE PRICE:** {live_price if live_price else 'N/A'}
            **MARKET STRUCTURE STATE:** [Bullish Expansion / Bearish Expansion / Liquidity Sweep Phase]

            ---

            ### 🎯 EXECUTION OPTIONS

            #### ⚡ Option A: Aggressive Entry (High Momentum)
            *Use when price is expanding rapidly and unlikely to offer deep pullbacks.*
            * **Entry Zone:** [Price Level / Narrow Range]
            * **Stop Loss (SL):** [Exact Price Level + Asset Buffer]
            * **Take Profit 1 (TP1 - Partial & BE):** [Exact Price Level]
            * **Take Profit 2 (TP2 - Target):** [Exact Price Level]
            * **Calculated R:R:** [e.g., 1:3.2]

            #### 🎯 Option B: Conservative OTE Limit (Deep Pullback)
            *Use when waiting for a full liquidity sweep into discount/premium Order Blocks.*
            * **Limit Entry Zone:** [Exact Price Level]
            * **Stop Loss (SL):** [Exact Price Level + Asset Buffer]
            * **Take Profit 1 (TP1 - Partial & BE):** [Exact Price Level]
            * **Take Profit 2 (TP2 - Target):** [Exact Price Level]
            * **Calculated R:R:** [e.g., 1:4.5]

            ---

            ### 📊 INSTITUTIONAL ORDER FLOW BREAKDOWN
            * **HTF Narrative (Chart 1):** Primary POI mitigated, dominant trend direction, and main target.
            * **LTF Trigger (Chart 2):** Exact Liquidity Sweep details (BSL/SSL taken) and CHoCH confirmation.
            * **Structural Invalidation:** The exact price level where this setup becomes invalid.
            """

            max_retries = 3
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
                    break
                except Exception as e:
                    if "503" in str(e) and attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        st.error(f"Execution Error: {e}")
                        break
