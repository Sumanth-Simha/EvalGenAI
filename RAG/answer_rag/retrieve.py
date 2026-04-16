# RAG/answer_rag/retrieve.py

from utils.embeddings import embed_text
from utils.config_loader import load_config
from .generate import generate_answer
from utils.db import get_chroma_client

# =========================
# CONFIG
# =========================

config = load_config()

CHROMA_CLIENT = get_chroma_client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="iot_kb")


# =========================
# RETRIEVE
# =========================

def retrieve(query):
    query_embedding = embed_text(query)

    # 🔥 1. Retrieve NOTES separately
    note_results = COLLECTION.query(
        query_embeddings=query_embedding,
        n_results=config["retrieval"]["top_k_answer"],
        where={"type": "note"}
    )

    # 🔥 2. Retrieve DIAGRAMS separately (ALWAYS)
    diagram_results = COLLECTION.query(
        query_embeddings=query_embedding,
        n_results=2,  # force diagrams
        where={"type": "diagram"}
    )

    notes = []
    diagrams = []
    seen_notes = set()

    # =========================
    # PROCESS NOTES
    # =========================

    if note_results and note_results.get("documents"):
        docs = note_results["documents"][0]

        for doc in docs:
            if doc not in seen_notes:
                notes.append(doc)
                seen_notes.add(doc)

    # =========================
    # PROCESS DIAGRAMS
    # =========================

    if diagram_results and diagram_results.get("metadatas"):
        metas = diagram_results["metadatas"][0]

        for meta in metas:
            diagrams.append({
                "title": meta.get("title", ""),
                "image_path": meta.get("image_path", ""),
                "topic": meta.get("topic", "")
            })

    # =========================
    # DEBUG LOGS
    # =========================

    print("\n📘 Notes Retrieved:", len(notes))
    print("🖼️ Diagrams Retrieved:", len(diagrams))

    if diagrams:
        print("🖼️ Diagram Titles:", [d["title"] for d in diagrams])

    return notes, diagrams


# =========================
# WRAPPER (used by agent)
# =========================

def retrieve_answer(query):
    notes, diagrams = retrieve(query)

    return generate_answer(query, notes, diagrams)