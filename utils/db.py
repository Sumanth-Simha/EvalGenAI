import os
from chromadb import PersistentClient

# 🔥 Absolute path to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_PATH = os.path.join(BASE_DIR, "chroma_db")

print("🔥 USING CHROMA DB AT:", DB_PATH)

def get_chroma_client():
    return PersistentClient(path=DB_PATH)