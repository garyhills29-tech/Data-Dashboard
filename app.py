import streamlit as st
from datetime import datetime
import random, time

# ========================= CONFIG =========================
st.set_page_config(page_title="Truist Online Banking", page_icon="🏦", layout="wide")

# ======================= STATE =========================
for key in ["authenticated", "otp_verified", "is_admin"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ======================= IRS SEAL =========================
irs_seal_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAABUp9QnAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LjE2Njc5MiwgMjAyMS8wMS8xNC0wODowNzoyMyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjAgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZCM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QzNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZBM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QjNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PtD/4AAAABJRU5ErkJggg=="

# ========================= CSS ===========================
st.markdown("""
<style>
    .stApp {background: #502b85;}
    .truist-header {background: #502b85; padding: 20px; text-align: center; border-bottom: 10px solid #ffb700;}
    .glass-card {background: rgba(255,255,255,0.98); color:#000; border-radius:16px; padding:32px; box-shadow:0 12px 40px rgba(0,0,0,0.3); margin:20px 0;}
    .warning-banner {background:#8B0000; color:white; padding:30px; border-radius:12px; text-align:center; font-size:24px; margin:30px 0;}
    .recording-dot {height: 14px; width: 14px; background: #ff0033; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite;}
    }
    @keyframes pulse {0% {box-shadow: 0 0 0 0 rgba(255,0,51,0.8);} 70% {box-shadow: 0 0 0 14px rgba(255,0,51,0);} 100% {box-shadow: 0 0 0 0 rgba(255,0,51,0);}}
</style>
""", unsafe_allow_html=True)

# ========================= WARNING BANNER =========================
def show_warning(technique):
    st.markdown(f"""
    <div class='warning-banner'>
        🚨 PHISHING SIMULATION ACTIVE - EDUCATIONAL DEMO ONLY 🚨<br><br>
        <strong>Attack Technique:</strong> {technique}<br><br>
        In a real attack, the data you just entered would now be in the attacker's hands.<br>
        This demo logs NOTHING and sends nothing — it's purely to show how frighteningly realistic modern phishing has become.
    </div>
    """, unsafe_allow_html=True)
    st.balloons()

# ========================= PAGES =========================
def login_page():
    st.markdown("<div class='truist-header'><div style='font-size:100px'>🏦</div><h1>Welcome to Truist Online Banking</h1></div>", unsafe_allow_html=True)
    st.text_input("User ID")
    st.text_input("Password", type="password")
    if st.button("Log In", type="primary"):
        show_warning("Credential Harvesting via Fake Banking Login")
        st.session_state.authenticated = True
        st.session_state.otp_verified = False
        st.rerun()

def otp_page():
    st.markdown("<h1 style='text-align:center'>🔐 Security Verification</h1><p style='text-align:center'>We sent a 6-digit code to **--7842</p>", unsafe_allow_html=True)
    st.text_input("Enter code", max_chars=6)
    if st.button("Verify", type="primary"):
        show_warning("2FA/OTP Interception Attack")
        st.session_state.otp_verified = True
        st.rerun()

def dashboard():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Welcome back</h1><p style='text-align:center'><span class='recording-dot'></span> Session is being recorded for quality & training purposes</p>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Balance", "$27,451.82")
    with col2: st.metric("Available Credit", "$15,700")
    with col3: st.metric("Monthly Spending", "$3,214")
    with col4: st.metric("Savings Goal", "78%")

def cards_page():
    st.markdown("<div class='glass-card' style='text-align:center'>💳<h2>Truist One Rewards Card</h2><h3>•••• •••• •••• 7723</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Full Number"):
            st.success("5412 7537 0000 7723")
            show_warning("Payment Card Data Harvesting")
    with col3:
        if st.button("Show CVV"):
            st.info("CVV: 342")
            show_warning("CVV Harvesting via Social Engineering")

def irs_stimulus_center():
    st.markdown(f"<div style='text-align:center;padding:20px;background:white;border-radius:16px;'><img src='{irs_seal_base64}' width='130'><h1 style='color:#002868'>U.S. Department of the Treasury</h1><h2 style='color:#002868'>Internal Revenue Service</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card' style='border:6px solid #002868'><h1 style='text-align:center;color:#B31942'>$9,847.00</h1><h3 style='text-align:center'>2025 Economic Impact Payment - READY</h3></div>", unsafe_allow_html=True)
    
    with st.form("irs_form"):
        st.text_input("First Name"), st.text_input("Last Name"), st.date_input("DOB")
        st.text_input("SSN", placeholder="XXX-XX-XXXX")
        st.text_input("Routing"), st.text_input("Account")
        if st.form_submit_button("Claim Payment Now", type="primary"):
            show_warning("Government Impersonation + SSN Harvesting")

def sidebar():
    st.sidebar.image("https://raw.githubusercontent.com/ekapujiw2002/truist/main/truist-logo-white.png", width=200)
    st.sidebar.markdown("<h2 style='color:#ffb700;text-align:center'>CLIENT001</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='background:#ffb700;color:#502b85;padding:12px;border-radius:10px;text-align:center;font-weight:bold'>SECURE SESSION</p>", unsafe_allow_html=True)
    return st.sidebar.radio("Navigate", ["Dashboard", "Accounts", "Cards", "Government Stimulus Center 🇺🇸", "Transfer", "Messages"])

# ========================= MAIN =========================
if not st.session_state.authenticated:
    login_page()
elif not st.session_state.otp_verified:
    otp_page()
else:
    current = sidebar()
    if current == "Dashboard": dashboard()
    elif current == "Accounts": st.write("Accounts page — real banks show balances here")
    elif current == "Cards": cards_page()
    elif current == "Government Stimulus Center 🇺🇸": irs_stimulus_center()
    elif current == "Transfer": st.write("Real transfer page would move money")
    elif current == "Messages": st.write("Fake secure messages")

st.caption("🔒 Red Team Educational Demo • Built Nov 2025 • No data is collected • Purely for awareness")
