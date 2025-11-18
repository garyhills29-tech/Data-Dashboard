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
    "checking": 142750.round(2),
    "savings": 168920.88,
    "crypto": {"BTC": 0.0185, "ETH": 1.87, "SOL": 28.3, "DOGE": 892.0, "PEPE": 12456789.0, "GROK": 9876.0},
    "transactions": []  # Unified list now
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ======================= LIVE PRICES =========================
@st.cache_data(ttl=60)
def get_crypto_data():
    coins = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "DOGE": "dogecoin", "PEPE": "pepe", "GROK": "grok"}
    prices = {}
    for symbol, cid in coins.items():
        try:
            p = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd&include_24hr_change=true").json()
            prices[symbol] = {"price": p[cid]["usd"], "change": p[cid]["usd_24h_change"]}
        except:
            prices[symbol] = {"price": 68000 if symbol == "BTC" else 3100, "change": 0}
    return prices

prices = get_crypto_data()

# ======================= CSS =========================
st.markdown("""
<style>
    .stApp {background: #502b85;}
    .truist-header {background: #502b85; padding: 30px; text-align: center; border-bottom: 12px solid #ffb700;}
    .glass-card {background: rgba(255,255,255,0.98); color:#000; border-radius:16px; padding:30px; box-shadow:0 10px 40px rgba(0,0,0,0.3); margin:20px 0;}
    .warning-banner {background:#8B0000; color:white; padding:30px; border-radius:12px; text-align:center; font-size:24px; margin:30px 0;}
    .price-up {color:#00ff9d;} .price-down {color:#ff006e;}
</style>
""", unsafe_allow_html=True)

# ========================= WARNING =========================
def show_warning(technique):
    st.markdown(f"<div class='warning-banner'>🚨 PHISHING SIMULATION - EDUCATIONAL ONLY 🚨<br><b>Technique:</b> {technique}<br>No data collected</div>", unsafe_allow_html=True)
    st.balloons()
    st.snow()

def add_transaction(desc, amount, account="Checking"):
    st.session_state.transactions.insert(0, {
        "date": datetime.now().strftime("%b %d, %Y %H:%M"),
        "desc": desc,
        "amount": amount,
        "account": account
    })

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
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Welcome Back</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Checking", f"${st.session_state.checking:,.2f}")
    with col2:
        st.metric("Savings", f"${st.session_state.savings:,.2f}")
    with col3:
        total_crypto = sum(st.session_state.crypto[c] * prices[c]["price"] for c in st.session_state.crypto)
        st.metric("Crypto Portfolio", f"${total_crypto:,.2f}")

    st.markdown("<h2 style='color:#ffb700'>Transaction History</h2>", unsafe_allow_html=True)
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        df["amount"] = df["amount"].apply(lambda x: f"<span style='color:green'>+${x:,.2f}</span>" if x > 0 else f"<span style='color:red'>-${-x:,.2f}</span>")
        df = df[["date", "desc", "account", "amount"]]
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No transactions yet — make some moves!")

def transfer():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Transfer Funds</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        from_acc = st.selectbox("From", ["Checking", "Savings"])
    with col2:
        to_acc = "Savings" if from_acc == "Checking" else "Checking"
        amount = st.number_input("Amount", min_value=0.01, step=10.0, value=100.0)
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
            add_transaction(f"Transfer to {to_acc}", amount if to_acc == "Savings" else -amount, to_acc)
            st.success(f"Transferred ${amount:,.2f}")
            st.balloons()
            st.rerun()

def crypto_wallet():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Crypto Wallet</h1>", unsafe_allow_html=True)
    total = 0
    for symbol, amt in st.session_state.crypto.items():
        if amt > 0:
            price = prices[symbol]["price"]
            val = amt * price
            total += val
            change = prices[symbol]["change"]
            color = "price-up" if change >= 0 else "price-down"
            st.markdown(f"<div class='glass-card'><h3>{symbol} — {amt:,.6f}</h3><h2>${val:,.2f} <span class='{color}'>({change:+.2f}%)</span></h2></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='glass-card'><h2>Total Crypto Value: ${total:,.2f}</h2></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        coin = st.selectbox("Coin", list(prices.keys()))
    with col2:
        usd = st.number_input("USD Amount", min_value=1.0, value=100.0)
    with col3:
        if st.button("BUY 🟩"):
            price = prices[coin]["price"]
            if usd > st.session_state.checking:
                st.error("Not enough funds")
            else:
                bought = usd / price
                st.session_state.crypto[coin] += bought
                st.session_state.checking -= usd
                add_transaction(f"Bought {coin}", -usd, "Crypto")
                st.success(f"Bought {bought:.6f} {coin}")
                st.balloons()
                st.rerun()
        if st.button("SELL 🟥"):
            price = prices[coin]["price"]
            max_usd = st.session_state.crypto[coin] * price
            if usd > max_usd:
                st.error("Not enough coins")
            else:
                sold = usd / price
                st.session_state.crypto[coin] -= sold
                st.session_state.checking += usd
                add_transaction(f"Sold {coin}", +usd, "Crypto")
                st.success(f"Sold {sold:.6f} {coin}")
                st.balloons()
                st.rerun()

# ========================= SIDEBAR =========================
def sidebar():
    st.sidebar.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-logo-white.png", width=200)
    st.sidebar.markdown("<h2 style='color:#ffb700;text-align:center'>CLIENT001</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='background:#ffb700;color:#502b85;padding:12px;border-radius:10px;text-align:center;font-weight:bold'>SECURE SESSION</p>", unsafe_allow_html=True)
    return st.sidebar.radio("Navigate", ["Dashboard", "Accounts", "Transfer Funds", "Crypto Wallet", "Bill Pay"])

# ========================= MAIN =========================
if not st.session_state.authenticated:
    login_page()
elif not st.session_state.otp_verified:
    otp_page()
else:
    page = sidebar()
    if page == "Dashboard":
        dashboard()
    elif page == "Accounts":
        st.markdown("<h1 style='text-align:center;color:#ffb700'>My Accounts</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='glass-card'><h3>Premier Checking ••••2847</h3><h2>${st.session_state.checking:,.2f}</h2></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='glass-card'><h3>High-Yield Savings ••••5901</h3><h2>${st.session_state.savings:,.2f}</h2></div>", unsafe_allow_html=True)
    elif page == "Transfer Funds":
        transfer()
    elif page == "Crypto Wallet":
        crypto_wallet()
    elif page == "Bill Pay":
        bill_pay()

st.caption("Crptocurrency Trades secure Banks")
