import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="Personal Finance Hub",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium banking look
st.markdown("""
<style>
    .css-1d391kg {padding-top: 1rem; padding-bottom: 3rem;}
    .css-1v0mbdj {font-size: 1.8rem !important;}
    .stMetric {background-color: #f0f2f6; padding: 1rem; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# Sidebar - clean login demo
st.sidebar.header("🔐 Secure Access")
user_name = st.sidebar.text_input("Full Name", value="Alexander Hamilton")
user_id = st.sidebar.text_input("Client ID", value="HAM-1789-US")
if st.sidebar.button("Access Dashboard"):
    st.sidebar.success(f"Welcome back, {user_name.split()[0]}!")

st.sidebar.markdown("---")
st.sidebar.caption("Personal Finance Hub © 2025 | Demo Version")

# Main title
st.title("💰 Personal Finance Hub")
st.markdown("#### Your Complete Financial Overview")

# Key metrics
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

# Recent transactions
st.subheader("📊 Recent Activity")

data = pd.DataFrame({
    "Date": ["2025-11-18", "2025-11-17", "2025-11-16", "2025-11-15", "2025-11-14", "2025-11-13"],
    "Description": [
        "Direct Deposit - Employer",
        "Amazon Purchase",
        "Whole Foods Market",
        "Netflix Subscription",
        "Shell Gas Station",
        "Starbucks Coffee"
    ],
    "Category": ["Income", "Shopping", "Groceries", "Entertainment", "Transport", "Dining"],
    "Amount": ["+$5,200.00", "-$187.34", "-$98.72", "-$15.99", "-$62.50", "-$8.75"]
})

# Color coding
def color_amount(val):
    color = "green" if val.startswith("+") else "red"
    return f"color: {color}"

styled_data = data.style.map(color_amount, subset=["Amount"])
st.dataframe(styled_data, use_container_width=True, hide_index=True)

# Charts side by side
col1, col2 = st.columns(2)
with col1:
    st.subheader("Spending by Category")
    category_data = pd.DataFrame({
        "Category": ["Shopping", "Groceries", "Dining", "Transport", "Entertainment"],
        "Amount": [187, 99, 145, 63, 16]
    })
    st.bar_chart(category_data.set_index("Category"))

with col2:
    st.subheader("Balance Trend")
    trend_data = {
        "Date": ["Nov 1", "Nov 3", "Nov 5", "Nov 7", "Nov 9", "Nov 11", "Nov 13", "Nov 15", "Nov 17"],
        "Balance": [22451, 22890, 22560, 23120, 22980, 23350, 23780, 24120, 27451]
    }
    trend = pd.DataFrame(trend_data)
    st.line_chart(trend.set_index("Date"))

# Quick actions
st.markdown("---")
st.subheader("🚀 Quick Actions")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("Transfer Funds"):
        st.success("Transfer module ready")
with c2:
    if st.button("Pay Bills"):
        st.info("Bill payment center")
with c3:
    if st.button("Investment Portfolio"):
        st.success("Portfolio overview loaded")
with c4:
    if st.button("Deposit Check"):
        st.balloons()
# Quick actions
st.markdown("---")
st.subheader("🚀 Quick Actions")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("Transfer Funds"):
        st.success("Transfer initiated")
with c2:
    if st.button("Pay Bills"):
        st.info("Opening bill payment center")
with c3:
    if st.button("View Investments"):
        st.success("Portfolio loaded")
with c4:
    if st.button("Deposit Check"):
        st.balloons()
# Footer
st.markdown("---")

st.caption("This is a demonstration dashboard • All data is simulated for illustration purposes only.")

