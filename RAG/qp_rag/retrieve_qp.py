from sentence_transformers import SentenceTransformer
from utils.db import get_chroma_client

# =========================
# CONFIG
# =========================

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

CHROMA_CLIENT = get_chroma_client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="iot_qp")



def predict_questions(query, top_k=15):
    query_embedding = EMBED_MODEL.encode([query]).tolist()

    results = COLLECTION.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    scored = []

    for doc, meta in zip(docs, metas):
        score = 0

        if meta["type"] == "assignment":
            score += 3
        elif meta["type"] == "ia":
            score += 2
        elif meta["type"] == "pyq":
            score += 1

        scored.append((doc, score))

    # sort by score
    scored.sort(key=lambda x: x[1], reverse=True)

    # remove duplicates
    seen = set()
    final = []

    for q, score in scored:
        if q not in seen:
            final.append((q, score))
            seen.add(q)

        if len(final) == 5:
            break

    # 🔥 FORMAT OUTPUT (THIS IS THE FIX)
    formatted = "🔥 Predicted Important Questions\n\n"

    for i, (q, score) in enumerate(final, 1):
        formatted += f"{i}. {q}\n\n"

    formatted += "💡 Focus on these for exams.\n"

    return formatted