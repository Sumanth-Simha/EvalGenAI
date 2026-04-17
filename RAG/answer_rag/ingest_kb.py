import os
import json
from sentence_transformers import SentenceTransformer
from utils.db import get_chroma_client

# =========================
# CONFIG
# =========================

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

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
# LOAD ALL DIAGRAMS (FIXED 🔥)
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
                    # 🔥 HANDLE BOTH JSON FORMATS (caption/title safe)
                    title = d.get("title") or d.get("topic", "Diagram")
                    description = d.get("description") or d.get("caption", "")

                    doc_text = f"{title}. {description}"

                    documents.append(doc_text)

                    # 🔥 FORCE CORRECT IMAGE PATH
                    filename = os.path.basename(d.get("image_path", ""))

                    correct_path = os.path.join(
                        "data", "iot", module, "diagrams", "images", filename
                    )

                    metadatas.append({
                        "type": "diagram",
                        "topic": d.get("topic", ""),
                        "module": module,
                        "image_path": correct_path,   # ✅ FIXED HERE
                        "title": title
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

    note_docs, note_meta, note_ids = load_all_notes()
    diag_docs, diag_meta, diag_ids = load_all_diagrams()

    documents = note_docs + diag_docs
    metadatas = note_meta + diag_meta
    ids = note_ids + diag_ids

    if not documents:
        print("❌ No data found. Check your data folder.")
        return

    print(f"📦 Total documents loaded: {len(documents)}")

    embeddings = EMBED_MODEL.encode(documents).tolist()

    # clear old DB
    try:
        COLLECTION.delete(where={})
        print("🧹 Cleared existing collection")
    except:
        print("⚠️ Could not clear collection (might be empty)")

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