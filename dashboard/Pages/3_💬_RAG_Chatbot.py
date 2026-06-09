import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", page_icon="💬", layout="wide")

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
div[data-testid="stChatMessage"] { background: #0c1628 !important; border: 1px solid #1e3050 !important; border-radius: 10px !important; margin-bottom: 0.5rem !important; }
div[data-testid="stChatMessage"] p { color: #c0d4e8 !important; }
div[data-testid="stChatInput"] textarea { background: #0c1628 !important; border: 1px solid #1e3050 !important; color: #c0d4e8 !important; border-radius: 10px !important; font-family: 'Inter', sans-serif !important; }
div[data-testid="stChatInput"] textarea:focus { border-color: #34d399 !important; box-shadow: 0 0 0 2px rgba(52,211,153,0.15) !important; }
div[data-testid="stExpander"] { background: #0c1628 !important; border: 1px solid #1e3050 !important; border-radius: 8px !important; }
div[data-testid="stExpander"] summary { color: #6a8aaa !important; font-size: 0.82rem !important; }
div[data-testid="stButton"] button { background: transparent !important; border: 1px solid #1e3050 !important; color: #6a8aaa !important; border-radius: 7px !important; font-family: 'Inter', sans-serif !important; }
div[data-testid="stButton"] button:hover { border-color: #f87171 !important; color: #f87171 !important; }
</style>"""

st.markdown(COMMON_CSS, unsafe_allow_html=True)

st.title("💬 RAG Knowledge Assistant")
st.markdown("TRAI regulations aur telecom fraud ke baare mein kuch bhi poochho.")
st.markdown("---")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        if message['role'] == 'assistant' and 'sources' in message:
            with st.expander("📚 Sources"):
                for source in message['sources']:
                    st.markdown(f"- {source}")

if prompt := st.chat_input("TRAI regulations ke baare mein kuch poochho..."):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        with st.spinner("Knowledge base search ho raha hai..."):
            try:
                response = requests.post(
                    "http://localhost:8000/query",
                    json={"question": prompt, "n_results": 3}, timeout=120
                )
                if response.status_code == 200:
                    result = response.json()
                    answer = result['answer']
                    sources = result['sources']
                    st.markdown(answer)
                    with st.expander("📚 Sources used"):
                        for source in sources:
                            st.markdown(f"- {source}")
                    st.session_state.messages.append({
                        'role': 'assistant', 'content': answer, 'sources': sources
                    })
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("### 💡 Sample Questions")
st.sidebar.markdown("""
- What happens after third TRAI violation?
- How to detect robocall fraud from CDR?
- What is International Revenue Share fraud?
- What does high CustServ calls indicate?
""")
