from ollama import chat


MODEL_NAME = "qwen3:8b"


def ask_llm(question):
    """
    Send a question to the local Qwen3 model
    and return its response.
    """

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.message.content


def generate_insight(question, result):
    """
    Generate a concise explanation from the database result.

    The LLM is only responsible for wording.
    It must not calculate or invent data.
    """

    prompt = f"""
You are a professional data analyst.

USER QUESTION:
{question}

DATABASE RESULT:
{result}

IMPORTANT:
The database result above is the ONLY source of truth.

All monetary values are in Indian Rupees (INR).

Your job is ONLY to explain the database result
in natural language.

STRICT RULES:

1. Do NOT calculate new values.
2. Do NOT invent values.
3. Do NOT omit important rows when summarizing rankings.
4. Do NOT change the order of values.
5. Use the exact names and numbers from the database result.
6. Use ₹ for monetary values.
7. Never use $, USD, or dollars.
8. Do not mention SQL, Python, databases, or programming.
9. Keep the answer concise: 1-2 sentences.
10. If the result contains a ranking, preserve the ranking exactly.

Answer ONLY with the business explanation.
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content.strip()


# ==========================================
# TEST INSIGHT GENERATION
# ==========================================

if __name__ == "__main__":

    question = "Which product generated the highest revenue?"

    result = """
product_name     total_revenue
Gaming Laptop   71630000
"""

    insight = generate_insight(
        question,
        result
    )

    print("\nAI Insight:")
    print(insight)