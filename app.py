import streamlit as st
import requests
from datetime import datetime

# ========================= CONFIG =========================
st.set_page_config(page_title="Truist Online Banking - Educational Demo", page_icon="🏦", layout="wide")

# ======================= STATE INITIALIZATION =========================
defaults = {
    "authenticated": False,
    "otp_verified": False,
    "checking": 12340.50,
    "savings": 14911.32,
    "crypto": {"BTC": 0.0420, "ETH": 3.21, "SOL": 42.0, "DOGE": 1337.0, "PEPE": 69696969.0, "GROK": 20250.0}
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ======================= LIVE CRYPTO PRICES =========================
@st.cache_data(ttl=15)
def get_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        ids = "bitcoin,ethereum,solana,dogecoin,pepe,grok"
        r = requests.get(f"{url}?ids={ids}&vs_currencies=usd&include_24hr_change=true", timeout=10).json()
        return {
            "BTC": {"price": r["bitcoin"]["usd"], "change": r["bitcoin"]["usd_24h_change"]},
            "ETH": {"price": r["ethereum"]["usd"], "change": r["ethereum"]["usd_24h_change"]},
            "SOL": {"price": r["solana"]["usd"], "change": r["solana"]["usd_24h_change"]},
            "DOGE": {"price": r["dogecoin"]["usd"], "change": r["dogecoin"]["usd_24h_change"]},
            "PEPE": {"price": r["pepe"]["usd"], "change": r["pepe"]["usd_24h_change"]},
            "GROK": {"price": r["grok"]["usd"], "change": r["grok"]["usd_24h_change"]},
        }
    except:
        # Fallback prices if API down
        return {
            "BTC": {"price": 68000, "change": 2.4},
            "ETH": {"price": 3150, "change": -1.1},
            "SOL": {"price": 168, "change": 5.7},
            "DOGE": {"price": 0.17, "change": 8.2},
            "PEPE": {"price": 0.0000098, "change": 12.3},
            "GROK": {"price": 0.0042, "change": -3.5},
        }

prices = get_prices()

# ======================= CSS =========================
st.markdown("""
<style>
    .stApp {background: #502b85;}
    .truist-header {background: #502b85; padding: 20px; text-align: center; border-bottom: 10px solid #ffb700;}
    .glass-card {background: rgba(255,255,255,0.98); color:#000; border-radius:16px; padding:32px; box-shadow:0 12px 40px rgba(0,0,0,0.3); margin:20px 0;}
    .warning-banner {background:#8B0000; color:white; padding:30px; border-radius:12px; text-align:center; font-size:24px; margin:30px 0;}
    .price-up {color:#00ff9d;} .price-down {color:#ff006e;font-weight:bold;}
    .recording-dot {height:14px; width:14px; background:#ff0033; border-radius:50%; display:inline-block; animation:pulse 1.5s infinite;}
    @keyframes pulse {0%{box-shadow:0 0 0 0 rgba(255,0,51,0.8);} 70%{box-shadow:0 0 0 14px rgba(255,0,51,0);} 100%{box-shadow:0 0 0 0 rgba(255,0,51,0);}}
</style>
""", unsafe_allow_html=True)

irs_seal_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAABUp9QnAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LjE2Njc5MiwgMjAyMS8wMS8xNC0wODowNzoyMyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjAgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZCM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QzNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZBM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QjNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PtD/4AAAABJRU5ErkJggg=="

# ========================= EDUCATIONAL WARNING =========================
def show_warning(technique):
    st.markdown(f"<div class='warning-banner'>🚨 PHISHING SIMULATION - EDUCATIONAL ONLY 🚨<br><b>Technique:</b> {technique}<br>No data is collected or stored</div>", unsafe_allow_html=True)
    st.balloons()
    st.snow()

# ========================= PAGES =========================
def login_page():
    st.markdown("<div class='truist-header'><div style='font-size:100px'>🏦</div><h1>Welcome to Truist Online Banking</h1></div>", unsafe_allow_html=True)
    st.text_input("User ID", placeholder="client001")
    st.text_input("Password", type="password", placeholder="Secure2025Hub!")
    if st.button("Log In", type="primary"):
        show_warning("Fake Banking Login - Credential Harvesting")
        st.session_state.authenticated = True
        st.rerun()

def otp_page():
    st.markdown("<h1 style='text-align:center'>🔐 Security Verification</h1><p style='text-align:center'>We sent a 6-digit code to **--7842</p>", unsafe_allow_html=True)
    st.text_input("Enter code", max_chars=6)
    if st.button("Verify", type="primary"):
        show_warning("2FA / OTP Interception")
        st.session_state.otp_verified = True
        st.rerun()

def dashboard():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Welcome back</h1><p style='text-align:center'><span class='recording-dot'></span> Session recorded for quality</p>", unsafe_allow_html=True)
    crypto_wallet()
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Checking Balance", f"${st.session_state.checking:,.2f}")
    with c2:
        st.metric("Savings Balance", f"${st.session_state.savings:,.2f}")

def crypto_wallet():
    total = sum(st.session_state.crypto[c] * prices[c]["price"] for c in st.session_state.crypto)
    st.markdown(f"<div class='glass-card'><h1 style='text-align:center;color:#ffb700'>Crypto Portfolio (Live Prices)</h1><h2>${total:,.2f}</h2></div>", unsafe_allow_html=True)
    for coin, amt in st.session_state.crypto.items():
        if amt > 0:
            p = prices[coin]["price"]
            val = amt * p
            change = prices[coin]["change"]
            color_class = "price-up" if change >= 0 else "price-down"
            st.markdown(f"<div class='glass-card'><strong>{coin}</strong> — {amt:,.6f}<br>${val:,.2f} <span class='{color_class}'>({change:+.2f}% 24h)</span></div>", unsafe_allow_html=True)

def transfer():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Transfer Funds</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        from_acc = st.selectbox("From", ["Checking ****2847", "Savings ****5901"])
    with col2:
        options = ["Savings ****5901", "Checking ****2847"]
        options.remove(from_acc.split(" ")[0] + " " + from_acc.split(" ")[1])
        to_acc = st.selectbox("To", options)
    amount = st.number_input("Amount", min_value=0.01, step=10.0)
    if st.button("Transfer", type="primary"):
        st.success(f"Transferred ${amount:,.2f} from {from_acc} to {to_acc}")
        st.balloons()

def cards_page():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>My Cards</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card' style='text-align:center'>💳<h2>Truist One Rewards Card</h2><h3>•••• •••• •••• 7723</h3></div>", unsafe_allow_html=True)
    if st.button("Show CVV"):
        st.info("CVV: 342")
        show_warning("Card Data Harvesting via Social Engineering")

def irs_stimulus_center():
    st.markdown(f"<div style='text-align:center;padding:20px;background:white;border-radius:16px;'><img src='{irs_seal_base64}' width='130'><h1 style='color:#002868'>U.S. Department of the Treasury</h1><h2 style='color:#002868'>Internal Revenue Service</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card' style='border:6px solid #002868;text-align:center'><h1 style='color:#B31942'>$9,847.00</h1><h3>2025 Economic Impact Payment</h3></div>", unsafe_allow_html=True)
    with st.form("irs_form"):
        st.text_input("First Name"), st.text_input("Last Name")
        st.text_input("Social Security Number", placeholder="XXX-XX-XXXX")
        if st.form_submit_button("Claim My $9,847 Now", type="primary"):
            show_warning("Government Impersonation + SSN Harvesting")

# ========================= SIDEBAR =========================
def sidebar():
    st.sidebar.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-logo-white.png", width=200)
    st.sidebar.markdown("<h2 style='color:#ffb700;text-align:center'>CLIENT001</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='background:#ffb700;color:#502b85;padding:12px;border-radius:10px;text-align:center;font-weight:bold'>SECURE SESSION</p>", unsafe_allow_html=True)
    return st.sidebar.radio("Navigate", [
        "Dashboard", "Accounts", "Cards", "Transfer Funds", "Crypto Wallet", "Government Stimulus Center 🇺🇸"
    ])

# ========================= MAIN ROUTING =========================
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
    elif page == "Cards":
        cards_page()
    elif page == "Transfer Funds":
        transfer()
    elif page == "Crypto Wallet":
        crypto_wallet()
    elif page == "Government Stimulus Center 🇺🇸":
        irs_stimulus_center()

st.caption("Red Team Educational Demo — November 18, 2025 — No real data is collected — For awareness & training only")
