from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

# ✅ USE GROQ CLIENT (NOT OPENAI)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(text):
    prompt = f"""
    Extract the following from this resume:

    1. Skills
    2. Projects
    3. Education

    Resume:
    {text}

    Give output in this format:

    Skills:
    Projects:
    Education:
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
    )

    return response.choices[0].message.content