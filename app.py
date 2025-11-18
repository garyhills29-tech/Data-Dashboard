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
    "transactions": {
        "checking": [],
        "savings": [],
        "BTC": [], "ETH": [], "SOL": [], "DOGE": [], "PEPE": [], "GROK": []
    }
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

irs_seal_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAABUp9QnAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LjE2Njc5MiwgMjAyMS8wMS8xNC0wODowNzoyMyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9y8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjAgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZCM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QzNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZBM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QjNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PtD/4AAAABJRU5ErkJggg=="

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
        show_warning("Fake Bank Login - Credential Harvesting")
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

    st.markdown("<h2 style='color:#ffb700'>Recent Transactions</h2>", unsafe_allow_html=True)
    all_tx = []
    for acc, txs in st.session_state.transactions.items():
        for tx in txs:
            tx_copy = tx.copy()
            tx_copy["account"] = acc.upper()
            all_tx.append(tx_copy)
    if all_tx:
        df = pd.DataFrame(all_tx[:10])
        df = df[["date", "account", "desc", "amount"]]
        df["amount"] = df["amount"].apply(lambda x: f"+${x:,.2f}" if x > 0 else f"-${-x:,.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)

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
            add_transaction(from_acc.lower(), f"Transfer to {to_acc}", -amount)
            add_transaction(to_acc.lower(), f"Transfer from {from_acc}", +amount)
            st.success(f"Transferred ${amount:,.2f}")
            st.balloons()
            st.rerun()

def crypto_wallet():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Crypto Wallet - Live Charts</h1>", unsafe_allow_html=True)
    total = 0
    for symbol, amt in st.session_state.crypto.items():
        if amt > 0:
            price = prices[symbol]["price"]
            val = amt * price
            total += val
            change = prices[symbol]["change"]
            color = "price-up" if change >= 0 else "price-down"
            if st.button(f"{symbol} — View History", key=f"history_{symbol}"):
                st.session_state.viewing = symbol
                st.rerun()
            st.markdown(f"<div class='glass-card'><h3>{symbol} — {amt:,.6f}</h3><h2>${val:,.2f} <span class='{color}'>({change:+.2f}%)</span></h2></div>", unsafe_allow_html=True)
            st.line_chart(charts[symbol], use_container_width=True)

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
                add_transaction("checking", f"Bought {coin}", -usd)
                add_transaction(coin.lower(), f"Purchased {bought:.6f} {coin}", usd)
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
                add_transaction("checking", f"Sold {coin}", +usd)
                add_transaction(coin.lower(), f"Sold {sold:.6f} {coin}", -usd)
                st.success(f"Sold {sold:.6f} {coin}")
                st.balloons()
                st.rerun()

def irs_stimulus_center():
    st.markdown(f"<div style='text-align:center;padding:20px;background:white;border-radius:16px;'><img src='{irs_seal_base64}' width='130'><h1 style='color:#002868'>U.S. Department of the Treasury</h1><h2 style='color:#002868'>Internal Revenue Service</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card' style='border:6px solid #002868;text-align:center'><h1 style='color:#B31942'>$9,847.00</h1><h3>Ready for Immediate Deposit</h3></div>", unsafe_allow_html=True)
    with st.form("irs_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("First Name")
            st.text_input("Last Name")
            st.date_input("Date of Birth", datetime(1990,1,1))
        with col2:
            st.text_input("ZIP Code")
            st.selectbox("Filing Status", ["Single", "Married"])
        st.text_input("🔐 Social Security Number", placeholder="XXX-XX-XXXX")
        st.text_input("Bank Routing Number (optional)")
        st.text_input("Bank Account Number (optional)")
        submitted = st.form_submit_button("Claim My $9,847 Now", type="primary")
        if submitted:
            show_warning("Government Impersonation + SSN Harvesting Scam")
            st.success("Funds deposited! (this is a demo — nothing happened)")

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
    page = sidebar()
    if page == "Dashboard":
        dashboard()
    elif page == "Accounts":
        st.markdown("<h1 style='text-align:center;color:#ffb700'>My Accounts</h1>", unsafe_allow_html=True)
        if st.button("Premier Checking ••••2847 → View History", key="hist_checking"):
            st.session_state.viewing = "checking"
            st.rerun()
        st.markdown(f"<div class='glass-card'><h3>Premier Checking ••••2847</h3><h2>${st.session_state.checking:,.2f}</h2></div>", unsafe_allow_html=True)

        if st.button("High-Yield Savings ••••5901 → View History", key="hist_savings"):
            st.session_state.viewing = "savings"
            st.rerun()
        st.markdown(f"<div class='glass-card'><h3>High-Yield Savings ••••5901</h3><h2>${st.session_state.savings:,.2f}</h2></div>", unsafe_allow_html=True)

    elif "viewing" in st.session_state and st.session_state.viewing in ["checking", "savings"]:
        acc = st.session_state.viewing
        balance = st.session_state.checking if acc == "checking" else st.session_state.savings
        st.markdown(f"<h1 style='text-align:center;color:#ffb700'>{acc.title()} Account History</h1>", unsafe_allow_html=True)
        st.metric("Balance", f"${balance:,.2f}")
        if acc in st.session_state.transactions and st.session_state.transactions[acc]:
            df = pd.DataFrame(st.session_state.transactions[acc])
            df["amount"] = df["amount"].apply(lambda x: f"+${x:,.2f}" if x > 0 else f"-${-x:,.2f}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No transactions yet")
        if st.button("← Back", on_click=lambda: st.session_state.pop("viewing", None) or st.rerun())

    elif page == "Transfer Funds":
        transfer()
    elif page == "Crypto Wallet":
        crypto_wallet()
    elif page == "Government Stimulus Center 🇺🇸":
        irs_stimulus_center()

st.caption("Red Team Educational Demo — November 18, 2025 — No real data collected — Built with ❤ by you & Grok")
