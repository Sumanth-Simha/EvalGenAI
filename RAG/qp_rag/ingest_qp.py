import os
import json
from sentence_transformers import SentenceTransformer

from utils.db import get_chroma_client  # 🔥 unified DB

# =========================
# CONFIG
# =========================

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

CHROMA_CLIENT = get_chroma_client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="iot_qp")


# =========================
# LOAD ALL QUESTIONS
# =========================

def extract_question(item, file):
    """
    Handles different formats safely
    """
    q_text = item.get("q") or item.get("question")

    if not q_text:
        print(f"⚠️ Skipping invalid question in {file}")
        return None

    return q_text


def load_all_questions():
    base_path = "data/iot"

    documents = []
    metadatas = []
    ids = []

    counter = 0

    # 🔥 ASSIGNMENTS (SUPERSET)
    assign_path = os.path.join(base_path, "superset")
    if os.path.exists(assign_path):
        for file in os.listdir(assign_path):
            if file.endswith(".json"):
                file_path = os.path.join(assign_path, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

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

    # 🔥 PYQ (includes IA papers)
    pyq_path = os.path.join(base_path, "pyq")
    if os.path.exists(pyq_path):
        for file in os.listdir(pyq_path):
            if file.endswith(".json"):
                file_path = os.path.join(pyq_path, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # 🔥 Handle IA structured format
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

                    elif isinstance(data, dict) and "questions" in data:
                        for qn in data["questions"]:
                            for opt in qn.get("options", []):
                                q_text = opt.get("question")

                                if q_text:
                                    documents.append(q_text)
                                    metadatas.append({
                                        "type": "pyq",
                                        "topic": opt.get("topic", "unknown")
                                    })
                                    ids.append(f"pyq_{counter}")
                                    counter += 1
                                else:
                                    print(f"⚠️ Skipping invalid IA entry in {file}")

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