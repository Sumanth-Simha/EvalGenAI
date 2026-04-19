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
    query_lower = query.lower()

    # =========================
    # 🔥 NOTES (CLEAN)
    # =========================
    note_results = COLLECTION.query(
        query_embeddings=query_embedding,
        n_results=5,
        where={"type": "note"}
    )

    notes = note_results.get("documents", [[]])[0]
    note_metas = note_results.get("metadatas", [[]])[0]

    # =========================
    # 🔥 DIAGRAMS (CONTROLLED)
    # =========================
    diagram_results = COLLECTION.query(
        query_embeddings=query_embedding,
        n_results=5,  # fetch more, filter later
        where={"type": "diagram"}
    )

    diagram_docs = diagram_results.get("documents", [[]])[0]
    diagram_metas = diagram_results.get("metadatas", [[]])[0]

    filtered_diagrams = []

    # 🔥 keyword-based matching
    query_words = set(query_lower.split())

    for doc, meta in zip(diagram_docs, diagram_metas):
        topic = meta.get("topic", "").lower()
        title = meta.get("title", "").lower()

        if any(word in topic or word in title for word in query_words):
            filtered_diagrams.append(meta)

    # =========================
    # 🔥 INTELLIGENT DIAGRAM CONTROL
    # =========================

    diagram_keywords = ["diagram", "draw", "illustrate", "architecture", "block diagram"]
    diagram_friendly_topics = [
        "osi", "architecture", "framework", "layers",
         "protocol", "model"
    ]

    user_wants_diagram = any(k in query_lower for k in diagram_keywords)
    topic_match = any(word in query_lower for word in diagram_friendly_topics)

    relevant_diagrams = filtered_diagrams[:2]

    # 🔥 FINAL DECISION
    if user_wants_diagram:
        diagrams = relevant_diagrams

    elif topic_match and len(filtered_diagrams) > 0:
        diagrams = relevant_diagrams

    else:
        diagrams = []

    # =========================
    # DEBUG LOGS
    # =========================
    print("\n📘 Notes Retrieved:", len(notes))
    print("🖼️ Diagrams Retrieved:", len(diagrams))

    if diagrams:
        print("🖼️ Diagram Titles:", [d.get("title", "") for d in diagrams])

    return notes, diagrams


# =========================
# WRAPPER (used by agent)
# =========================

def retrieve_answer(query):
    notes, diagrams = retrieve(query)
    return generate_answer(query, notes, diagrams)