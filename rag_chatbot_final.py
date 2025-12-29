"""
Improved RAG Chatbot using Streamlit + LangChain

Features:
- PDF upload and indexing
- Adaptive retrieval using similarity search
- Corrective self-check to avoid hallucinations
- Document-only suggested questions
- Clean UI with reset, upload status, and chat history control
"""

import streamlit as st
import tempfile
import os
import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="📄 My RAG Chatbot", layout="wide")
st.title("📄 RAG Chatbot (Adaptive + Corrective + Self)")

# -------------------------------------------------
# Session State
# -------------------------------------------------
st.session_state.setdefault("vectorstore", None)
st.session_state.setdefault("messages", [])
st.session_state.setdefault("suggested_questions", [])
st.session_state.setdefault("asked_questions", set())
st.session_state.setdefault("pending_question", None)
st.session_state.setdefault("pdf_indexed", False)
st.session_state.setdefault("uploader_key", 0)
st.session_state.setdefault("upload_status", "Awaiting PDF upload")

# -------------------------------------------------
# Sidebar Controls
# -------------------------------------------------
with st.sidebar:
    st.markdown("### Controls")

    if st.button("🔄 Reset Chat"):
        for key in [
            "vectorstore",
            "messages",
            "suggested_questions",
            "asked_questions",
            "pending_question",
            "pdf_indexed",
        ]:
            st.session_state.pop(key, None)

        st.session_state.uploader_key += 1
        st.session_state.upload_status = "Awaiting PDF upload"
        st.rerun()

    st.markdown("---")
    st.markdown("### 📌 Upload Status")
    st.info(st.session_state.upload_status)

# -------------------------------------------------
# Models
# -------------------------------------------------
@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

@st.cache_resource
def load_llm(temp=0):
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temp
    )

embeddings = load_embeddings()
answer_llm = load_llm(temp=0)
question_llm = load_llm(temp=0.7)

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def llm_text(out):
    return out.content if hasattr(out, "content") else str(out)

def is_definition_question(q):
    q = q.lower().strip()
    return q.startswith(("who", "where", "when", "what"))

# -------------------------------------------------
# Suggested Questions (Document-only)
# -------------------------------------------------
def generate_suggested_questions_from_docs(docs, asked, n=5):
    text = "\n\n".join(d.page_content for d in docs)[:3000]

    prompt = f"""
Generate {n} NEW factual questions.

Rules:
- Answerable ONLY from the text
- Do NOT repeat these questions: {list(asked)}
- One question per line
- End with '?'

Text:
{text}
"""

    raw = llm_text(question_llm.invoke(prompt))

    questions = []
    for line in raw.split("\n"):
        line = re.sub(r"^[\d\.\-\•\*]+\s*", "", line.strip())
        if line.endswith("?") and line not in asked:
            questions.append(line)

    return questions[:n]

# -------------------------------------------------
# PDF Upload (with dynamic key)
# -------------------------------------------------
uploaded_pdf = st.file_uploader(
    "Upload a PDF",
    type="pdf",
    key=f"pdf_uploader_{st.session_state.uploader_key}"
)

if uploaded_pdf and not st.session_state.pdf_indexed:
    st.session_state.upload_status = "⏳ Uploading and indexing PDF..."

    with st.spinner("Reading and indexing PDF..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_pdf.read())
            pdf_path = tmp.name

        pages = PyPDFLoader(pdf_path).load()
        os.remove(pdf_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        chunks = splitter.split_documents(pages)

        st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
        st.session_state.pdf_indexed = True

        st.session_state.suggested_questions = generate_suggested_questions_from_docs(
            chunks[:6], set()
        )

    st.session_state.upload_status = "✅ PDF indexed and ready to chat"

# -------------------------------------------------
# RAG Answer Logic
# -------------------------------------------------
def rag_answer(question):
    vs = st.session_state.vectorstore

    results = vs.similarity_search_with_score(question, k=6)
    docs = [doc for doc, _ in results]

    if not docs:
        return "❌ No verified answer found in the document.", []

    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
Answer in ONE sentence.
Use ONLY words that appear in the context.
Do NOT paraphrase.

Context:
{context}

Question:
{question}
"""
    answer = llm_text(answer_llm.invoke(prompt))

    if not is_definition_question(question):
        check = llm_text(
            answer_llm.invoke(
                f"""
Context:
{context}

Answer:
{answer}

Does the context clearly contain the same factual information as the answer,
even if phrased differently?

Reply ONLY YES or NO.
"""
            )
        ).lower()

        if "no" in check:
            answer = "⚠️ Answer not fully supported by the document."

    return answer, docs

# -------------------------------------------------
# UI
# -------------------------------------------------
if st.session_state.vectorstore:
    col1, col2 = st.columns([2, 1])

    # Suggested Questions
    with col2:
        st.markdown("### 💡 Suggested Questions")
        st.caption("Updated after every answer")

        for i, q in enumerate(st.session_state.suggested_questions):
            if st.button(q, key=f"sug_{i}"):
                st.session_state.pending_question = q
                st.rerun()

    # Chat
    with col1:
        user_input = st.chat_input("Ask a question from the document")

        question = user_input or st.session_state.pending_question
        st.session_state.pending_question = None

        if question:
            answer, docs = rag_answer(question)
            st.session_state.asked_questions.add(question)

            # Latest first
            st.session_state.messages.insert(0, ("assistant", answer))
            st.session_state.messages.insert(0, ("user", question))

            # Refresh suggestions
            st.session_state.suggested_questions = generate_suggested_questions_from_docs(
                docs, st.session_state.asked_questions
            )

            st.rerun()

        # Show only last 5 chat histories (10 messages)
        for role, msg in st.session_state.messages[:10]:
            with st.chat_message(role):
                st.write(msg)
else:
    st.info("⬆️ Upload a PDF to start chatting.")
