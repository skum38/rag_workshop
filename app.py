# app.py
import streamlit as st

from state import init_state, reset_state
from core.llm import load_embeddings, load_answer_llm, load_question_llm
from core.document_loader import load_and_chunk_pdf
from core.vector_store import build_vectorstore
from core.rag_engine import rag_answer
from core.question_generator import generate_questions

# -------------------------
# Init
# -------------------------
init_state()

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("📄 RAG Chatbot")

embeddings = load_embeddings()
answer_llm = load_answer_llm()
question_llm = load_question_llm()

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.markdown("### Controls")

    if st.button("🔄 Reset"):
        reset_state()
        st.rerun()

    st.markdown("---")
    st.info(st.session_state.upload_status)

# -------------------------
# PDF Upload
# -------------------------
uploaded_pdf = st.file_uploader(
    "Upload a PDF",
    type="pdf",
    key=f"pdf_{st.session_state.uploader_key}"
)

if uploaded_pdf and not st.session_state.pdf_indexed:
    st.session_state.upload_status = "⏳ Indexing PDF..."

    with st.spinner("Reading and indexing PDF..."):
        chunks = load_and_chunk_pdf(uploaded_pdf)
        st.session_state.vectorstore = build_vectorstore(chunks, embeddings)
        st.session_state.pdf_indexed = True

        st.session_state.suggested_questions = generate_questions(
            chunks[:6], set(), question_llm
        )

    st.session_state.upload_status = "✅ PDF indexed and ready"

# -------------------------
# Main UI (only if PDF ready)
# -------------------------
if st.session_state.vectorstore:
    col1, col2 = st.columns([2, 1])

    # ---- Suggested Questions ----
    with col2:
        st.markdown("### 💡 Suggested Questions")
        for i, q in enumerate(st.session_state.suggested_questions):
            if st.button(q, key=f"sug_{i}"):
                st.session_state.pending_question = q

    # ---- Chat ----
    with col1:
        user_input = st.chat_input("Ask a question from the document")

        question = user_input or st.session_state.pending_question
        st.session_state.pending_question = None

        if question:
            answer, docs = rag_answer(
                question,
                st.session_state.vectorstore,
                answer_llm
            )

            st.session_state.asked_questions.add(question)
            st.session_state.messages.insert(0, ("assistant", answer))
            st.session_state.messages.insert(0, ("user", question))

            st.session_state.suggested_questions = generate_questions(
                docs,
                st.session_state.asked_questions,
                question_llm
            )

            if st.session_state.first_question_done:
                st.rerun()
            else:
                st.session_state.first_question_done = True

        # Show last 5 chats (10 messages)
        for role, msg in st.session_state.messages[:10]:
            with st.chat_message(role):
                st.write(msg)

else:
    st.info("⬆️ Upload a PDF to start chatting")
