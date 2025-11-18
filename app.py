import streamlit as st
import requests
from datetime import datetime
import random, time

# ========================= CONFIG =========================
st.set_page_config(page_title="Truist Online Banking - Educational Demo", page_icon="🏦", layout="wide")

# ======================= STATE =========================
for key in ["authenticated", "otp_verified"]:
    if key not in st.session_state:
        st.session_state[key] = False

# Fake crypto holdings (for show)
if "crypto" not in st.session_state:
    st.session_state.crypto = {
        "BTC": 0.0420,
        "ETH": 3.21,
        "SOL": 42.0,
        "DOGE": 1337.0,
        "PEPE": 69696969.0,
        "GROK": 20250.0
    }

# ======================= LIVE CRYPTO PRICES =========================
@st.cache_data(ttl=15)
def get_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        ids = "bitcoin,ethereum,solana,dogecoin,pepe,grok"
        r = requests.get(f"{url}?ids={ids}&vs_currencies=usd&include_24hr_change=true", timeout=10).json()
        return {
            "BTC": {"price": r["bitcoin"]["usd"], "change": r["bitcoin"]["usd_24h_change"]},
            "ETH": {"price": r["ethereum"]["usd"], "change": r["ethereum"]["usd_24h_change"]},
            "SOL": {"price": r["solana"]["usd"], "change": r["solana"]["usd_24h_change"]},
            "DOGE": {"price": r["dogecoin"]["usd"], "change": r["dogecoin"]["usd_24h_change"]},
            "PEPE": {"price": r["pepe"]["usd"], "change": r["pepe"]["usd_24h_change"]},
            "GROK": {"price": r["grok"]["usd"], "change": r["grok"]["usd_24h_change"]},
        }
    except:
        return {k: {"price": 0, "change": 0} for k in st.session_state.crypto}

prices = get_prices()

# ======================= CSS =========================
irs_seal_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAABUp9QnAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LjE2Njc5MiwgMjAyMS8wMS8xNC0wODowNzoyMyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjAgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZCM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QzNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjJERjY4RjZBM0YxMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoyREY2OEY2QjNGExMTFFM0I4QjBCMEJBQjBCMDhCMEJCQyIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PtD/4AAAABJRU5ErkJggg=="

st.markdown(f"""
<style>
    .stApp {{background: #502b85;}}
    .truist-header {{background: #502b85; padding: 20px; text-align: center; border-bottom: 10px solid #ffb700;}}
    .glass-card {{background: rgba(255,255,255,0.98); color:#000; border-radius:16px; padding:32px; box-shadow:0 12px 40px rgba(0,0,0,0.3); margin:20px 0;}}
    .warning-banner {{background:#8B0000; color:white; padding:30px; border-radius:12px; text-align:center; font-size:24px; margin:30px 0;}}
    .crypto-row {{display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee;}}
    .price-up {{color: #00ff9d;}} .price-down {{color: #ff006e;}}
    .recording-dot {{height: 14px; width: 14px; background: #ff0033; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite;}}
    @keyframes pulse {{0% {{box-shadow: 0 0 0 0 rgba(255,0,51,0.8);}} 70% {{box-shadow: 0 0 0 14px rgba(255,0,51,0);}} 100% {{box-shadow: 0 0 0 0 rgba(255,0
