# core/rag_engine.py
from config import TOP_K

def is_definition_question(q):
    return q.lower().startswith(("who", "what", "where", "when"))

def rag_answer(question, vectorstore, llm):
    results = vectorstore.similarity_search_with_score(question, k=TOP_K)
    docs = [doc for doc, _ in results]

    if not docs:
        return "❌ No verified answer found.", []

    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
Answer in ONE sentence.
Use ONLY words from the context.

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt).content

    if not is_definition_question(question):
        check = llm.invoke(
            f"""
Context:
{context}

Answer:
{answer}

Is this answer fully supported?
Reply YES or NO.
"""
        ).content.lower()

        if "no" in check:
            answer = "⚠️ Answer not fully supported by the document."

    return answer, docs

