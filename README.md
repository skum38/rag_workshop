# 📄 My RAG Chatbot (Adaptive + Corrective + Self)

My RAG Chatbot is a document-aware conversational assistant built using **Streamlit** and **LangChain**.  
It allows users to upload a PDF and ask questions that are answered **strictly from the document content**, ensuring accuracy and minimizing hallucinations.

---

## 🚀 Features

- 📄 **PDF Upload & Indexing**  
  Upload any PDF document and convert it into a searchable knowledge base.

- 🧠 **Adaptive Retrieval (RAG)**  
  Retrieves only the most relevant document chunks for each question using vector similarity search.

- 🛡️ **Corrective Self-Check**  
  Automatically validates answers against the retrieved document context and warns when an answer is not fully supported.

- 💡 **Document-Only Suggested Questions**  
  Dynamically generates relevant, factual questions based solely on the document content.

- 🔄 **Session Reset & Re-upload**  
  Easily clear the chat history and upload a new document without restarting the app.

- 🧾 **Clean Chat History**  
  Displays only the most recent interactions for a focused user experience.

---

## 🧠 How It Works

1. **PDF Loading**  
   The uploaded PDF is read and split into overlapping text chunks.

2. **Vector Indexing**  
   Chunks are converted into embeddings and stored in a FAISS vector database.

3. **Question Answering (RAG)**  
   User questions retrieve the most relevant chunks, which are passed to the LLM for answering.

4. **Answer Validation**  
   A self-check step verifies that the generated answer is supported by the document.

5. **Suggested Questions Refresh**  
   After each answer, new document-based questions are generated.

---

## 🏗️ Tech Stack

- **UI Framework:** Streamlit  
- **LLM:** OpenAI (GPT-4o-mini)  
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)  
- **Vector Store:** FAISS  
- **Framework:** LangChain  

---

## 📦 Installation

```bash
pip install streamlit langchain langchain-community langchain-huggingface \
langchain-openai sentence-transformers faiss-cpu pypdf python-dotenv
