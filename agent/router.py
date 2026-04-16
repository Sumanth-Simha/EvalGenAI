# agent/router.py

from agent.classifier import classify
from RAG.answer_rag.retrieve import retrieve_answer
from RAG.qp_rag.retrieve_qp import predict_questions


def route(query: str):
    task = classify(query)

    print(f"\n🧠 Detected Task: {task.upper()}")

    if task == "predict":
        return predict_questions(query)

    return retrieve_answer(query)
