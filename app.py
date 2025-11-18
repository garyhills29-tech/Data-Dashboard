import streamlit as st
import pandas as pd
import numpy as np

# === CONFIG ===
st.set_page_config(page_title="Personal Finance Hub", page_icon="🏦", layout="centered")

# Hardcoded credentials (change these to whatever you want)
VALID_USERNAME = "client001"
VALID_PASSWORD = "Secure2025!"

# === SESSION STATE ===
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# === LOGIN PAGE ===
def show_login():
    st.markdown("""
    <style>
        .login-container {max-width: 400px; margin: auto; padding-top: 8rem;}
        .stButton>button {width: 100%; background-color: #0066cc; color: white;}
    </style>
    """, unsafe_allow_html=True)

    st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_column_width=True)
    st.markdown("<h1 style='text-align: center;'>🏦 Personal Finance Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Secure Client Portal</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        username = st.text_input("Username / Client ID", placeholder="e.g. client001")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Sign In", type="primary"):
                if username == VALID_USERNAME and password == VALID_PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.attempts = 0
                    st.rerun()
                else:
                    st.session_state.attempts += 1
                    if st.session_state.attempts >= 3:
                        st.error("⚠ Account locked due to multiple failed attempts. Contact support.")
                    else:
                        st.error(f"Invalid credentials. Attempt {st.session_state.attempts}/3")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.8rem; color: gray;'>"
                    "Forgot password? • Use of this system constitutes consent to monitoring</p>", unsafe_allow_html=True)

# === MAIN DASHBOARD (only shown after login) ===
def show_dashboard():
    st.sidebar.header(f"🔐 Welcome, {VALID_USERNAME}")
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

    st.title("🏦 Personal Finance Hub")
    st.markdown("#### Your Complete Financial Overview")

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

# === RUN APP ===
if not st.session_state.authenticated:
    show_login()
else:
    show_dashboard()
