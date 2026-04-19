import random
import json
import os

BASE_PATH = "data/iot/superset/all_questions.json"

MARK_PATTERNS = [
    [6, 8, 6],
    [7, 7, 6],
    [5, 5, 10],
    [10, 10]
]


# =========================
# LOAD MODULE-WISE QUESTIONS
# =========================

def load_module_questions():
    if not os.path.exists(BASE_PATH):
        return {}

    with open(BASE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    module_map = {}

    for module in data:
        module_name = module.get("module", "Unknown")

        questions = [
            q["q"] for q in module.get("questions", [])
            if "q" in q and q["q"].strip()
        ]

        module_map[module_name] = questions

    return module_map


# =========================
# HELPERS
# =========================

def choose_pattern():
    return random.choice(MARK_PATTERNS)


def split_questions(questions, pattern):
    if not questions:
        questions = ["Explain IoT framework"]

    parts = []
    for i, marks in enumerate(pattern):
        q = questions[i % len(questions)]
        parts.append((q, marks))

    return parts


# =========================
# MAIN GENERATOR
# =========================

def generate_sem_paper(query):
    module_map = load_module_questions()

    paper = "📝 IOT SEM END MODEL PAPER\n\n"
    paper += "Time: 3 Hours\nMax Marks: 100\n\n"
    paper += "-------------------------------------\n\n"

    q_counter = 1

    for module, questions in module_map.items():

        if not questions:
            questions = ["Explain IoT concepts"] * 10

        random.shuffle(questions)

        # ensure enough
        if len(questions) < 10:
            questions = (questions * 3)[:10]

        paper += f"📘 {module} (20 Marks)\n\n"

        q1_input = questions[:5]
        q2_input = questions[5:10]

        p1 = choose_pattern()
        p2 = choose_pattern()

        q1 = split_questions(q1_input, p1)
        q2 = split_questions(q2_input, p2)

        # Q1
        paper += f"Q{q_counter}.\n"
        for i, (q, marks) in enumerate(q1):
            label = chr(97 + i)
            paper += f"{label}) {q} ({marks} Marks)\n"

        paper += "\nOR\n\n"
        q_counter += 1

        # Q2
        paper += f"Q{q_counter}.\n"
        for i, (q, marks) in enumerate(q2):
            label = chr(97 + i)
            paper += f"{label}) {q} ({marks} Marks)\n"

        paper += "\n-------------------------------------\n\n"
        q_counter += 1

    return paper