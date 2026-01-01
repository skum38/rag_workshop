# state.py
import streamlit as st

DEFAULT_STATE = {
    "vectorstore": None,
    "messages": [],
    "suggested_questions": [],
    "asked_questions": set(),
    "pending_question": None,
    "pdf_indexed": False,
    "uploader_key": 0,
    "upload_status": "Awaiting PDF upload",
    "first_question_done": False,
}

def init_state():
    for key, value in DEFAULT_STATE.items():
        st.session_state.setdefault(key, value)

def reset_state():
    for key in DEFAULT_STATE:
        st.session_state.pop(key, None)

