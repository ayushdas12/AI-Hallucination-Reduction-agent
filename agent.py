import os
import requests
from dotenv import load_dotenv
from verifier import verify_answer

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# -------------------------------
#  YOUR AGENT (UNCHANGED CORE)
# -------------------------------
def generate_answer(question):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a highly accurate AI assistant.

Rules:
- Do NOT guess
- If unsure, say "I am not confident"
- Give factual answers only

Question:
{question}
"""

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

    except Exception as e:
        answer = "I am not confident due to API error."

    verification = verify_answer(question, answer)

    return {
        "question": question,
        "answer": answer,
        "confidence": verification["confidence"],
        "verified": verification["verified"],
        "reason": verification["reason"]
    }


# -------------------------------
# NORMAL AI (NO SAFETY RULES)
# -------------------------------
def normal_ai_answer(question):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except:
        return "Error"


# -------------------------------
#  SCORE SYSTEM
# -------------------------------
def calculate_score(verified, answer):
    score = 10000

    if not verified:
        score -= 5000

    if "not confident" in answer.lower():
        score += 2000

    return score


# -------------------------------
#  MULTI QUESTION TEST
# -------------------------------
def run_tests():
    questions = [
        "Who is PM of USA?",
        "Capital of France?",
        "Who discovered gravity?",
        "President of India?",
        "Speed of light?"
    ]

    for q in questions:
        print("\n==============================")
        print(f"Question: {q}")

        normal = normal_ai_answer(q)
        agent = generate_answer(q)

        score = calculate_score(agent["verified"], agent["answer"])

        print("\n--- NORMAL AI ---")
        print(normal)

        print("\n--- YOUR AGENT ---")
        print(agent["answer"])

        print("\nVerified:", agent["verified"])
        print("Confidence:", agent["confidence"])
        print("Reason:", agent["reason"])
        print("Score:", score, "/ 10000")


# -------------------------------
#  MAIN MENU
# -------------------------------
if __name__ == "__main__":
    choice = input("1. Single Question\n2. Run Full Test\nChoose: ")

    if choice == "1":
        q = input("Enter your question: ")
        result = generate_answer(q)

        print("\n===== RESULT =====")
        for k, v in result.items():
            print(f"{k}: {v}")

    else:
        run_tests()