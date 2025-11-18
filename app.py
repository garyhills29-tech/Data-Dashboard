import streamlit as st
import pandas as pd

# === CONFIG ===
st.set_page_config(page_title="Personal Finance Hub • Sign In", page_icon="🏦", layout="centered")

# Hardcoded credentials (change if you want)
VALID_USERNAME = "client001"
VALID_PASSWORD = "Secure2025!"

# Session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# === PREMIUM LOGIN PAGE ===
def show_login():
    st.markdown("""
    <style>
        /* Full background */
        .stApp {background: linear-gradient(135deg, #0f1b3d 0%, #1a2a6c 100%); color: white;}
        
        /* Center card */
        .login-card {
            background: rgba(255, 255, 255, 0.98);
            padding: 40px 50px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            max-width: 420px;
            margin: 60px auto;
            color: #1a1a1a;
        }
        .logo-header {text-align: center; margin-bottom: 30px;}
        .bank-title {font-size: 32px; font-weight: 700; color: #0f1b3d; margin: 0;}
        .bank-subtitle {color: #666; font-size: 14px; margin-top: 8px;}
        
        /* Inputs */
        .stTextInput > div > div > input {
            border-radius: 12px !important;
            border: 1px solid #ddd !important;
            padding: 14px !important;
            font-size: 16px !important;
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #0066cc, #004d99);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 14px;
            font-size: 18px;
            font-weight: 600;
            margin-top: 20px;
            transition: all 0.3s;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #0055aa, #003d80);
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,102,204,0.3);
        }
        .extra-links {text-align: center; margin-top: 25px; font-size: 14px;}
        .extra-links a {color: #0066cc; text-decoration: none;}
    </style>
    """, unsafe_allow_html=True)

    # Login Card
    st.markdown("""
    <div class="login-card">
        <div class="logo-header">
            <h1 class="bank-title">🏦 Personal Finance Hub</h1>
            <p class="bank-subtitle">Secure Client Portal • Member FDIC</p>
        </div>
    """, unsafe_allow_html=True)

    username = st.text_input("👤 Username / Client ID", placeholder="client001")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter your secure password")
    
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Remember me")
    with col2:
        st.markdown("<div style='text-align: right;'><a href='#'>Forgot password?</a></div>", unsafe_allow_html=True)

    if st.button("🔐 Sign In Securely"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.attempts = 0
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.error("🚫 Account temporarily locked. Contact support at support@pfhub.com")
            else:
                st.error(f"Invalid credentials • Attempt {st.session_state.attempts} of 3")

    st.markdown("""
        <div class="extra-links">
            <p>Need help? Call 1-800-555-0199<br>
            <small>© 2025 Personal Finance Hub. All rights reserved.</small></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# === DASHBOARD (same as before) ===
def show_dashboard():
    st.sidebar.success(f"✓ Logged in as {VALID_USERNAME}")
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

    st.title("🏦 Personal Finance Hub")
    st.markdown("#### Welcome back! Here's your financial overview")

    # [Rest of your dashboard code — metrics, table, charts, quick actions — paste from previous working version here]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Balance", "$27,451.82", "+$5,200 this month")
    with col2:
        st.metric("Available Credit", "$18,500.00", "$2,300 used")
    with col3:
        st.metric("Monthly Spending", "$3,214.67", "-12% vs last month")
    with col4:
        st.metric("Savings Goal Progress", "78%", "+5%")

    st.markdown("---")
    st.subheader("📊 Recent Activity")
    data = pd.DataFrame({
        "Date": ["2025-11-18", "2025-11-17", "2025-11-16", "2025-11-15", "2025-11-14"],
        "Description": ["Direct Deposit - Employer", "Amazon Purchase", "Whole Foods", "Netflix Subscription", "Shell Gas Station"],
        "Amount": ["+$5,200.00", "-$187.34", "-$98.72", "-$15.99", "-$62.50"]
    })
    def color_amount(val):
        color = "green" if "+" in val else "red"
        return f"color: {color}"
    st.dataframe(data.style.map(color_amount, subset=["Amount"]), use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Spending by Category")
        cat = pd.DataFrame({"Category": ["Shopping", "Groceries", "Dining", "Transport"], "Amount": [187, 99, 145, 63]})
        st.bar_chart(cat.set_index("Category"))
    with col2:
        st.subheader("Balance Trend")
        trend = pd.DataFrame({"Date": ["Nov 1", "Nov 5", "Nov 9", "Nov 13", "Nov 17"], "Balance": [22451, 22890, 23120, 23780, 27451]})
        st.line_chart(trend.set_index("Date"))

    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Transfer Funds"): st.success("Transfer initiated")
    with c2:
        if st.button("Pay Bills"): st.info("Opening bill payment center")
    with c3:
        if st.button("View Investments"): st.success("Portfolio loaded")
    with c4:
        if st.button("Deposit Check"): st.balloons()

# === RUN ===
if not st.session_state.authenticated:
    show_login()
else:
    show_dashboard()
