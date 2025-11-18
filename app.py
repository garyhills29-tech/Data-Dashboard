import streamlit as st
import pandas as pd
from datetime import datetime

# ========================= CONFIG =========================
st.set_page_config(page_title="Personal Finance Hub", page_icon="🏦", layout="wide")

# Credentials
VALID_USERNAME = "client001"
VALID_PASSWORD = "Secure2025Hub!"

# Session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "login_time" not in st.session_state:
    st.session_state.login_time = None

# ========================= PREMIUM CSS =========================
dashboard_css = """
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
    .stButton>button {
        background: linear-gradient(90deg, #00c4ff, #007bff);
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 600;
    }
    .stButton>button:hover {transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,124,255,0.5);}
    .secure-badge {background: #00c853; padding: 5px 15px; border-radius: 30px; font-size: 13px; font-weight: bold;}
    .page-icon {font-size: 42px; margin-bottom: 10px;}
</style>
"""

login_css = """
<style>
    .stApp {background: linear-gradient(135deg, #0f1b3d 0%, #1a2a6c 100%); color: white;}
    .login-card {background: rgba(255,255,255,0.98); padding: 50px; border-radius: 20px; 
                 box-shadow: 0 25px 50px rgba(0,0,0,0.4); max-width: 440px; margin: 80px auto; color: #1a1a1a;}
    .bank-title {font-size: 36px; font-weight: 800; color: #0f1b3d;}
    .stButton>button {width: 100%; background: linear-gradient(90deg, #0066cc, #004999); 
                      color: white; border-radius: 14px; padding: 16px; font-size:19px; font-weight:600;}
</style>
"""

# ========================= PAGES =========================
def page_login():
    st.markdown(login_css, unsafe_allow_html=True)
    st.markdown("""
    <div class="login-card">
        <div style="text-align:center; margin-bottom:35px;">
            <div class="page-icon">🏦</div>
            <h1 class="bank-title">Personal Finance Hub</h1>
            <p style="color:#555; font-size:15px;">Secure Client Portal • Member FDIC</p>
        </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username / Client ID", placeholder="client001")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    col1, col2 = st.columns([1.5,1])
    with col1: st.checkbox("Stay signed in")
    with col2: st.markdown("<div style='text-align:right'><a href='#'>Forgot?</a></div>", unsafe_allow_html=True)

    if st.button("Sign In Securely"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.login_time = datetime.now()
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.error("Account locked — contact 1-800-555-0199")
            else:
                st.error(f"Invalid credentials • Attempt {st.session_state.attempts}/3")

def page_dashboard():
    st.markdown(dashboard_css, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#00c4ff;'>Secure Dashboard</h1>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Balance", "$27,451.82", "+$5,200")
    with col2: st.metric("Available Credit", "$18,500", "+$2,300")
    with col3: st.metric("Monthly Spending", "$3,214", "-12%")
    with col4: st.metric("Savings Rate", "78%", "+5%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Recent Transactions")
        df = pd.DataFrame({
            "Date": ["Nov 18", "Nov 17", "Nov 16", "Nov 15"],
            "Description": ["Salary Deposit", "Amazon", "Supermarket", "Netflix"],
            "Amount": ["+$5,200", "-$187", "-$99", "-$16"]
        })
        st.dataframe(df.style.applymap(lambda x: "color: lime" if x.startswith('+') else "color: red", subset=["Amount"]),
                     hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Balance Trend")
        trend = pd.DataFrame({"Date": ["Nov 1", "Nov 5", "Nov 9", "Nov13", "Nov17"], "Balance": [22451, 22890, 23120, 23780, 27451]})
        st.line_chart(trend.set_index("Date"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def page_accounts():
    st.markdown(dashboard_css, unsafe_allow_html=True)
    st.markdown("<div class='page-icon' style='text-align:center'>💳</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#00c4ff;'>My Accounts</h1>", unsafe_allow_html=True)

    accounts = [
        {"type": "Premier Checking", "number": "**** 2847", "balance": "$12,340.50", "available": "$12,340.50"},
        {"type": "High-Yield Savings", "number": "**** 5901", "balance": "$14,911.32", "available": "$14,911.32"},
        {"type": "Credit Card Platinum", "number": "**** 7723", "balance": "$2,300.00", "available": "$15,700 / $18,000"},
    ]

    for acc in accounts:
        st.markdown(f"""
        <div class='glass-card'>
