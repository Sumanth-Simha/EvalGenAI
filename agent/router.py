# agent/router.py

from agent.classifier import classify
from RAG.answer_rag.retrieve import retrieve_answer
from RAG.qp_rag.retrieve_qp import predict_questions
from RAG.qp_rag.generate_paper import build_pairs, format_ia_paper
from RAG.qp_rag.generate_sem_paper import generate_sem_paper

# =========================
# HELPER
# =========================

def extract_questions_list(result):
    """
    Ensure we always get a clean list of questions
    """
    if isinstance(result, list):
        # already list of tuples or strings
        return [q if isinstance(q, str) else q[0] for q in result]

    # fallback (if string - shouldn't happen ideally)
    lines = result.split("\n")
    questions = []

    for line in lines:
        if line.strip().startswith(tuple(str(i) for i in range(1, 10))):
            q = line.split(".", 1)[-1].strip()
            if q:
                questions.append(q)

    return questions


# =========================
# ROUTER
# =========================
def route(query: str):
    task = classify(query)

    print(f"\n🧠 Detected Task: {task.upper()}")

    query_lower = query.lower()

    # 🔥 SEM PAPER (CHECK FIRST)
    if "sem paper" in query_lower or "semester paper" in query_lower:
        return generate_sem_paper(query)

    # 🔥 IA PAPER
    if "question paper" in query_lower or "ia paper" in query_lower:
        questions = predict_questions(query, top_k=50)

        q_list = extract_questions_list(questions)

        if len(q_list) < 2:
            return "⚠️ Not enough questions to generate paper."

        pairs = build_pairs(q_list)

        return format_ia_paper(pairs)

    # 🔥 NORMAL PREDICTION
    if task == "predict":
        return predict_questions(query)

    # 🔥 ANSWER GENERATION
    return retrieve_answer(query)
