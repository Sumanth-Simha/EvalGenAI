# RAG/answer_rag/generate.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# =========================
# CONFIG
# =========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)


# =========================
# GENERATE
# =========================

def generate_answer(query, notes, diagrams):
    # 🔒 Safety: handle empty retrieval
    if not notes and not diagrams:
        return {
            "answer": "⚠️ No relevant information found in knowledge base.",
            "diagrams": []
        }

    context = "\n\n".join(notes[:5])  # limit context

    # 🔥 Stronger diagram injection
    diagram_text = ""

    if diagrams:
        diagram_text = "\n\nIMPORTANT DIAGRAMS:\n"
        for d in diagrams:
            diagram_text += f"""
Diagram Title: {d.get('title', '')}
"""

    prompt = f"""
You are an academic assistant.

Answer the question in a clear, exam-ready format.

Context:
{context}

{diagram_text}

Question:
{query}

Instructions:
- Start with a clear definition
- Use headings and bullet points
- Highlight important keywords
- Provide examples if relevant
- 🔥 MUST refer to diagrams if provided
- Mention diagram names explicitly
- Keep answer structured and exam-friendly
"""

    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")  # safer model

        response = model.generate_content(prompt)

        if not response or not response.text:
            raise ValueError("Empty response from LLM")

        return {
            "answer": response.text.strip(),
            "diagrams": diagrams  # 🔥 return diagrams for UI
        }

    except Exception as e:
        print("⚠️ LLM generation failed:", e)

        # 🔥 fallback content
        fallback = "\n\n".join(notes[:3]) if notes else "No fallback available."

        return {
            "answer": f"""
⚠️ AI generation failed. Showing best retrieved content:

{fallback}

👉 Tip: Try rephrasing your question.
""",
            "diagrams": diagrams
        }