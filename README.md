📄 My RAG Chatbot – Brief Overview

My RAG Chatbot is a document-aware conversational assistant built using Streamlit and LangChain. It allows users to upload a PDF and ask questions that are answered strictly from the document content, ensuring accuracy and preventing hallucinations.

🔍 How it works

The uploaded PDF is parsed, chunked, and indexed using FAISS vector search.

User questions are answered using Retrieval-Augmented Generation (RAG), where only the most relevant document sections are used as context.

The chatbot includes adaptive retrieval, corrective self-checking, and document-only constraints to ensure reliable responses.

✨ Key Features

📄 PDF-based Q&A – Answers are grounded in the uploaded document

💡 Auto-generated suggested questions – Dynamically created from document content

🧠 Adaptive RAG – Retrieves the most relevant sections per question

🛡️ Corrective self-check – Flags answers not fully supported by the document

🔄 Reset & re-upload support – Clean session management

🧾 Minimal chat history view – Shows the most recent interactions for clarity

🎯 Use Cases

Reading and understanding books or articles

Analyzing policy or technical documents

Educational content exploration

Fast knowledge extraction from large PDFs

🏗️ Tech Stack

Frontend: Streamlit

LLMs: OpenAI (GPT-4o-mini)

Embeddings: Sentence-Transformers (MiniLM)

Vector Store: FAISS

Framework: LangChain
