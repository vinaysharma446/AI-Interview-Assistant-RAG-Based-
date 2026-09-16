# 🤖 AI Interview Assistant (RAG-Based)

An intelligent **AI-powered interview preparation platform** that simulates real interview scenarios using a candidate's resume.

The application combines **Retrieval-Augmented Generation (RAG)**, **Large Language Models (LLMs)**, **FAISS vector search**, and **voice interaction** to generate personalized interview questions and evaluate candidate responses.

---

## 🚀 Features

### ✨ Resume-Based Question Generation
- Upload your resume in PDF format.
- Extract relevant information from the resume.
- Generate role-specific interview questions.
- Questions are personalized according to the candidate's experience, skills, and projects.

### 🧠 RAG-Powered Intelligence
- Resume content is divided into meaningful chunks.
- Chunks are converted into vector embeddings.
- FAISS is used for efficient similarity search.
- Relevant resume context is retrieved before generating questions.
- Helps reduce generic questions and improves personalization.

### 🎤 Voice + Text Interaction
- Answer interview questions using text or voice.
- Speech-to-text support using Whisper.
- Text-to-speech support for interactive interview sessions.

### 📊 Answer Evaluation
- AI evaluates candidate answers.
- Provides feedback on the response.
- Identifies strengths and weaknesses.
- Generates a score based on answer quality and relevance.

### 📄 Final Performance Report
The application provides an overall interview report containing:
- Strengths
- Weaknesses
- Performance analysis
- Areas for improvement
- Suggestions for better interview preparation

---

## 🧩 Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Programming Language | Python |
| LLM | OpenAI GPT-OSS-20B via Groq API |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector Database | FAISS |
| RAG | Custom RAG Pipeline |
| Speech-to-Text | Whisper |
| Text-to-Speech | TTS |
| PDF Processing | Python PDF extraction libraries |

---

## 🏗️ Project Structure

```text
AI-Interview-Assistant-RAG-Based-
│
├── app.py                  # Main Streamlit application
├── interview_engine.py     # AI-based interview question generation
├── rag_engine.py           # Text chunking, embeddings and retrieval
├── rag_pipeline.py         # RAG-based knowledge retrieval pipeline
├── resume_analyzer.py      # Resume analysis and insights
├── evaluation.py           # Candidate answer evaluation
│
├── data/
│   └── interview_qa.txt    # Interview knowledge base
│
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Ignored files and secrets
└── .env                    # API credentials (local only)