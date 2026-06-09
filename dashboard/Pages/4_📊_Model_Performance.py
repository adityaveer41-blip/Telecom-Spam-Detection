import streamlit as st
import os

st.set_page_config(page_title="Model Performance", page_icon="📊", layout="wide")

COMMON_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.8rem; }
.stApp { background-color: #080d18; background-image: radial-gradient(ellipse at 15% 60%, rgba(220,38,38,0.04) 0%, transparent 45%), linear-gradient(rgba(255,255,255,0.012) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.012) 1px, transparent 1px); background-size: 100% 100%, 36px 36px, 36px 36px; }
section[data-testid="stSidebar"] { background: #060b14 !important; border-right: 1px solid #1a2640; min-width: 230px !important; }
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] { padding: 0.45rem 1rem !important; border-radius: 7px !important; font-size: 0.87rem !important; font-weight: 500 !important; color: #8ab4d4 !important; white-space: nowrap !important; transition: background 0.15s, color 0.15s; }
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover, section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] { background: rgba(220,38,38,0.12) !important; color: #f87171 !important; }
h1 { color: #dce8f5 !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
h2, h3 { color: #b0c8e0 !important; font-weight: 600 !important; }
p, .stMarkdown p { color: #4a6a8a !important; }
hr { border-color: #1a2e48 !important; }
div[data-testid="stTabs"] button { color: #4a6a8a !important; font-family: 'Inter', sans-serif !important; font-weight: 500 !important; font-size: 0.88rem !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #fbbf24 !important; border-bottom-color: #fbbf24 !important; }
div[data-testid="stImage"] { background: #0c1628 !important; border: 1px solid #1e3050 !important; border-radius: 10px !important; padding: 1rem !important; }
</style>"""

st.markdown(COMMON_CSS, unsafe_allow_html=True)

st.title("📊 Model Performance")
st.markdown("SHAP explainability plots aur model comparison.")
st.markdown("---")

PROCESSED_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'data', 'processed'
)

tab1, tab2, tab3 = st.tabs(["🐝 SHAP Beeswarm", "📊 Feature Importance", "🏆 Model Comparison"])

with tab1:
    st.subheader("SHAP Beeswarm Plot")
    st.markdown("Har feature ka fraud prediction pe impact.")
    img_path = os.path.join(PROCESSED_PATH, 'shap_beeswarm.png')
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning(f"Image not found: {img_path}")

with tab2:
    st.subheader("SHAP Feature Importance")
    st.markdown("Top features jo fraud detect karne mein sabse important hain.")
    img_path = os.path.join(PROCESSED_PATH, 'shap_important.png')
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning(f"Image not found: {img_path}")

with tab3:
    st.subheader("Model Comparison")
    st.markdown("Different models ka accuracy, precision, recall comparison.")
    img_path = os.path.join(PROCESSED_PATH, 'model_comparison.png')
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning(f"Image not found: {img_path}")
