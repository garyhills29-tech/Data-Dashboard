import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

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
def get_live_price(coin_id):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true").json()
        return {
            "price": r[coin_id]["usd"],
            "change": r[coin_id]["usd_24h_change"]
        }
    except:
        return {"price": 0, "change": 0}

@st.cache_data(ttl=300)
def get_chart_data(coin_id, days=30):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        r = requests.get(url, params={"vs_currency": "usd", "days": days, "interval": "hourly"}).json()
        df = pd.DataFrame(r["prices"], columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit='ms')
        return df
    except:
        # Fallback fake data
        dates = pd.date_range(end=datetime.now(), periods=720, freq='H')
        base = 68000 if "bitcoin" in coin_id else 3100 if "ethereum" in coin_id else 170
        prices = [base + random.uniform(-base*0.1, base*0.1) for _ in range(720)]
        return pd.DataFrame({"date": dates, "price": prices})

coin_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "DOGE": "dogecoin",
    "PEPE": "pepe",
    "GROK": "grok"
}

# Live current prices
current_prices = {}
for symbol, coin_id in coin_map.items():
    current_prices[symbol] = get_live_price(coin_id)

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
    st.session_state.transactions.insert(0, {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "desc": desc,
        "amount": amount
    })

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
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Live Crypto Wallet & Charts</h1>", unsafe_allow_html=True)
    total_val = 0
    for symbol, amt in st.session_state.crypto.items():
        if amt > 0:
            price_data = current_prices.get(symbol, {"price": 0, "change": 0})
            val = amt * price_data["price"]
            total_val += val
            change = price_data["change"]
            color = "price-up" if change >= 0 else "price-down"
            st.markdown(f"<div class='glass-card'><h3>{symbol} — {amt:,.6f}</h3><h2>${val:,.2f} <span class='{color}'>({change:+.2f}% 24h)</span></h2></div>", unsafe_allow_html=True)

            # LIVE CHART
            chart_df = get_chart_data(coin_map[symbol])
            fig = go.Figure(data=[go.Scatter(x=chart_df['date'], y=chart_df['price'], mode='lines', line=dict(color="#ffb700", width=3))])
            fig.update_layout(title=f"{symbol}/USD - 30 Day Chart", xaxis_title="Date", yaxis_title="Price (USD)", template="plotly_dark", height=400, margin=dict(l=0,r=0,b=0,t=50))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"<div class='glass-card'><h2>Total Crypto Value: ${total_val:,.2f}</h2></div>", unsafe_allow_html=True)

    # Buy/Sell
    col1, col2, col3 = st.columns(3)
    with col1:
        coin = st.selectbox("Coin", list(coin_map.keys()))
    with col2:
        usd = st.number_input("USD Amount", min_value=1.0, value=100.0)
    with col3:
        if st.button("BUY 🟩", type="primary"):
            price = current_prices[coin]["price"]
            if usd > st.session_state.checking:
                st.error("Not enough funds!")
            else:
                bought = usd / price
                st.session_state.crypto[coin] += bought
                st.session_state.checking -= usd
                add_transaction(f"Bought {coin}", -usd)
                st.success(f"Bought {bought:.6f} {coin}!")
                st.balloons()
                st.rerun()
        if st.button("SELL 🟥"):
            price = current_prices[coin]["price"]
            max_usd = st.session_state.crypto[coin] * price
            if usd > max_usd:
                st.error(f"Only ${max_usd:,.2f} available")
            else:
                sold = usd / price
                st.session_state.crypto[coin] -= sold
                st.session_state.checking += usd
                add_transaction(f"Sold {coin}", +usd)
                st.success(f"Sold {sold:.6f} {coin}!")
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
    if st.button("Transfer Now", type="primary"):
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
            st.success(f"Transferred ${amount:,.2f}")
            st.balloons()
            st.rerun()

def dashboard():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Welcome back</h1><p style='text-align:center'><span class='recording-dot'></span> Session recorded</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Checking", f"${st.session_state.checking:,.2f}")
    with col2:
        st.metric("Savings", f"${st.session_state.savings:,.2f}")
    with col3:
        total_crypto = sum(st.session_state.crypto[c] * current_prices[c]["price"] for c in st.session_state.crypto if c in current_prices)
        st.metric("Crypto Portfolio", f"${total_crypto:,.2f}")

    st.markdown("<h2 style='color:#ffb700'>Recent Transactions</h2>", unsafe_allow_html=True)
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions[:10])
        df["amount"] = df["amount"].apply(lambda x: f"+${x:,.2f}" if x > 0 else f"-${-x:,.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet")

# ========================= SIDEBAR =========================
def sidebar():
    st.sidebar.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-logo-white.png", width=200)
    st.sidebar.markdown("<h2 style='color:#ffb700;text-align:center'>CLIENT001</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='background:#ffb700;color:#502b85;padding:12px;border-radius:10px;text-align:center;font-weight:bold'>SECURE SESSION</p>", unsafe_allow_html=True)
    return st.sidebar.radio("Navigate", ["Dashboard", "Transfer Funds", "Crypto Wallet", "Transaction History"])

# ========================= MAIN =========================
if not st.session_state.authenticated:
    login_page()
elif not st.session_state.otp_verified:
    otp_page()
else:
    page = sidebar()
    if page == "Dashboard":
        dashboard()
    elif page == "Transfer Funds":
        transfer()
    elif page == "Crypto Wallet":
        crypto_wallet()
    elif page == "Transaction History":
        st.markdown("<h2 style='color:#ffb700'>Full Transaction History</h2>", unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.transactions)
        df["amount"] = df["amount"].apply(lambda x: f"+${x:,.2f}" if x > 0 else f"-${-x:,.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)

st.caption("Red Team Educational Demo — November 18, 2025 — No real data collected — Built with ❤ for awareness")
