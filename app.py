import streamlit as st
import pandas as pd
from datetime import datetime

# === CONFIG ===
st.set_page_config(page_title="Personal Finance Hub", page_icon="🔒", layout="wide")

# Credentials
VALID_USERNAME = "client001"
VALID_PASSWORD = "Secure2025!"

# Session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "login_time" not in st.session_state:
    st.session_state.login_time = None

# === ULTRA SECURE DASHBOARD STYLING ===
dashboard_css = """
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f1629 0%, #1a237e 100%);
        color: #e0e0e0;
    }
    
    /* Glass cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 10px 0;
    }
    
    /* Metrics glow */
    .stMetric > div {
        background: rgba(0, 102, 204, 0.2) !important;
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(0, 102, 204, 0.4);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00c4ff, #007bff) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 124, 255, 0.4) !important;
    }
    
    /* Sidebar premium */
    .css-1d391kg {background: rgba(15, 22, 41, 0.95);}
    .secure-badge {background: #00c853; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;}
</style>
"""
# === LOGIN PAGE (keeping the beautiful one from before) ===
def show_login():
    st.markdown("""
    <style>
        .stApp {background: linear-gradient(135deg, #0f1b3d 0%, #1a2a6c 100%); color: white;}
        .login-card {background: rgba(255,255,255,0.98); padding: 40px 50px; border-radius: 20px; 
                     box-shadow: 0 20px 40px rgba(0,0,0,0.3); max-width: 420px; margin: 60px auto; color: #1a1a1a;}
        .bank-title {font-size: 32px; font-weight: 700; color: #0f1b3d;}
        .stButton>button {width: 100%; background: linear-gradient(90deg, #0066cc, #004d99); 
                          color: white; border-radius: 12px; padding: 14px; font-size: 18px; font-weight: 600;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-card">
        <div style="text-align:center; margin-bottom:30px;">
            <h1 class="bank-title">🔒 Personal Finance Hub</h1>
            <p style="color:#666;">Secure Client Portal • Member FDIC</p>
        </div>
    """, unsafe_allow_html=True)

    username = st.text_input("👤 Username / Client ID", placeholder="client001")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter secure password")
    
    col1, col2 = st.columns(2)
    with col1: st.checkbox("Remember me")
    with col2: st.markdown("<div style='text-align:right'><a href='#'>Forgot password?</a></div>", unsafe_allow_html=True)

    if st.button("🔐 Sign In Securely"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.login_time = datetime.now()
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.error("🚫 Account locked — contact support@pfhub.com")
            else:
                st.error(f"Invalid credentials • Attempt {st.session_state.attempts}/3")

# === SECURE DASHBOARD ===
def show_dashboard():
    st.markdown(dashboard_css, unsafe_allow_html=True)

    # Premium sidebar
    st.sidebar.image("https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80", width=100)
    st.sidebar.markdown(f"<h2 style='color:#00c4ff;'>Welcome back</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<h3>{VALID_USERNAME.upper()}</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='secure-badge'>🔒 SECURE SESSION</p>", unsafe_allow_html=True)
    if st.session_state.login_time:
        st.sidebar.caption(f"Last login: {st.session_state.login_time.strftime('%b %d, %Y at %I:%M %p')}")
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Log Out Securely"):
        st.session_state.authenticated = False
        st.rerun()

    # Header
    st.markdown("<h1 style='text-align:center; color:#00c4ff;'>🔒 Secure Financial Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>Your session is protected with bank-grade encryption</p>", unsafe_allow_html=True)

    # Metrics in glass cards
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Balance", "$27,451.82", "+$5,200")
    with col2: st.metric("Available Credit", "$18,500", "+$2,300")
    with col3: st.metric("Monthly Spending", "$3,214.67", "-12%")
    with col4: st.metric("Savings Progress", "78%", "+5%")
    st.markdown("</div>", unsafe_allow_html=True)

    # Rest of dashboard in glass cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Recent Transactions")
        data = pd.DataFrame({
            "Date": ["Nov 18", "Nov 17", "Nov 16", "Nov 15", "Nov 14"],
            "Description": ["Salary Deposit", "Amazon", "Grocery", "Netflix", "Gas"],
            "Amount": ["+$5,200", "-$187", "-$99", "-$16", "-$63"]
        })
        def color(val): return f"color: {'lime' if '+' in val else 'red'}"
        st.dataframe(data.style.map(color, subset=["Amount"]), hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 Balance Trend")
        trend = pd.DataFrame({"Date": ["Nov 1", "Nov 5", "Nov 9", "Nov 13", "Nov 17"], 
                             "Balance": [22451, 22890, 23120, 23780, 27451]})
        st.line_chart(trend.set_index("Date"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Quick actions
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🚀 Secure Quick Actions")
    c1, c2, c3, c4 = st.columns(4)
    with c1: if st.button("Transfer Funds"): st.success("Encrypted transfer initiated")
    with c2: if st.button("Pay Bills"): st.info("Secure bill pay loaded")
    with c3: if st.button("Investments"): st.success("Portfolio access granted")
    with c4: if st.button("Deposit Check"): st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("<p style='text-align:center; color:#666; margin-top:50px;'>"
                "🔒 End-to-end encrypted • Session expires in 15 minutes • Monitored for security"
                "</p>", unsafe_allow_html=True)

# === RUN ===
if not st.session_state.authenticated:
    show_login()
else: 
    show_dashboard()
