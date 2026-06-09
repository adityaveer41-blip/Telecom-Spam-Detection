import streamlit as st
import requests

st.set_page_config(page_title="Fraud Scoring", page_icon="🎯", layout="wide")

COMMON_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.8rem; }
.stApp {
    background-color: #080d18;
    background-image: radial-gradient(ellipse at 15% 60%, rgba(220,38,38,0.04) 0%, transparent 45%),
        linear-gradient(rgba(255,255,255,0.012) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.012) 1px, transparent 1px);
    background-size: 100% 100%, 36px 36px, 36px 36px;
}
section[data-testid="stSidebar"] { background: #060b14 !important; border-right: 1px solid #1a2640; min-width: 230px !important; }
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] { padding: 0.45rem 1rem !important; border-radius: 7px !important; font-size: 0.87rem !important; font-weight: 500 !important; color: #8ab4d4 !important; white-space: nowrap !important; transition: background 0.15s, color 0.15s; }
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover,
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] { background: rgba(220,38,38,0.12) !important; color: #f87171 !important; }
h1 { color: #dce8f5 !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
h2, h3 { color: #b0c8e0 !important; font-weight: 600 !important; }
p, .stMarkdown p { color: #4a6a8a !important; }
hr { border-color: #1a2e48 !important; }
div[data-testid="stNumberInput"] input { background: #0c1628 !important; border: 1px solid #1e3050 !important; border-radius: 7px !important; color: #c0d4e8 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.85rem !important; }
div[data-testid="stNumberInput"] input:focus { border-color: #f87171 !important; box-shadow: 0 0 0 2px rgba(248,113,113,0.15) !important; }
div[data-testid="stNumberInput"] label { color: #6a8aaa !important; font-size: 0.8rem !important; font-weight: 500 !important; }
div[data-testid="stFormSubmitButton"] button { background: linear-gradient(135deg, #dc2626, #b91c1c) !important; border: none !important; color: #fff !important; font-weight: 600 !important; border-radius: 8px !important; font-family: 'Inter', sans-serif !important; }
div[data-testid="stFormSubmitButton"] button:hover { opacity: 0.88 !important; }
div[data-testid="stMetric"] { background: #0c1628 !important; border: 1px solid #1e3050 !important; border-radius: 10px !important; padding: 0.9rem 1.1rem !important; }
div[data-testid="stMetricLabel"] { color: #4a6a8a !important; font-size: 0.78rem !important; }
div[data-testid="stMetricValue"] { color: #dce8f5 !important; font-weight: 700 !important; }
div[data-testid="stAlert"] { border-radius: 8px !important; }
div[data-testid="stProgressBar"] > div { background: linear-gradient(90deg, #dc2626, #f87171) !important; border-radius: 4px !important; }
div[data-testid="stProgressBar"] { background: #1a2e48 !important; border-radius: 4px !important; }
/* Form container */
div[data-testid="stForm"] { background: #0c1628 !important; border: 1px solid #1e3050 !important; border-radius: 12px !important; padding: 1.2rem !important; }
</style>"""

st.markdown(COMMON_CSS, unsafe_allow_html=True)

st.title("🎯 Fraud Scoring")
st.markdown("CDR data enter karo — fraud probability aur risk level milega.")
st.markdown("---")

with st.form("cdr_form"):
    st.subheader("CDR Input")
    col1, col2, col3 = st.columns(3)
    with col1:
        account_length = st.number_input("Account Length (days)", value=82.0)
        vmail_message  = st.number_input("VMail Messages", value=0.0)
        day_mins       = st.number_input("Day Minutes", value=300.3)
        day_calls      = st.number_input("Day Calls", value=109.0)
        day_charge     = st.number_input("Day Charge", value=51.05)
    with col2:
        eve_mins    = st.number_input("Evening Minutes", value=181.0)
        eve_calls   = st.number_input("Evening Calls", value=100.0)
        eve_charge  = st.number_input("Evening Charge", value=15.39)
        night_mins  = st.number_input("Night Minutes", value=270.1)
        night_calls = st.number_input("Night Calls", value=73.0)
    with col3:
        night_charge   = st.number_input("Night Charge", value=12.15)
        intl_mins      = st.number_input("International Minutes", value=11.7)
        intl_calls     = st.number_input("International Calls", value=4.0)
        intl_charge    = st.number_input("International Charge", value=3.16)
        custserv_calls = st.number_input("Customer Service Calls", value=0.0)
    submitted = st.form_submit_button("🔍 Check Fraud Score", use_container_width=True)

if submitted:
    payload = {
        "Account_Length": account_length, "VMail_Message": vmail_message,
        "Day_Mins": day_mins, "Day_Calls": day_calls, "Day_Charge": day_charge,
        "Eve_Mins": eve_mins, "Eve_Calls": eve_calls, "Eve_Charge": eve_charge,
        "Night_Mins": night_mins, "Night_Calls": night_calls, "Night_Charge": night_charge,
        "Intl_Mins": intl_mins, "Intl_Calls": intl_calls, "Intl_Charge": intl_charge,
        "CustServ_Calls": custserv_calls
    }
    try:
        with st.spinner("Analyzing CDR data..."):
            response = requests.post("http://localhost:8000/score", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.markdown("---")
            st.subheader("📊 Results")
            risk_colors = {"LOW":"🟢","MEDIUM":"🟡","HIGH":"🟠","CRITICAL":"🔴"}
            risk_icon = risk_colors.get(result['risk_level'], "⚪")
            col1, col2, col3 = st.columns(3)
            col1.metric("Fraud Probability", f"{result['fraud_percentage']}%")
            col2.metric("Risk Level", f"{risk_icon} {result['risk_level']}")
            col3.metric("Is Fraud", "✅ YES" if result['is_fraud'] else "❌ NO")
            if result['is_fraud']:
                st.error(f"⚠️ {result['message']}")
            else:
                st.success(f"✅ {result['message']}")
            st.subheader("🔑 Top Contributing Features")
            for feature, value in result['top_features'].items():
                st.progress(min(float(value)/500, 1.0), text=f"{feature}: {value}")
        else:
            st.error(f"API Error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ API Not Running — Start docker-compose first\n\n{e}")
