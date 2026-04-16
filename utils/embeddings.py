from sentence_transformers import SentenceTransformer


# =========================
# LOAD MODEL ONCE
# =========================

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


# =========================
# GENERATE EMBEDDINGS
# =========================

def embed_text(texts):
    model = get_model()

    if isinstance(texts, str):
        texts = [texts]

    return model.encode(texts).tolist()
