from groq import Groq
from rag_engine import split_text, create_vector_store, retrieve
from rag_pipeline import load_knowledge_base, retrieve_knowledge
from dotenv import load_dotenv
import os

load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔹 Load knowledge base once
kb_index, kb_chunks = load_knowledge_base()

def generate_questions(resume_text, role, num_questions=5):

    # ---------------- RESUME RAG ----------------
    resume_chunks = split_text(resume_text)
    resume_index, resume_chunks = create_vector_store(resume_chunks)

    resume_context = retrieve(f"{role} experience skills projects", resume_index, resume_chunks)

    # ---------------- KNOWLEDGE RAG ----------------
    knowledge_context = retrieve_knowledge(f"{role} interview questions", kb_index, kb_chunks)

    # ---------------- COMBINED CONTEXT ----------------
    context = "\n".join(resume_context + knowledge_context)

    # ---------------- LLM ----------------
    prompt = f"""
You are a professional AI interviewer.

Use the following CONTEXT to generate interview questions.

CONTEXT:
{context}

Generate {num_questions - 1} high-quality interview questions.

STRICT RULES:
- Each must be a complete question
- No headings
- No explanations
- Mix resume-based + role-based questions
- Avoid generic questions

Role: {role}
"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )

    raw_text = response.choices[0].message.content

    questions = []
    for line in raw_text.split("\n"):
        line = line.strip().lstrip("1234567890. ").strip()
        if "?" in line:
            questions.append(line)

    return ["Can you introduce yourself?"] + questions[:num_questions-1]