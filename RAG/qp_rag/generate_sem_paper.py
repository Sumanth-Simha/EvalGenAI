import random
from collections import defaultdict
from RAG.qp_rag.retrieve_qp import predict_questions


# =========================
# CONFIG
# =========================

MARK_PATTERNS = [
    [6, 8, 6],
    [7, 7, 6],
    [5, 5, 10],
    [10, 10]
]


# =========================
# HELPER: GROUP BY MODULE + TOPIC
# =========================

def group_by_module(metas, docs):
    module_map = defaultdict(list)

    for doc, meta in zip(docs, metas):
        module = meta.get("module", "module 1")
        topic = meta.get("topic", "general")

        module_map[module].append({
            "question": doc,
            "topic": topic
        })

    return module_map


# =========================
# HELPER: PICK MARK PATTERN
# =========================

def choose_pattern(topics):
    unique_topics = len(set(topics))

    # 🔥 your rule
    if unique_topics <= 2:
        return random.choice([[10, 10], [7, 7, 6]])
    else:
        return random.choice(MARK_PATTERNS)


# =========================
# HELPER: BUILD SUBPARTS
# =========================

def build_subparts(questions, pattern):
    parts = []

    for i, marks in enumerate(pattern):
        if i < len(questions):
            q = questions[i]
        else:
            q = questions[0]

        parts.append((q, marks))

    return parts


# =========================
# BUILD ONE MODULE
# =========================

def build_module(module_name, questions):
    random.shuffle(questions)

    topics = [q["topic"] for q in questions]

    pattern1 = choose_pattern(topics)
    pattern2 = choose_pattern(topics[::-1])

    q1_parts = build_subparts([q["question"] for q in questions[:3]], pattern1)
    q2_parts = build_subparts([q["question"] for q in questions[3:6]], pattern2)

    return q1_parts, q2_parts


# =========================
# FORMAT PAPER
# =========================

def format_sem_paper(module_map):
    paper = "📝 IOT SEM END MODEL PAPER\n\n"
    paper += "Time: 3 Hours\nMax Marks: 100\n\n"
    paper += "-------------------------------------\n\n"

    q_counter = 1

    for module, questions in sorted(module_map.items()):
        paper += f"📘 {module.upper()} (20 Marks)\n\n"

        q1, q2 = build_module(module, questions)

        # Q1
        paper += f"Q{q_counter}.\n"
        for idx, (q, marks) in enumerate(q1):
            label = chr(97 + idx)
            paper += f"{label}) {q} ({marks} Marks)\n"
        paper += "\nOR\n\n"
        q_counter += 1

        # Q2
        paper += f"Q{q_counter}.\n"
        for idx, (q, marks) in enumerate(q2):
            label = chr(97 + idx)
            paper += f"{label}) {q} ({marks} Marks)\n"

        paper += "\n-------------------------------------\n\n"
        q_counter += 1

    return paper


# =========================
# MAIN FUNCTION
# =========================

def generate_sem_paper(query):
    # 🔥 get more data
    results = predict_questions(query, top_k=40)

    # results = [(doc, score)]
    docs = [r[0] for r in results]
    metas = [r[1] if isinstance(r[1], dict) else {} for r in results]

    # ⚠️ if your predict doesn't return meta, fix that separately

    module_map = group_by_module(metas, docs)

    return format_sem_paper(module_map)
