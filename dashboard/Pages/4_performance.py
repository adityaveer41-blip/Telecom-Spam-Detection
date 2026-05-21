# dashboard/pages/4_performance.py
import streamlit as st
import os

st.set_page_config(
    page_title="Model Performance", 
    page_icon="📊", 
    layout="wide"
)

st.title("📊 Model Performance")
st.markdown("SHAP explainability plots aur model comparison.")
st.markdown("---")

# Images ka path
PROCESSED_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'data', 'processed'
)

# Tab layout
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