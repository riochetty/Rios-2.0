import streamlit as st
import time
import sqlite3
import pandas as pd
from google import genai
from google.genai import types
from PIL import Image

# 1. Page Config
st.set_page_config(
    page_title="RIOS 2.0 // QUANTUM TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optional yfinance import with fallback
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

# 2. Database Setup (SQLite for Trade Logging)
def init_db():
    conn = sqlite3.connect("trade_history.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            asset TEXT,
            direction TEXT,
            entry_price TEXT,
            sl TEXT,
            tp TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def log_trade(asset, direction, entry, sl, tp):
    conn = sqlite3.connect("trade_history.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO trades (asset, direction, entry_price, sl, tp, status)
        VALUES (?, ?, ?, ?, ?, 'PENDING')
    ''', (asset, direction, entry, sl, tp))
    conn.commit()
    conn.close()

def update_trade_status(trade_id, status):
    conn = sqlite3.connect("trade_history.db")
    c = conn.cursor()
    c.execute('UPDATE trades SET status = ? WHERE id = ?', (status, trade_id))
    conn.commit()
    conn.close()

def get_trades_df():
    conn = sqlite3.connect("trade_history.db")
    df = pd.read_sql_query('SELECT * FROM trades ORDER BY id DESC', conn)
    conn.close()
    return df

# Initialize Session State for Auto-Fill
if 'log_asset' not in st.session_state:
    st.session_state.log_asset = "XAUUSD"
if 'log_dir' not in st.session_state:
    st.session_state.log_dir = "BUY"
if 'log_entry' not in st.session_state:
    st.session_state.log_entry = ""
if 'log_sl' not in st.session_state:
    st.session_state.log_sl = ""
if 'log_tp' not in st.session_state:
    st.session_state.log_tp = ""

# 3. CSS Styling
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

    .title-text {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00F0FF, #7000FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(0, 240, 255, 0.3);
        margin-bottom: 0px;
    }
    
    .sub-text {
        font-size: 0.8rem;
        color: #64748B;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }

    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .price-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #00F0FF;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00F0FF 0%, #7000FF 100%);
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 10px;
        padding: 14px 20px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        transition: all 0.3s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Header & Win-Rate Sidebar
st.markdown("<div class='title-text'>⚡ RIOS 2.0 // QUANTUM TERMINAL</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>INSTITUTIONAL ICT EXECUTION ENGINE • AUTOMATED WIN-RATE JOURNAL</div>", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("SYSTEM CRITICAL: GEMINI_API_KEY missing from Streamlit Secrets!")
    st.stop()

client = genai.Client(api_key=api_key)

with st.sidebar:
    st.markdown("### 📊 WIN-RATE DASHBOARD")
    df_trades = get_trades_df()
    
    total_trades = len(df_trades)
    wins = len(df_trades[df_trades['status'] == 'WIN'])
    losses = len(df_trades[df_trades['status'] == 'LOSS'])
    completed = wins + losses
    win_rate = round((wins / completed * 100), 1) if completed > 0 else 0.0

    st.metric("TOTAL TRADES", total_trades)
    st.metric("WIN RATE", f"{win_rate}%")
    st.write(f"🟢 **Wins:** {wins} | 🔴 **Losses:** {losses}")
    st.divider()

    st.markdown("### 📝 PENDING TRADES")
    pending_trades = df_trades[df_trades['status'] == 'PENDING']
    
    if not pending_trades.empty:
        for idx, row in pending_trades.iterrows():
            st.write(f"**#{row['id']} {row['asset']}** ({row['direction']})")
            st.caption(f"Entry: {row['entry_price']} | SL: {row['sl']} | TP: {row['tp']}")
            col_w, col_l = st.columns(2)
            if col_w.button(f"✅ WIN", key=f"w_{row['id']}"):
                update_trade_status(row['id'], 'WIN')
                st.rerun()
            if col_l.button(f"❌ LOSS", key=f"l_{row['id']}"):
                update_trade_status(row['id'], 'LOSS')
                st.rerun()
            st.divider()
    else:
        st.info("No active trades pending outcome.")

# 5. Control Bar & Live Price Sync
ASSET_MAP = {
    "🥇 XAUUSD (Gold)": "GC=F",
    "📊 US30 (Dow Jones)": "^DJI",
    "💻 NAS100 (Nasdaq)": "^IXIC"
}

col_asset, col_sess, col_price_input = st.columns([2, 2, 2])

with col_asset:
    asset_choice = st.selectbox("TARGET ASSET:", list(ASSET_MAP.keys()))

with col_sess:
    session_choice = st.selectbox(
        "SESSION / KILLZONE:",
        ["⚡ London Open Killzone", "🔥 New York Open (AM Session)", "🌆 New York PM / Asian Session"]
    )

ticker_symbol = ASSET_MAP[asset_choice]

def fetch_live_price(symbol):
    if YFINANCE_AVAILABLE:
        try:
            data = yf.Ticker(symbol).history(period="1d", interval="1m")
            if not data.empty:
                return round(data['Close'].iloc[-1], 2)
        except:
            return None
    return None

auto_price = fetch_live_price(ticker_symbol)

with col_price_input:
    if auto_price:
        st.markdown(
            f"""
            <div class='glass-card'>
                <div style='font-size: 0.75rem; color: #94A3B8;'>AUTO LIVE PRICE</div>
                <div class='price-value'>{auto_price}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        live_price_str = str(auto_price)
    else:
        manual_price = st.text_input("CURRENT LIVE PRICE (Optional):", value="", placeholder="e.g., 2650.50")
        live_price_str = manual_price if manual_price else "Refer to chart scale"

st.markdown("<br>", unsafe_allow_html=True)

# 6. Chart Uploads & Signal Generation
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
        with st.spinner("CALCULATING ICT CONFLUENCE & EXECUTING SIGNAL..."):
            
            sys_inst = f"""
            You are RIOS 2.0, an institutional ICT engine for {asset_choice}.
            Session: {session_choice}. Price Ref: {live_price_str}.
            Provide clear levels for Direction, Entry, Stop Loss, and Take Profit.
            """

            user_prompt = f"""
            Analyze both charts and format output strictly as Markdown:

            ## ⚡ RIOS 2.0 SIGNAL // [{asset_choice}]
            **DIRECTION:** [BUY / LONG or SELL / SHORT]
            **CONFLUENCE SCORE:** [e.g., 9.5/10]

            ---

            ### 🎯 EXECUTION PARAMETERS
            * **Entry Zone:** [Price Level]
            * **Stop Loss (SL):** [Price Level]
            * **Take Profit 1 (TP1):** [Price Level]
            * **Take Profit 2 (Target TP):** [Price Level]
            * **Calculated R:R:** [e.g., 1:3.5]
            """

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[img_htf, img_ltf, user_prompt],
                    config=types.GenerateContentConfig(system_instruction=sys_inst, temperature=0.1)
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Execution Error: {e}")

# 7. Trade Logger Form
st.divider()
st.markdown("### 📥 JOURNAL LOG ENTRY")

with st.form("trade_logger_form"):
    c1, c2, c3, c4, c5 = st.columns(5)
    in_asset = c1.text_input("Asset", value=st.session_state.log_asset)
    in_dir = c2.selectbox("Direction", ["BUY", "SELL"], index=0 if st.session_state.log_dir == "BUY" else 1)
    in_entry = c3.text_input("Entry Price", value=st.session_state.log_entry)
    in_sl = c4.text_input("Stop Loss", value=st.session_state.log_sl)
    in_tp = c5.text_input("Take Profit", value=st.session_state.log_tp)
    
    submit_log = st.form_submit_button("⚡ COMMIT TRADE TO JOURNAL")
    if submit_log:
        if in_entry and in_sl and in_tp:
            log_trade(in_asset, in_dir, in_entry, in_sl, in_tp)
            st.success("Trade recorded to database! Check the sidebar to mark as WIN or LOSS.")
            st.rerun()
        else:
            st.warning("Please specify Entry, Stop Loss, and Take Profit levels.")
