# core/llm.py
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st
from config import EMBEDDING_MODEL, ANSWER_MODEL

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

@st.cache_resource
def load_answer_llm():
    return ChatOpenAI(model=ANSWER_MODEL, temperature=0)

@st.cache_resource
def load_question_llm():
    return ChatOpenAI(model=ANSWER_MODEL, temperature=0.7)

