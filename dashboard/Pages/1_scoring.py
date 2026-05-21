# dashboard/pages/1_scoring.py
import streamlit as st
import requests

st.set_page_config(page_title="Fraud Scoring", page_icon="🎯", layout="wide")

st.title("🎯 Fraud Scoring")
st.markdown("CDR data enter karo — fraud probability aur risk level milega.")
st.markdown("---")

# CDR Input Form
with st.form("cdr_form"):
    st.subheader("📋 CDR Input")

    col1, col2, col3 = st.columns(3)

    with col1:
        account_length = st.number_input("Account Length (days)", value=82.0)
        vmail_message = st.number_input("VMail Messages", value=0.0)
        day_mins = st.number_input("Day Minutes", value=300.3)
        day_calls = st.number_input("Day Calls", value=109.0)
        day_charge = st.number_input("Day Charge", value=51.05)

    with col2:
        eve_mins = st.number_input("Evening Minutes", value=181.0)
        eve_calls = st.number_input("Evening Calls", value=100.0)
        eve_charge = st.number_input("Evening Charge", value=15.39)
        night_mins = st.number_input("Night Minutes", value=270.1)
        night_calls = st.number_input("Night Calls", value=73.0)

    with col3:
        night_charge = st.number_input("Night Charge", value=12.15)
        intl_mins = st.number_input("International Minutes", value=11.7)
        intl_calls = st.number_input("International Calls", value=4.0)
        intl_charge = st.number_input("International Charge", value=3.16)
        custserv_calls = st.number_input("Customer Service Calls", value=0.0)

    submitted = st.form_submit_button("🔍 Check Fraud Score", use_container_width=True)

# API Call
if submitted:
    payload = {
        "Account_Length": account_length,
        "VMail_Message": vmail_message,
        "Day_Mins": day_mins,
        "Day_Calls": day_calls,
        "Day_Charge": day_charge,
        "Eve_Mins": eve_mins,
        "Eve_Calls": eve_calls,
        "Eve_Charge": eve_charge,
        "Night_Mins": night_mins,
        "Night_Calls": night_calls,
        "Night_Charge": night_charge,
        "Intl_Mins": intl_mins,
        "Intl_Calls": intl_calls,
        "Intl_Charge": intl_charge,
        "CustServ_Calls": custserv_calls
    }

    try:
        with st.spinner("Analyzing CDR data..."):
            response = requests.post("http://localhost:8000/score", json=payload)

        if response.status_code == 200:
            result = response.json()

            st.markdown("---")
            st.subheader("📊 Results")

            # Risk level color
            risk_colors = {
                "LOW": "🟢", "MEDIUM": "🟡",
                "HIGH": "🟠", "CRITICAL": "🔴"
            }
            risk_icon = risk_colors.get(result['risk_level'], "⚪")

            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Fraud Probability", f"{result['fraud_percentage']}%")
            col2.metric("Risk Level", f"{risk_icon} {result['risk_level']}")
            col3.metric("Is Fraud", "✅ YES" if result['is_fraud'] else "❌ NO")

            # Message
            if result['is_fraud']:
                st.error(f"⚠️ {result['message']}")
            else:
                st.success(f"✅ {result['message']}")

            # Top features
            st.subheader("🔑 Top Contributing Features")
            for feature, value in result['top_features'].items():
                st.progress(min(float(value) / 500, 1.0), text=f"{feature}: {value}")

        else:
            st.error(f"API Error: {response.status_code}")

    except Exception as e:
        st.error(f"❌ API Not Running — Start docker-compose first\n\n{e}")