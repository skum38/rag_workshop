# core/question_generator.py
import re
from config import MAX_SUGGESTED_QUESTIONS

def generate_questions(docs, asked, llm):
    text = "\n\n".join(d.page_content for d in docs)[:3000]

    prompt = f"""
Generate {MAX_SUGGESTED_QUESTIONS} factual questions.
Only from text. No repeats.
{text}
"""

    raw = llm.invoke(prompt).content

    questions = []
    for line in raw.split("\n"):
        line = re.sub(r"^[\d\.\-\*]+\s*", "", line.strip())
        if line.endswith("?") and line not in asked:
            questions.append(line)

    return questions[:MAX_SUGGESTED_QUESTIONS]

