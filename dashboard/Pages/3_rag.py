# dashboard/pages/3_rag.py
import streamlit as st
import requests

st.set_page_config(
    page_title="RAG Chatbot", 
    page_icon="💬", 
    layout="wide"
)

st.title("💬 RAG Knowledge Assistant")
st.markdown("TRAI regulations aur telecom fraud ke baare mein kuch bhi poochho.")
st.markdown("---")

# Session state mein chat history initialize karo
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Purani messages display karo
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        # Sources dikhao agar assistant ka message hai
        if message['role'] == 'assistant' and 'sources' in message:
            with st.expander("📚 Sources"):
                for source in message['sources']:
                    st.markdown(f"- {source}")

# Chat input
if prompt := st.chat_input("TRAI regulations ke baare mein kuch poochho..."):

    # User message add karo history mein
    st.session_state.messages.append({
        'role': 'user',
        'content': prompt
    })

    # User message display karo
    with st.chat_message('user'):
        st.markdown(prompt)

    # API call karo
    with st.chat_message('assistant'):
        with st.spinner("Knowledge base search ho raha hai..."):
            try:
                response = requests.post(
                    "http://localhost:8000/query",
                    json={"question": prompt, "n_results": 3},
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()
                    answer = result['answer']
                    sources = result['sources']

                    # Answer display karo
                    st.markdown(answer)

                    # Sources expander mein dikhao
                    with st.expander("📚 Sources used"):
                        for source in sources:
                            st.markdown(f"- {source}")

                    # History mein save karo
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': answer,
                        'sources': sources
                    })

                else:
                    st.error(f"API Error: {response.status_code}")

            except Exception as e:
                st.error(f"❌ Error: {e}")

# Sidebar mein chat clear button
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Sidebar mein sample questions
st.sidebar.markdown("### 💡 Sample Questions")
st.sidebar.markdown("""
- What happens after third TRAI violation?
- How to detect robocall fraud from CDR?
- What is International Revenue Share fraud?
- What does high CustServ calls indicate?
""")

 