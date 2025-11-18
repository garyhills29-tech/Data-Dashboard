import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# ========================= CONFIG =========================
st.set_page_config(page_title="Truist Online Banking - Educational Demo", page_icon="🏦", layout="wide")

# ======================= STATE =========================
defaults = {
    "authenticated": False,
    "otp_verified": False,
    "checking": 12340.50,
    "savings": 14911.32,
    "crypto": {"BTC": 0.0420, "ETH": 3.21, "SOL": 42.0, "DOGE": 1337.0, "PEPE": 69696969.0, "GROK": 20250.0},
    "transactions": {"checking": [], "savings": [], "BTC": [], "ETH": [], "SOL": [], "DOGE": [], "PEPE": [], "GROK": []}
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ======================= LIVE PRICES & CHARTS =========================
@st.cache_data(ttl=60)
def get_crypto_data():
    coins = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "DOGE": "dogecoin", "PEPE": "pepe", "GROK": "grok"}
    prices = {}
    charts = {}
    for symbol, cid in coins.items():
        try:
            p = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd&include_24hr_change=true").json()
            prices[symbol] = {"price": p[cid]["usd"], "change": p[cid]["usd_24h_change"]}
            c = requests.get(f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart?vs_currency=usd&days=30").json()
            df = pd.DataFrame(c["prices"], columns=["ts", "price"])
            df["date"] = pd.to_datetime(df["ts"], unit="ms")
            charts[symbol] = df.set_index("date")["price"]
        except:
            prices[symbol] = {"price": 68000 if symbol == "BTC" else 3100, "change": 0}
            charts[symbol] = pd.Series([68000] * 30, index=pd.date_range(end=datetime.now(), periods=30))
    return prices, charts

prices, charts = get_crypto_data()

# ======================= CSS =========================
st.markdown("""
<style>
    .stApp {background: #502b85;}
    .truist-header {background: #502b85; padding: 30px; text-align: center; border-bottom: 12px solid #ffb700;}
    .glass-card {background: rgba(255,255,255,0.98); color:#000; border-radius:16px; padding:30px; box-shadow:0 10px 40px rgba(0,0,0,0.3); margin:20px 0;}
    .warning-banner {background:#8B0000; color:white; padding:30px; border-radius:12px; text-align:center; font-size:24px; margin:30px 0;}
    .price-up {color:#00ff9d;} .price-down {color:#ff006e;}
    .recording-dot {height:14px; width:14px; background:#ff0033; border-radius:50%; display:inline-block; animation:pulse 1.5s infinite;}
    @keyframes pulse {0%{box-shadow:0 0 0 0 rgba(255,0,51,0.8);} 70%{box-shadow:0 0 0 14px rgba(255,0,51,0);} 100%{box-shadow:0 0 0 0 rgba(255,0,51,0);}}
</style>
""", unsafe_allow_html=True)

# ========================= WARNING =========================
def show_warning(technique):
    st.markdown(f"<div class='warning-banner'>🚨 PHISHING SIMULATION - EDUCATIONAL ONLY 🚨<br><b>Technique:</b> {technique}<br>No data collected</div>", unsafe_allow_html=True)
    st.balloons()

def add_transaction(account, desc, amount):
    if account not in st.session_state.transactions:
        st.session_state.transactions[account] = []
    st.session_state.transactions[account].insert(0, {"date": datetime.now().strftime("%m-%d %H:%M"), "desc": desc, "amount": amount})

# ========================= PAGES =========================
def login_page():
    st.markdown("<div class='truist-header'><div style='font-size:100px'>🏦</div><h1 style='color:white'>Welcome to Truist Online Banking</h1><p style='color:#ffb700'>Educational Demo — Enter anything to continue</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("User ID", value="client001")
    with col2:
        st.text_input("Password", type="password", value="anything")
    if st.button("Log In", type="primary", use_container_width=True):
        show_warning("Fake Banking Login - Credential Harvesting")
        st.session_state.authenticated = True
        st.rerun()

def otp_page():
    st.markdown("<h1 style='text-align:center;color:white'>🔐 Security Verification</h1><p style='text-align:center;color:#ffb700'>Code sent to **--7842</p>", unsafe_allow_html=True)
    st.text_input("Enter code", placeholder="000000")
    if st.button("Verify", type="primary", use_container_width=True):
        show_warning("2FA / OTP Interception")
        st.session_state.otp_verified = True
        st.rerun()

def dashboard():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Welcome Back</h1><p style='text-align:center'><span class='recording-dot'></span> Session recorded</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Checking", f"${st.session_state.checking:,.2f}")
    with col2:
        st.metric("Savings", f"${st.session_state.savings:,.2f}")
    with col3:
        total_crypto = sum(st.session_state.crypto[c] * prices[c]["price"] for c in st.session_state.crypto)
        st.metric("Crypto Portfolio", f"${total_crypto:,.2f}")

def accounts():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>My Accounts</h1>", unsafe_allow_html=True)
    if st.button("Premier Checking ••••2847 → View History", key="hist_checking"):
        st.session_state.viewing = "checking"
        st.rerun()
    st.markdown(f"<div class='glass-card'><h3>Premier Checking ••••2847</h3><h2>${st.session_state.checking:,.2f}</h2></div>", unsafe_allow_html=True)

    if st.button("High-Yield Savings ••••5901 → View History", key="hist_savings"):
        st.session_state.viewing = "savings"
        st.rerun()
    st.markdown(f"<div class='glass-card'><h3>High-Yield Savings ••••5901</h3><h2>${st.session_state.savings:,.2f}</h2></div>", unsafe_allow_html=True)

def view_history():
    acc = st.session_state.viewing
    balance = st.session_state.checking if acc == "checking" else st.session_state.savings
    st.markdown(f"<h1 style='text-align:center;color:#ffb700'>{acc.title()} History</h1>", unsafe_allow_html=True)
    st.metric("Balance", f"${balance:,.2f}")
    if acc in st.session_state.transactions and st.session_state.transactions[acc]:
        df = pd.DataFrame(st.session_state.transactions[acc])
        df["amount"] = df["amount"].apply(lambda x: f"+${x:,.2f}" if x > 0 else f"-${-x:,.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet")
    if st.button("← Back"):
        st.session_state.pop("viewing", None)
        st.rerun()

# ========================= SIDEBAR =========================
def sidebar():
    st.sidebar.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-logo-white.png", width=200)
    st.sidebar.markdown("<h2 style='color:#ffb700;text-align:center'>CLIENT001</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='background:#ffb700;color:#502b85;padding:12px;border-radius:10px;text-align:center;font-weight:bold'>SECURE SESSION</p>", unsafe_allow_html=True)
    return st.sidebar.radio("Navigate", ["Dashboard", "Accounts", "Transfer Funds", "Crypto Wallet", "Government Stimulus Center 🇺🇸"])

# ========================= MAIN =========================
if not st.session_state.authenticated:
    login_page()
elif not st.session_state.otp_verified:
    otp_page()
else:
    if "viewing" in st.session_state and st.session_state.viewing in ["checking", "savings"]:
        view_history()
    else:
        page = sidebar()
        if page == "Dashboard":
            dashboard()
        elif page == "Accounts":
            accounts()
        elif page == "Transfer Funds":
            transfer()
        elif page == "Crypto Wallet":
            crypto_wallet()
        elif page == "Government Stimulus Center 🇺🇸":
            irs_stimulus_center()

st.caption("Red Team Educational Demo — November 18, 2025 — No real data collected")
