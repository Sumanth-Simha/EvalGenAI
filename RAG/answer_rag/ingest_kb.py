import os
import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from utils.db import get_chroma_client

# =========================
# CONFIG
# =========================

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

from utils.db import get_chroma_client

CHROMA_CLIENT = get_chroma_client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="iot_kb")


# =========================
# LOAD ALL NOTES
# =========================

def load_all_notes():
    base_path = "data/iot"

    documents = []
    metadatas = []
    ids = []

    for module in os.listdir(base_path):
        notes_path = os.path.join(base_path, module, "notes")

        if not os.path.exists(notes_path):
            continue

        for file in os.listdir(notes_path):
            if file.endswith(".json"):
                file_path = os.path.join(notes_path, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    for item in data:
                        try:
                            documents.append(item["content"])

                            metadatas.append({
                                "type": "note",
                                "topic": item.get("topic", "unknown"),
                                "module": module
                            })

                            ids.append(f"{module}_{item['id']}")

                        except KeyError:
                            print(f"⚠️ Skipping invalid note entry in {file_path}")

    return documents, metadatas, ids


# =========================
# LOAD ALL DIAGRAMS
# =========================

def load_all_diagrams():
    base_path = "data/iot"

    documents = []
    metadatas = []
    ids = []

    for module in os.listdir(base_path):
        diag_path = os.path.join(base_path, module, "diagrams", "diagrams.json")

        if not os.path.exists(diag_path):
            continue

        with open(diag_path, "r", encoding="utf-8") as f:
            diagrams = json.load(f)

            for d in diagrams:
                try:
                    doc_text = f"{d['title']}. {d['description']}"

                    documents.append(doc_text)

                    metadatas.append({
                        "type": "diagram",
                        "topic": ", ".join(d.get("topics", [])),
                        "module": module,
                        "image_path": d.get("image_path", ""),
                        "title": d.get("title", "")
                    })

                    ids.append(f"{module}_{d['id']}")

                except KeyError:
                    print(f"⚠️ Skipping invalid diagram entry in {diag_path}")

    return documents, metadatas, ids


# =========================
# INGEST EVERYTHING
# =========================

def ingest_all():
    print("🚀 Starting ingestion...\n")

    # Load data
    note_docs, note_meta, note_ids = load_all_notes()
    diag_docs, diag_meta, diag_ids = load_all_diagrams()

    # Combine
    documents = note_docs + diag_docs
    metadatas = note_meta + diag_meta
    ids = note_ids + diag_ids

    if not documents:
        print("❌ No data found. Check your data folder.")
        return

    print(f"📦 Total documents loaded: {len(documents)}")

    # Generate embeddings
    embeddings = EMBED_MODEL.encode(documents).tolist()

    # 🔥 Clear existing DB (safe re-run)
    try:
        COLLECTION.delete(where={})
        print("🧹 Cleared existing collection")
    except:
        print("⚠️ Could not clear collection (might be empty)")

    # Add to DB
    COLLECTION.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )
    

    print("\n✅ Ingestion completed successfully!")
    print(f"📊 Notes: {len(note_docs)}")
    print(f"🖼️ Diagrams: {len(diag_docs)}")
    print(f"📦 Total stored: {len(documents)}")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    ingest_all()
