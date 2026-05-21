import streamlit as st
import requests

st.set_page_config(
    page_title= "Telecom Fraud Detection",
     page_icon="🔍",
    layout="wide"
)
st.title("🔍 Telecom Fraud Detection Platform")
st.markdown("---")
st.markdown("""
## Welcome

This platform analyzes **Call Detail Records (CDR)** to identify fraudulent callers
using Machine Learning and Generative AI.

| Page | Description |
|------|-------------|
| 🎯 Fraud Scoring | CDR data → fraud probability + risk level |
| 🧠 AI Explanation | LLM-powered explanation for flagged numbers |
| 💬 RAG Chatbot | Query TRAI regulations knowledge base |
| 📊 Model Performance | SHAP plots and model comparison |
""")

st.sidebar.success("Select a page above.")
st.sidebar.markdown("---")
st.sidebar.markdown("**API status")

try:
    r = requests.get("http://localhost:8000/")
    if r.status_code ==200:
        st.sidebar.success("API Connected")
    else:
        st.sidebar.error("API Error")
except:
    st.sidebar.error("API Not Running")
    