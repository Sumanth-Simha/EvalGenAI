# agent/classifier.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)


# =========================
# RULE-BASED CLASSIFIER
# =========================

def rule_based(query: str):
    q = query.lower()

    if any(word in q for word in ["predict", "important questions", "likely questions"]):
        return "predict"

    if any(word in q for word in ["explain", "what is", "define", "describe"]):
        return "answer"

    return None


# =========================
# LLM CLASSIFIER (SAFE)
# =========================

def llm_classify(query: str):
    prompt = f"""
You are a classifier.

Classify the user query into ONE of the following categories:
1. answer
2. predict

Query: "{query}"

Respond with ONLY one word: answer OR predict
"""

    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content(prompt)

        result = response.text.strip().lower()

        if "predict" in result:
            return "predict"

        return "answer"

    except Exception as e:
        print("⚠️ LLM classification failed:", e)

        # 🔥 FALLBACK (VERY IMPORTANT)
        return "answer"


# =========================
# FINAL CLASSIFIER
# =========================

def classify(query: str):
    # 🔥 Step 1: fast rule-based
    result = rule_based(query)

    if result:
        return result

    # 🔥 Step 2: LLM fallback
    return llm_classify(query)
