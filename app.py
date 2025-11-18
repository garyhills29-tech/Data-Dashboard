import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import random

# ========================= CONFIG =========================
st.set_page_config(page_title="Truist Online Banking - Educational Demo", page_icon="🏦", layout="wide")

# ======================= STATE =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False
if "checking" not in st.session_state:
    st.session_state.checking = 12340.50
if "savings" not in st.session_state:
    st.session_state.savings = 14911.32
if "crypto" not in st.session_state:
    st.session_state.crypto = {"BTC": 0.0420, "ETH": 3.21, "SOL": 42.0, "DOGE": 1337.0, "PEPE": 69696969.0, "GROK": 20250.0}
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# ======================= LIVE PRICES & CHARTS =========================
@st.cache_data(ttl=60)
def get_price_and_chart(coin_id):
    try:
        price = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true").json()[coin_id]["usd"]
        change = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true").json()[coin_id]["usd_24h_change"]
        chart_data = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=30").json()["prices"]
        df = pd.DataFrame(chart_data, columns=["ts", "price"])
        df["date"] = pd.to_datetime(df["ts"], unit="ms")
        df = df.set_index("date")["price"]
        return price, change, df
    except:
        fake = pd.Series([random.uniform(60000, 70000) for _ in range(30)], index=pd.date_range(end=datetime.now(), periods=30))
        return 68200, 1.8, fake

coin_ids = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "DOGE": "dogecoin", "PEPE": "pepe", "GROK": "grok"}
prices = {}
charts = {}
for symbol, cid in coin_ids.items():
    prices[symbol], _, charts[symbol] = get_price_and_chart(cid)

# ======================= CSS =========================
# Add this to show something when not logged in
if not st.session_state.authenticated and not st.session_state.otp_verified:
    st.markdown("<div style='text-align:center; padding:100px; color:white; font-size:30px'>🔒 Secure Login Required<br><small>Enter any credentials to continue (educational demo)</small></div>", unsafe_allow_html=True)
st.markdown("""
<style>
    .stApp {background: #502b85;}
    .truist-header {background: #502b85; padding: 20px; text-align: center; border-bottom: 10px solid #ffb700;}
    .glass-card {background: rgba(255,255,255,0.98); color:#000; border-radius:16px; padding:32px; box-shadow:0 12px 40px rgba(0,0,0,0.3); margin:20px 0;}
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

def add_transaction(desc, amount):
    st.session_state.transactions.insert(0, {"date": datetime.now().strftime("%m-%d %H:%M"), "desc": desc, "amount": amount})

# ========================= PAGES =========================
def login_page():
    st.markdown("<div class='truist-header'><div style='font-size:100px'>🏦</div><h1>Welcome to Truist Online Banking</h1></div>", unsafe_allow_html=True)
    st.text_input("User ID")
    st.text_input("Password", type="password")
    if st.button("Log In", type="primary"):
        show_warning("Fake Bank Login - Credential Harvesting")
        st.session_state.authenticated = True
        st.rerun()

def otp_page():
    st.markdown("<h1 style='text-align:center'>🔐 Security Verification</h1><p style='text-align:center'>Code sent to **--7842</p>", unsafe_allow_html=True)
    st.text_input("Enter code")
    if st.button("Verify", type="primary"):
        show_warning("2FA / OTP Interception")
        st.session_state.otp_verified = True
        st.rerun()

def crypto_wallet():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Crypto Wallet - Live Charts</h1>", unsafe_allow_html=True)
    total = 0
    for symbol, amt in st.session_state.crypto.items():
        if amt > 0:
            price = prices[symbol]
            val = amt * price
            total += val
            st.markdown(f"<div class='glass-card'><h3>{symbol} — {amt:,.6f} coins = ${val:,.2f}</h3></div>", unsafe_allow_html=True)
            st.line_chart(charts[symbol], use_container_width=True)
    st.markdown(f"<div class='glass-card'><h2>Total Crypto Value: ${total:,.2f}</h2></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        coin = st.selectbox("Coin", list(coin_ids.keys()))
    with col2:
        usd = st.number_input("USD Amount", min_value=1.0, value=100.0)
    with col3:
        if st.button("BUY 🟩"):
            if usd > st.session_state.checking:
                st.error("Insufficient funds")
            else:
                bought = usd / prices[coin]
                st.session_state.crypto[coin] += bought
                st.session_state.checking -= usd
                add_transaction(f"Bought {coin}", -usd)
                st.success

