import os
import json
from sentence_transformers import SentenceTransformer
from utils.db import get_chroma_client

# =========================
# CONFIG
# =========================

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

CHROMA_CLIENT = get_chroma_client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="iot_qp")


# =========================
# SMART QUESTION EXTRACTOR 🔥
# =========================

def extract_question(item, file):
    """
    Handles ALL possible formats safely
    """

    if not isinstance(item, dict):
        return None

    # 🔥 try multiple keys
    for key in ["q", "question", "text", "content"]:
        val = item.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()

    return None


# =========================
# LOAD ALL QUESTIONS
# =========================

def load_all_questions():
    base_path = "data/iot"

    documents = []
    metadatas = []
    ids = []

    counter = 0
    skipped = 0

    # 🔥 ASSIGNMENTS / SUPERSET
    assign_path = os.path.join(base_path, "superset")
    if os.path.exists(assign_path):
        for file in os.listdir(assign_path):
            if file.endswith(".json"):
                file_path = os.path.join(assign_path, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    if isinstance(data, list):
                        for item in data:
                            q_text = extract_question(item, file)

                            if q_text:
                                documents.append(q_text)
                                metadatas.append({
                                    "type": "assignment",
                                    "topic": item.get("topic", "unknown")
                                })
                                ids.append(f"assign_{counter}")
                                counter += 1
                            else:
                                skipped += 1

    # 🔥 PYQ + IA
    pyq_path = os.path.join(base_path, "pyq")
    if os.path.exists(pyq_path):
        for file in os.listdir(pyq_path):
            if file.endswith(".json"):
                file_path = os.path.join(pyq_path, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # CASE 1: simple list
                    if isinstance(data, list):
                        for item in data:
                            q_text = extract_question(item, file)

                            if q_text:
                                documents.append(q_text)
                                metadatas.append({
                                    "type": "pyq",
                                    "topic": item.get("topic", "unknown")
                                })
                                ids.append(f"pyq_{counter}")
                                counter += 1
                            else:
                                skipped += 1

                    # CASE 2: IA structured
                    elif isinstance(data, dict) and "questions" in data:
                        for qn in data["questions"]:
                            options = qn.get("options", [])

                            for opt in options:
                                q_text = extract_question(opt, file)

                                if q_text:
                                    documents.append(q_text)
                                    metadatas.append({
                                        "type": "pyq",
                                        "topic": opt.get("topic", "unknown")
                                    })
                                    ids.append(f"pyq_{counter}")
                                    counter += 1
                                else:
                                    skipped += 1

    print(f"⚠️ Skipped {skipped} invalid entries")

    return documents, metadatas, ids


# =========================
# INGEST
# =========================

def ingest_qp():
    docs, metas, ids = load_all_questions()

    if not docs:
        print("❌ No questions found.")
        return

    print(f"📦 Loaded {len(docs)} questions")

    embeddings = EMBED_MODEL.encode(docs).tolist()

    # 🔥 Clear old data
    try:
        COLLECTION.delete(where={})
        print("🧹 Cleared old collection")
    except:
        print("⚠️ Could not clear collection")

    COLLECTION.add(
        documents=docs,
        metadatas=metas,
        ids=ids,
        embeddings=embeddings
    )

    print("✅ Question Prediction DB ready")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    ingest_qp()
