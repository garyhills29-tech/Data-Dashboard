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

# ======================= LIVE PRICES & CHART DATA =========================
@st.cache_data(ttl=60)
def get_price_and_chart(coin_id):
    try:
        # Price
        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
        price = requests.get(price_url).json()[coin_id]["usd"]
        change = requests.get(price_url).json()[coin_id]["usd_24h_change"]
        
        # Chart (30 days)
        chart_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=30&interval=daily"
        data = requests.get(chart_url).json()["prices"]
        df = pd.DataFrame(data, columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit='ms')
        df = df.set_index("date")["price"]
        return price, change, df
    except:
        fake_df = pd.Series([random.uniform(60000, 70000) for _ in range(30)], index=pd.date_range(end=datetime.now(), periods=30))
        return 68200, 2.1, fake_df

coin_ids = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "DOGE": "dogecoin", "PEPE": "pepe", "GROK": "grok"}
prices = {}
charts = {}
for symbol, cid in coin_ids.items():
    prices[symbol], change, chart = get_price_and_chart(cid)
    charts[symbol] = chart

# ======================= CSS =========================
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
    st.session_state.transactions.insert(0, {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "desc": desc, "amount": amount})

# ========================= PAGES =========================
def login_page():
    st.markdown("<div class='truist-header'><div style='font-size:100px'>🏦</div><h1>Welcome to Truist Online Banking</h1></div>", unsafe_allow_html=True)
    st.text_input("User ID")
    st.text_input("Password", type="password")
    if st.button("Log In", type="primary"):
        show_warning("Fake Bank Login")
        st.session_state.authenticated = True
        st.rerun()

def otp_page():
    st.markdown("<h1 style='text-align:center'>🔐 Security Verification</h1><p style='text-align:center'>Code sent to **--7842</p>", unsafe_allow_html=True)
    st.text_input("Enter code")
    if st.button("Verify", type="primary"):
        show_warning("2FA Interception")
        st.session_state.otp_verified = True
        st.rerun()

def crypto_wallet():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Crypto Wallet - Live Charts & Trading</h1>", unsafe_allow_html=True)
    total = 0
    for symbol, amt in st.session_state.crypto.items():
        if amt > 0:
            price = prices[symbol]
            val = amt * price
            total += val
            st.markdown(f"<div class='glass-card'><h3>{symbol} — {amt:,.6f} coins = ${val:,.2f}</h3></div>", unsafe_allow_html=True)
            st.line_chart(charts[symbol], use_container_width=True, height=300)
    st.markdown(f"<div class='glass-card'><h2>Total Crypto Value: ${total:188,.2f}</h2></div>", unsafe_allow_html=True)

    # Buy/Sell
    col1, col2, col3 = st.columns(3)
    with col1:
        coin = st.selectbox("Coin", list(coin_ids.keys()))
    with col2:
        usd = st.number_input("USD Amount", min_value=1.0, value=100.0)
    with col3:
        if st.button("BUY 🟩"):
            price = prices[coin]
            if usd > st.session_state.checking:
                st.error("Not enough funds")
            else:
                bought = usd / price
                st.session_state.crypto[coin] += bought
                st.session_state.checking -= usd
                add_transaction(f"Bought {coin}", -usd)
                st.success(f"Bought {bought:.6f} {coin}")
                st.balloons()
                st.rerun()
        if st.button("SELL 🟥"):
            price = prices[coin]
            max_usd = st.session_state.crypto[coin] * price
            if usd > max_usd:
                st.error("Not enough coins")
            else:
                sold = usd / price
                st.session_state.crypto[coin] -= sold
                st.session_state.checking += usd
                add_transaction(f"Sold {coin}", +usd)
                st.success(f"Sold {sold:.6f} {coin}")
                st.balloons()
                st.rerun()

def transfer():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Transfer Funds</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        from_acc = st.selectbox("From", ["Checking", "Savings"])
    with col2:
        to_acc = "Savings" if from_acc == "Checking" else "Checking"
        amount = st.number_input("Amount", min_value=0.01, step=10.0)
    if st.button("Transfer", type="primary"):
        from_bal = st.session_state.checking if from_acc == "Checking" else st.session_state.savings
        if amount > from_bal:
            st.error("Insufficient funds")
        else:
            if from_acc == "Checking":
                st.session_state.checking -= amount
                st.session_state.savings += amount
            else:
                st.session_state.savings -= amount
                st.session_state.checking += amount
            add_transaction(f"Transfer to {to_acc}", amount if to_acc == "Savings" else -amount)
            st.success("Transfer successful")
            st.balloons()
            st.rerun()

def dashboard():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Welcome back</h1><p style='text-align:center'><span class='recording-dot'></span> Session recorded</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Checking", f"${st.session_state.checking:,.2f}")
        st.metric("Savings", f"${st.session_state.savings:,.2f}")
    with col2:
        total_crypto = sum(st.session_state.crypto[c] * prices[c] for c in st.session_state.crypto)
        st.metric("Crypto Portfolio", f"${total_crypto:,.2f}")
    st.markdown("<h2 style='color:#ffb700'>Recent Transactions</h2>", unsafe_allow_html=True)
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions[:10])
        df["amount"] = df["amount"].apply(lambda x: f"+${x:,.2f}" if x > 0 else f"-${-x:,.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ========================= SIDEBAR & ROUTING =========================
def sidebar():
    st.sidebar.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-logo-white.png", width=200)
    st.sidebar.markdown("<h2 style='color:#ffb700;text-align:center'>CLIENT001</h2>", unsafe_allow
