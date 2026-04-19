from sentence_transformers import SentenceTransformer
from utils.db import get_chroma_client
import re

# =========================
# CONFIG
# =========================

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

CHROMA_CLIENT = get_chroma_client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="iot_qp")


# =========================
# MODULE EXTRACTOR 🔥
# =========================

def extract_module(query):
    match = re.search(r"module\s*(\d+)", query.lower())
    if match:
        return f"Module {match.group(1)}"
    return None


# =========================
# PREDICT QUESTIONS
# =========================

def predict_questions(query, top_k=15):
    query_embedding = EMBED_MODEL.encode([query]).tolist()

    module = extract_module(query)

    # 🔥 STRICT FILTER (NO DIAGRAMS EVER)
    where_clause = {
        "type": {"$in": ["assignment", "pyq"]}
    }

    if module:
        where_clause = {
            "$and": [
                {"type": {"$in": ["assignment", "pyq"]}},
                {"module": module}
            ]
        }

    results = COLLECTION.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where=where_clause
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    if not docs:
        return "⚠️ No relevant questions found."

    scored = []

    for doc, meta in zip(docs, metas):
        score = 0

        if meta.get("type") == "assignment":
            score += 3
        elif meta.get("type") == "ia":
            score += 2
        elif meta.get("type") == "pyq":
            score += 1

        scored.append((doc, score))

    # sort by score
    scored.sort(key=lambda x: x[1], reverse=True)

    # remove duplicates
    seen = set()
    final = []

    for q, score in scored:
        if q not in seen:
            final.append(q)
            seen.add(q)

        if len(final) == 5:
            break

    # 🔥 CLEAN OUTPUT
    formatted = "🔥 Predicted Important Questions\n\n"

    if module:
        formatted += f"📘 {module}\n\n"

    for i, q in enumerate(final, 1):
        formatted += f"{i}. {q}\n\n"

    formatted += "💡 Focus on these for exams.\n"

    return formatted