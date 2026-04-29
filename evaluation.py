from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def evaluate_answer(question, answer):
    prompt = f"""
You are a professional interviewer.

Evaluate the candidate's answer strictly.

Question:
{question}

Answer:
{answer}

Give output EXACTLY in this format:

Score: X/10

Strengths:
- point 1
- point 2

Weaknesses:
- point 1
- point 2

Correct Answer:
(clear ideal answer)

Improvement Tip:
(one short suggestion)
"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )

    return response.choices[0].message.content