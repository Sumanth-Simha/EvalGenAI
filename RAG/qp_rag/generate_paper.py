# RAG/qp_rag/generate_paper.py

def build_pairs(questions):
    pairs = []

    # remove duplicates while preserving order
    seen = set()
    clean_qs = []
    for q in questions:
        if q not in seen:
            clean_qs.append(q)
            seen.add(q)

    # ensure enough data
    if len(clean_qs) < 10:
        clean_qs = clean_qs * 3  # repeat if low data

    # build pairs
    for i in range(0, len(clean_qs) - 1, 2):
        pairs.append({
            "a": clean_qs[i],
            "b": clean_qs[i + 1]
        })

    return pairs[:5]  # IA = 5 questions


def format_ia_paper(pairs):
    paper = "📝 IOT IA MODEL PAPER\n\n"

    for i, pair in enumerate(pairs, 1):
        paper += f"Q{i}.\n"
        paper += f"a) {pair['a']}\n"
        paper += "OR\n"
        paper += f"b) {pair['b']}\n\n"

    return paper