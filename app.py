import streamlit as st
import pandas as pd
from datetime import datetime

# ========================= CONFIG =========================
st.set_page_config(page_title="Personal Finance Hub", page_icon="🏦", layout="wide")

# ========================= CREDENTIALS =========================
VALID_USERNAME = "client001"
VALID_PASSWORD = "Secure2025Hub!"

# ========================= SESSION STATE =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "login_time" not in st.session_state:
    st.session_state.login_time = None

# ========================= GLOBAL CSS =========================
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0f1629 0%, #1a237e 100%) ; color: #e0e0e0;}
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
    .big-icon {font-size: 70px; text-align: center; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# ========================= LOGIN PAGE =========================
def login_page():
    # Temporary light theme for login only
    st.markdown("""
    <style>
        .stApp {background: linear-gradient(135deg, #0f1b3d 0%, #1a2a6c 100%); color: white;}
        .login-box {
            background: rgba(255,255,255,0.98);
            padding: 60px 50px;
            border-radius: 20px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.5);
            max-width: 480px;
            margin: 80px auto;
            text-align: center;
            color: #1a1a1a;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<div class='big-icon'>🏦</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#0f1b3d; margin:0'>Personal Finance Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666; font-size:16px'>Secure Client Portal • Member FDIC</p>", unsafe_allow_html=True)
    st.markdown("---")

    username = st.text_input("Username / Client ID", placeholder="client001")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    col1, col2 = st.columns([1,1])
    with col1: st.checkbox("Remember me")
    with col2: st.markdown("<div style='text-align:right'><small><a href='#'>Forgot password?</a></small></div>", unsafe_allow_html=True)

    if st.button("🔐 Sign In Securely", type="primary"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.login_time = datetime.now()
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.error("Account locked for security. Contact support.")
            else:
                st.error(f"Invalid credentials — Attempt {st.session_state.attempts}/3")

    st.markdown("</div>", unsafe_allow_html=True)

# ========================= DASHBOARD PAGES =========================
def dashboard():
    st.markdown("<h1 style='text-align:center; color:#00c4ff;'>Secure Dashboard</h1>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", "$27,451.82", "+$5,200")
    with c2: st.metric("Available Credit", "$18,500")
    with c3: st.metric("Monthly Spending", "$3,214", "-12%")
    with c4: st.metric("Savings Goal", "78%", "+5%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Recent Transactions")
        df = pd.DataFrame({
            "Date": ["Nov 18", "Nov 17", "Nov 16", "Nov 15"],
            "Description": ["Salary Deposit", "Amazon", "Grocery", "Netflix"],
            "Amount": ["+$5,200", "-$187", "-$99", "-$16"]
        })
        def color_amt(val): return f"color: {'lime' if '+' in val else 'red'}"
        styled = df.style.map(color_amt, subset=["Amount"])
        st.dataframe(styled, hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Balance Trend")
        trend = pd.DataFrame({"Date": ["Nov 1", "Nov 5", "Nov 9", "Nov 13", "Nov 17"], "Balance": [22451, 22890, 23120, 23780, 27451]})
        st.line_chart(trend.set_index("Date"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def accounts():
    st.markdown("<h1 style='text-align:center; color:#00c4ff;'>My Accounts</h1>", unsafe_allow_html=True)
    accounts_list = [
        ("Premier Checking • ****2847", "$12,340.50"),
        ("High-Yield Savings • ****5901", "$14,911.32"),
        ("Platinum Credit Card • ****7723", "$2,300 / $18,000"),
    ]
    for name, bal in accounts_list:
        st.markdown(f"<div class='glass-card'><h3>{name}</h3><h2>{bal}</h2></div>", unsafe_allow_html=True)

def transfer():
    st.markdown("<h1 style='text-align:center; color:#00c4ff;'>Transfer Funds</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.radio("Transfer Type", ["Between My Accounts", "To Another Bank", "Zelle"])
    col1, col2 = st.columns(2)
    with col1: st.selectbox("From Account", ["Premier Checking ****2847", "Savings ****5901"])
    with col2: st.selectbox("To Account", ["Savings ****5901", "Chase ****1234 (External)"])
    amount = st.number_input("Amount ($)", min_value=0.01, step=10.0)
    if st.button("Review & Send"):
        st.success(f"${amount:,.2f} transfer completed successfully!")
        st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

def messages():
    st.markdown("<h1 style='text-align:center; color:#00c4ff;'>Secure Messages</h1>", unsafe_allow_html=True)
    msgs = [
        "Your November statement is ready",
        "New login detected from Chrome on Windows",
        "Your savings rate has increased to 4.75% APY",
    ]
    for m in msgs:
        st.markdown(f"<div class='glass-card'><h4>🟢 {m}</h4></div>", unsafe_allow_html=True)

# ========================= SIDEBAR (only after login) =========================
def show_sidebar():
    st.sidebar.image("https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80", width=100)
    st.sidebar.markdown(f"<h2 style='color:#00c4ff; text-align:center'>{VALID_USERNAME.upper()}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='secure-badge' style='text-align:center'>SECURE SESSION</p>", unsafe_allow_html=True)
    if st.session_state.login_time:
        st.sidebar.caption(f"Logged in {st.session_state.login_time.strftime('%I:%M %p')}")

    page = st.sidebar.radio("Navigate", [
        "🏠 Dashboard",
        "💳 Accounts",
        "⇄ Transfer Funds",
        "✉ Messages"
    ])

    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

    return page

# ========================= MAIN LOGIC =========================
if not st.session_state.authenticated:
    login_page()
else:
    current_page = show_sidebar()

    if "Accounts" in current_page:
        accounts()
    elif "Transfer" in current_page:
        transfer()
    elif "Messages" in current_page:
        messages()
    else:
        dashboard()
