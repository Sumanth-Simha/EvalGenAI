def build_pairs(questions):
    pairs = []

    for i in range(0, min(len(questions), 10), 2):
        if i + 1 < len(questions):
            pairs.append({
                "a": questions[i],
                "b": questions[i + 1]
            })

    return pairs[:5]


def format_ia_paper(pairs):
    paper = "📝 IOT IA MODEL PAPER\n\n"

    for i, pair in enumerate(pairs, 1):
        paper += f"Q{i}.\n"
        paper += f"a) {pair['a']}\n"
        paper += f"OR\n"
        paper += f"b) {pair['b']}\n\n"

    return paper
