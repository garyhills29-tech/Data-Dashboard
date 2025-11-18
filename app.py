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

# ========================= CSS =========================
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
    .secure-badge {background: #00c853; padding: 5px 15px; border-radius: 30px; font-size: 13px; font-weight: bold;}
</style>
"""

login_css = """
<style>
    .stApp {background: linear-gradient(135deg, #0f1b3d 0%, #1a2a6c 100%); color: white;}
    .login-card {
        background: rgba(255,255,255,0.98);
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.4);
        max-width: 440px;
        margin: 80px auto;
        color: #1a1a1a;
    }
    .bank-title {font-size: 36px; font-weight: 800; color: #0f1b3d;}
</style>
"""

# ========================= LOGIN PAGE =========================
def page_login():
    st.markdown(login_css, unsafe_allow_html=True)
    st.markdown('''
    <div class="login-card">
        <div style="text-align:center; margin-bottom:35px;">
            <div style="font-size:60px;">🏦</div>
            <h1 class="bank-title">Personal Finance Hub</h1>
            <p style="color:#555; font-size:15px;">Secure Client Portal • Member FDIC</p>
        </div>
    ''', unsafe_allow_html=True)

    username = st.text_input("Username / Client ID", placeholder="client001")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    col1, col
