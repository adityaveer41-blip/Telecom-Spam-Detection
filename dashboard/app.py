import streamlit as st
import requests

st.set_page_config(
    page_title="Telecom Fraud Detection",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.8rem; padding-bottom: 2rem; }

/* App bg — dark navy with subtle grid */
.stApp {
    background-color: #080d18;
    background-image:
        radial-gradient(ellipse at 15% 60%, rgba(220,38,38,0.05) 0%, transparent 45%),
        radial-gradient(ellipse at 85% 15%, rgba(251,146,60,0.04) 0%, transparent 40%),
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #060b14 !important;
    border-right: 1px solid #1a2640;
    min-width: 230px !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
    padding: 0.45rem 1rem !important;
    border-radius: 7px !important;
    font-size: 0.87rem !important;
    font-weight: 500 !important;
    color: #8ab4d4 !important; 
    white-space: nowrap !important;
    overflow: visible !important;
    transition: background 0.15s, color 0.15s;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover,
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
    background: rgba(220,38,38,0.12) !important;
    color: #f87171 !important;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #0d1829 0%, #111f35 60%, #0a1422 100%);
    border: 1px solid #1e3050;
    border-radius: 14px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.6rem;
    position: relative; overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 260px; height: 260px; border-radius: 50%;
    background: radial-gradient(circle, rgba(220,38,38,0.08) 0%, transparent 70%);
    animation: radar 4s ease-in-out infinite;
}
@keyframes radar {
    0%,100% { transform: scale(1); opacity:0.5; }
    50%      { transform: scale(1.3); opacity:1; }
}
.hero-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem; letter-spacing: 0.14em;
    color: #f87171;
    background: rgba(220,38,38,0.1);
    border: 1px solid rgba(220,38,38,0.25);
    padding: 3px 10px; border-radius: 4px;
    display: inline-block; margin-bottom: 1rem;
}
.hero-title {
    font-size: 2rem; font-weight: 700;
    color: #dce8f5; letter-spacing: -0.025em;
    line-height: 1.25; margin-bottom: 0.6rem;
}
.hero-title .accent { color: #f87171; }
.hero-desc { color: #4a6a8a; font-size: 0.92rem; font-weight: 300; line-height: 1.65; max-width: 520px; }

/* Cards */
.card-shell {
    background: #0c1628;
    border: 1px solid #1a2e48;
    border-radius: 12px;
    padding: 1.3rem 1.2rem 1rem;
    height: 100%;
    position: relative; overflow: hidden;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}
.card-shell::before {
    content: '';
    position: absolute; top:0; left:0; right:0; height:3px;
    background: var(--c);
    transform: scaleX(0); transform-origin: left;
    transition: transform 0.22s ease;
}
.card-shell:hover {
    border-color: var(--c);
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.4);
}
.card-shell:hover::before { transform: scaleX(1); }
.card-icon { font-size: 1.5rem; margin-bottom: 0.65rem; display: block; }
.card-name { font-size: 0.92rem; font-weight: 600; color: #c0d4e8; margin-bottom: 0.35rem; }
.card-info { font-size: 0.77rem; color: #3a5470; line-height: 1.55; margin-bottom: 0.9rem; }
.card-divider { height:1px; background:#1a2e48; margin-bottom: 0.7rem; }

/* Streamlit button inside card — styled as card CTA */
.card-shell div[data-testid="stButton"] button {
    background: transparent !important;
    border: 1px solid #1e3454 !important;
    border-radius: 6px !important;
    color: var(--c) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    padding: 5px 12px !important;
    width: 100% !important;
    transition: background 0.15s, border-color 0.15s !important;
    cursor: pointer !important;
}
.card-shell div[data-testid="stButton"] button:hover {
    background: rgba(255,255,255,0.04) !important;
    border-color: var(--c) !important;
}

/* API pill */
.api-pill {
    display:flex; align-items:center; gap:0.5rem;
    background:#080d18; border:1px solid #1a2640;
    border-radius:8px; padding:0.55rem 0.9rem;
    font-family:'JetBrains Mono',monospace; font-size:0.73rem;
}
.dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.dot-g { background:#22c55e; box-shadow:0 0 5px #22c55e88; }
.dot-r { background:#ef4444; box-shadow:0 0 5px #ef444488; }
.ok { color:#22c55e; } .err { color:#ef4444; }
.port { color:#1e3454; margin-left:auto; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<p style='font-family:JetBrains Mono,monospace;font-size:0.67rem;"
        "letter-spacing:0.1em;color:#1e3454;text-transform:uppercase;margin:0 0 6px'>"
        "System Status</p>", unsafe_allow_html=True)
    try:
        r = requests.get("http://localhost:8000/", timeout=2)
        ok = r.status_code == 200
    except Exception:
        ok = False

    dot = "dot-g" if ok else "dot-r"
    cls = "ok" if ok else "err"
    txt = "FastAPI Online" if ok else "API Offline"
    st.markdown(f'<div class="api-pill"><div class="dot {dot}"></div>'
                f'<span class="{cls}">{txt}</span>'
                f'<span class="port">:8000</span></div>', unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">⚠️ &nbsp;FRAUD DETECTION SYSTEM</div>
    <div class="hero-title">Telecom <span class="accent">Fraud Detection</span> Platform</div>
    <div class="hero-desc">
        Analyze Call Detail Records (CDR) in real time to identify fraudulent callers
        using ensemble Machine Learning and Generative AI explainability.
    </div>
</div>
""", unsafe_allow_html=True)


# ── Cards with st.button + st.switch_page ────────────────────────────────────
# st.switch_page() = Streamlit ka proper navigation function
# st.button() = visible, styleable, actually clickable
# CSS variable --c is set inline so each card has its own color

CARDS = [
    {"color":"#f87171", "icon":"🎯", "name":"Fraud Scoring",
     "desc":"CDR input → fraud probability, risk tier & confidence score.",
     "page":"pages/1_🎯_Fraud_Scoring.py", "btn":"Go to Scoring →"},
    {"color":"#fb923c", "icon":"🧠", "name":"AI Explanation",
     "desc":"LLM-powered natural language explanation for flagged numbers via SHAP.",
     "page":"pages/2_🧠_AI_Explanation.py", "btn":"Go to Explain →"},
    {"color":"#facc15", "icon":"💬", "name":"RAG Chatbot",
     "desc":"Query TRAI regulations knowledge base with retrieval-augmented generation.",
     "page":"pages/3_💬_RAG_Chatbot.py", "btn":"Go to Chatbot →"},
    {"color":"#4ade80", "icon":"📊", "name":"Model Performance",
     "desc":"SHAP plots, PR curves & model comparison across all classifiers.",
     "page":"pages/4_📊_Model_Performance.py", "btn":"Go to Metrics →"},
]

cols = st.columns(4, gap="medium")
for col, card in zip(cols, CARDS):
    with col:
        st.markdown(f"""
        <div class="card-shell" style="--c:{card['color']}">
            <span class="card-icon">{card['icon']}</span>
            <div class="card-name">{card['name']}</div>
            <div class="card-info">{card['desc']}</div>
            <div class="card-divider"></div>
        </div>
        """, unsafe_allow_html=True)
        # st.switch_page navigates to that page when button clicked
        if st.button(card["btn"], key=card["name"]):
            st.switch_page(card["page"])
