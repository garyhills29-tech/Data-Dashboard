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
    "transactions": []
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
    for symbol, id in coins.items():
        try:
            # Price + 24h change
            p = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd&include_24hr_change=true").json()
            prices[symbol] = {"price": p[id]["usd"], "change": p[id]["usd_24h_change"]}
            # 30-day chart
            c = requests.get(f"https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency=usd&days=30").json()
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

# ========================= FUNCTIONS =========================
def show_warning(technique):
    st.markdown(f"<div class='warning-banner'>🚨 PHISHING SIMULATION - EDUCATIONAL ONLY 🚨<br><b>Technique:</b> {technique}<br>No data is collected or stored</div>", unsafe_allow_html=True)
    st.balloons()
    st.snow()

def add_transaction(desc, amount):
    st.session_state.transactions.insert(0, {
        "date": datetime.now().strftime("%m-%d %H:%M"),
        "desc": desc,
        "amount": amount
    })

# ========================= PAGES =========================
def login_page():
    st.markdown("""
    <div class='truist-header'>
        <div style='font-size:100px'>🏦</div>
        <h1 style='color:white'>Welcome to Truist Online Banking</h1>
        <p style='color:#ffb700; font-size:24px'>Educational Phishing Awareness Demo — 2025</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:50px; color:white; font-size:20px'>Enter anything below to continue (this is a demo)</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("User ID", value="client001")
    with col2:
        st.text_input("Password", type="password", value="anything")
    if st.button("Log In →", type="primary", use_container_width=True):
        show_warning("Fake Banking Login Page — Credential Harvesting")
        st.session_state.authenticated = True
        st.rerun()

def otp_page():
    st.markdown("<h1 style='text-align:center; color:white'>🔐 Security Verification Required</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ffb700; font-size:20px'>We sent a 6-digit code to **--7842</p>", unsafe_allow_html=True)
    st.text_input("Enter 6-digit code", max_chars=6, placeholder="000000")
    if st.button("Verify", type="primary", use_container_width=True):
        show_warning("2FA / OTP Interception Attack")
        st.session_state.otp_verified = True
        st.rerun()

def dashboard():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Welcome Back, CLIENT001</h1><p style='text-align:center'><span class='recording-dot'></span> Session is being recorded</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Checking", f"${st.session_state.checking:,.2f}")
    with col2:
        st.metric("Savings", f"${st.session_state.savings:,.2f}")
    with col3:
        crypto_total = sum(st.session_state.crypto[c] * prices[c]["price"] for c in st.session_state.crypto)
        st.metric("Crypto Portfolio", f"${crypto_total:,.2f}")

    st.markdown("<h2 style='color:#ffb700'>Recent Transactions</h2>", unsafe_allow_html=True)
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions[:15])
        df["amount"] = df["amount"].apply(lambda x: f"<span style='color:green'>+${x:,.2f}</span>" if x > 0 else f"<span style='color:red'>-${-x:,.2f}</span>", )
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No transactions yet — make some moves!")

def transfer():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Transfer Funds</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        from_acc = st.selectbox("From Account", ["Checking", "Savings"])
    with col2:
        to_acc = "Savings" if from_acc == "Checking" else "Checking")
        amount = st.number_input("Amount", min_value=0.01, step=10.0)
    if st.button("Transfer Now", type="primary"):
        from_bal = st.session_state.checking if from_acc == "Checking" else st.session_state.savings
        if amount > from_bal:
            st.error("Insufficient funds!")
        else:
            if from_acc == "Checking":
                st.session_state.checking -= amount
                st.session_state.savings += amount
            else:
                st.session_state.savings -= amount
                st.session_state.checking += amount
            add_transaction(f"Transfer to {to_acc}", amount if to_acc == "Savings" else -amount)
            st.success(f"Transferred ${amount:,.2f} to {to_acc}")
            st.balloons()
            st.rerun()

def crypto_wallet():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Crypto Wallet — Live Prices & Charts</h1>", unsafe_allow_html=True)
    total = 0
    for symbol, amt in st.session_state.crypto.items():
        if amt > 0:
            price = prices[symbol]["price"]
            val = amt * price
            total += val
            change = prices[symbol]["change"]
            color = "price-up" if change >= 0 else "price-down"
            st.markdown(f"<div class='glass-card'><h3>{symbol} — {amt:,.6f} coins</h3><h2>${val:,.2f} <span class='{color}'>({change:+.2f}% 24h)</span></h2></div>", unsafe_allow_html=True)
            st.line_chart(charts[symbol], use_container_width=True, height=300)

    st.markdown(f"<div class='glass-card'><h2>Total Crypto Value: ${total:,.2f}</h2></div>", unsafe_allow_html=True)

    st.markdown("### Buy / Sell Crypto")
    col1, col2, col3 = st.columns(3)
    with col1:
        coin = st.selectbox("Select Coin", list(prices.keys()))
    with col2:
        usd = st.number_input("USD Amount", min_value=100.0, min_value=1.0)
    with col3:
        price = prices[coin]["price"]
        if st.button("BUY 🟩", type="primary"):
            if usd > st.session_state.checking:
                st.error("Not enough fiat!")
            else:
                bought = usd / price
                st.session_state.crypto[coin] += bought
                st.session_state.checking -= usd
                add_transaction(f"Bought {coin}", -usd)
                st.success(f"Bought {bought:.6f} {coin}!")
                st.balloons()
                st.rerun()
        if st.button("SELL 🟥"):
            max_usd = st.session_state.crypto[coin] * price
            if usd > max_usd:
                st.error("Not enough coins!")
            else:
                sold = usd / price
                st.session_state.crypto[coin] -= sold
                st.session_state.checking += usd
                add_transaction(f"Sold {coin}", +usd)
                st.success(f"Sold {sold:.6f} {coin}!")
                st.balloons()
                st.rerun()

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
        st.markdown("<h2 style='color:#ffb700'>Transaction History</h2>", unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.transactions)
        if not df.empty:
            df["amount"] = df["amount"].apply(lambda x: f"+${x:,.2f}" if x > 0 else f"-${-x:,.2f}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No transactions yet")

st.caption("Red Team Educational Demo — November 18, 2025 — No real data collected — Built with ❤ by you & Grok"))
