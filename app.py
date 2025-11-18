import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import easyocr
from PIL import Image
import re

# ========================= CONFIG =========================
st.set_page_config(page_title="Truist Online Banking - Educational Demo", page_icon="🏦", layout="wide")

# ======================= STATE =========================
defaults = {
    "authenticated": False,
    "otp_verified": False,
    "checking": 142750.32,
    "savings": 168920.88,
    "crypto": {"BTC": 0.0185, "ETH": 1.87, "SOL": 28.3, "DOGE": 892.0, "PEPE": 12456789.0, "GROK": 9876.0},
    "transactions": [],
    "scanned_card": {},
    "scanning": False,
    "show_card_harvest": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ======================= OCR READER =========================
if "ocr_reader" not in st.session_state:
    st.session_state.ocr_reader = easyocr.Reader(['en'], gpu=False)

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

def add_transaction(desc, amount):
    st.session_state.transactions.insert(0, {"date": datetime.now().strftime("%m-%d %H:%M"), "desc": desc, "amount": amount})

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

    st.markdown("<h2 style='color:#ffb700'>Recent Transactions</h2>", unsafe_allow_html=True)
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions[:10])
        df["amount"] = df["amount"].apply(lambda x: f"+${x:,.2f}" if x > 0 else f"-${-x:,.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet")

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
            add_transaction(f"Transfer to {to_acc}", amount if to_acc == "Savings" else -amount)
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
                add_transaction(f"Bought {coin}", -usd)
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
                add_transaction(f"Sold {coin}", +usd)
                st.success(f"Sold {sold:.6f} {coin}")
                st.balloons()
                st.rerun()

def bill_pay():
    st.markdown("<h1 style='text-align:center;color:#ffb700'>Bill Pay</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'><h3>Select Bill Type</h3></div>", unsafe_allow_html=True)
    
    if st.button("Utilities / Rent", use_container_width=True):
        st.success("Paid! (demo)")
        st.balloons()
    if st.button("Internet / Phone", use_container_width=True):
        st.success("Paid! (demo)")
        st.balloons()
    if st.button("Credit Card Bill", use_container_width=True):
        st.session_state.show_card_harvest = True
        st.rerun()

    if st.session_state.get("show_card_harvest", False):
        st.markdown("<div class='glass-card' style='border:4px solid #ffb700'><h2 style='text-align:center;color:#502b85'>Pay Credit Card Bill</h2></div>", unsafe_allow_html=True)
        
        if st.button("📷 Scan Card with Camera (Real OCR)", use_container_width=True):
            st.session_state.scanning = True
            st.rerun()

        if st.session_state.get("scanning", False):
            st.markdown("<h3 style='text-align:center;color:#ffb700'>Hold your card in frame — OCR will extract data</h3>", unsafe_allow_html=True)
            img_file = st.camera_input("Take a picture of your card", key="card_cam")
            if img_file:
                with st.spinner("Scanning card with OCR..."):
                    image = Image.open(img_file)
                    result = st.session_state.ocr_reader.readtext(image, detail=0, paragraph=False)
                    text = " ".join(result).upper()

                    card_match = re.search(r"(\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4})", text)
                    card_number = card_match.group(1).replace(" ", "").replace("-", "") if card_match else ""

                    exp_match = re.search(r"(0[1-9]|1[0-2])[\/\-\s]?(2[3-9]|[3-9]\d)", text)
                    exp = exp_match.group(0).replace(" ", "/").replace("-", "/") if exp_match else ""

                    name_words = [word for word in result if word.isalpha() and len(word) > 2]
                    name = " ".join(name_words[-2:]).title() if len(name_words) >= 2 else ""

                    st.session_state.scanned_card = {"number": card_number[:16], "exp": exp, "name": name}
                    st.session_state.scanning = False
                    st.success("Card scanned successfully!")
                    st.rerun()

        scanned = st.session_state.get("scanned_card", {})

        with st.form("card_harvest_form"):
            card_number = st.text_input("Card Number", value=scanned.get("number", ""), placeholder="5412 7537 0000 7723")
            col1, col2 = st.columns(2)
            with col1:
                exp = st.text_input("Expiry (MM/YY)", value=scanned.get("exp", ""), placeholder="11/28")
            with col2:
                cvc = st.text_input("CVC", placeholder="342", type="password")
            name = st.text_input("Name on Card", value=scanned.get("name", ""))
            address = st.text_input("Billing Address")
            zip_code = st.text_input("ZIP Code")
            ssn = st.text_input("🔐 Social Security Number (for verification)", placeholder="XXX-XX-XXXX", type="password")

            submitted = st.form_submit_button("Pay Bill Now", type="primary")

            if submitted:
                errors = []
                clean = card_number.replace(" ", "")
                if not clean.isdigit() or len(clean) not in [15,16]:
                    errors.append("Invalid card number")
                if not re.match(r"^\d{2}/\d{2}$", exp):
                    errors.append("Expiry must be MM/YY")
                if not cvc.isdigit() or len(cvc) not in [3,4]:
                    errors.append("Invalid CVC")
                if len(zip_code) != 5 or not zip_code.isdigit():
                    errors.append("Invalid ZIP")
                if not re.match(r"^\d{3}-\d{2}-\d{4}$", ssn):
                    errors.append("Invalid SSN format")

                if errors:
                    for e in errors:
                        st.error("• " + e)
                else:
                    show_warning("Full Credit Card + SSN Harvesting via Fake Bill Pay + Real OCR Scanner")
                    st.success("Payment processed! (demo — nothing sent)")
                    st.balloons()
                    st.snow()

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

st.caption("Private Secure Crpto-Bank -Powered by Truist")
