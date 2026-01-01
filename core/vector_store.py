# core/vector_store.py
from langchain_community.vectorstores import FAISS

def build_vectorstore(chunks, embeddings):
    return FAISS.from_documents(chunks, embeddings)

