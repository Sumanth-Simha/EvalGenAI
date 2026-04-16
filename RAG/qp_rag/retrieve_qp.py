from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from utils.db import get_chroma_client

# =========================
# CONFIG
# =========================

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

from utils.db import get_chroma_client

CHROMA_CLIENT = get_chroma_client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="iot_qp")


# =========================
# PREDICTION LOGIC
# =========================

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

        # 🔥 WEIGHTING SYSTEM
        if meta["type"] == "assignment":
            score += 3
        elif meta["type"] == "ia":
            score += 2
        elif meta["type"] == "pyq":
            score += 1

        scored.append((doc, score))

    # 🔥 SORT BY SCORE
    scored.sort(key=lambda x: x[1], reverse=True)

    # remove duplicates while keeping order
    seen = set()
    final = []

    for q, score in scored:
        if q not in seen:
            final.append((q, score))
            seen.add(q)

        if len(final) == 5:
            break

    return final


# =========================
# RUN
# =========================

if __name__ == "__main__":
    query = input("Enter topic (e.g., IoT Framework): ")

    results = predict_questions(query)

    print("\n🔥 Predicted Questions:\n")

    for q, score in results:
        print(f"[Score {score}] {q}")
