# 📄 My RAG Chatbot – Brief Overview

My RAG Chatbot is a document-aware conversational assistant built using **Streamlit** and **LangChain**.  
It allows users to upload a PDF and ask questions that are answered **strictly from the document content**, ensuring accuracy and preventing hallucinations.

---

## 🔍 How It Works

- The uploaded PDF is **parsed, chunked, and indexed** using FAISS vector search.
- User questions are answered using **Retrieval-Augmented Generation (RAG)**, where only the most relevant document sections are used as context.
- The chatbot combines **adaptive retrieval**, **corrective self-checking**, and **document-only constraints** to ensure reliable and trustworthy responses.
- Run -  pip install streamlit langchain langchain-community langchain-huggingface transformers langchain-openai sentence-transformers faiss-cpu pypdf
- **streamlit run '.\rag_chatbot_final.py' **

---

## ✨ Key Features

- 📄 **PDF-based Q&A**  
  Answers are fully grounded in the uploaded document.

- 💡 **Auto-generated Suggested Questions**  
  Questions are dynamically generated from document content only.

- 🧠 **Adaptive RAG**  
  Retrieves the most relevant document sections for each query.

- 🛡️ **Corrective Self-Check**  
  Flags answers that are not fully supported by the document.

- 🔄 **Reset & Re-upload Support**  
  Clean session management for multiple documents.

- 🧾 **Minimal Chat History View**  
  Displays only the most recent interactions for clarity.

---

## 🎯 Use Cases

- Reading and understanding books or articles  
- Analyzing policy or technical documents  
- Educational content exploration  
- Fast knowledge extraction from large PDFs  

---

## 🏗️ Tech Stack

- **Frontend:** Streamlit  
- **LLMs:** OpenAI (GPT-4o-mini)  
- **Embeddings:** Sentence-Transformers (MiniLM)  
- **Vector Store:** FAISS  
- **Framework:** LangChain  

---

## 📌 Design Philosophy

- Accuracy over creativity  
- No hallucinated answers  
- Document-first reasoning  
- Simple, clean, and explainable RAG pipeline  

---

## 📄 License

This project is intended for learning, experimentation, and demonstrations.  
You are free to extend and customize it for your own use.

<img width="1080" height="602" alt="image" src="https://github.com/user-attachments/assets/879159e9-5b2a-42e4-8345-478cfaa26011" />

