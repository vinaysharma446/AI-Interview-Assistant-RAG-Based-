import streamlit as st
from resume_parser import extract_text
from resume_analyzer import analyze_resume
from interview_engine import generate_questions
from voice_module import record_audio, speech_to_text, speak
from evaluation import evaluate_answer
from groq import Groq
from dotenv import load_dotenv
import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv()

# ---------------- LOAD ENV ----------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Interview Assistant")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>🤖 AI Interview Assistant</h1>
<p style='text-align:center;color:gray;'>Practice interviews with AI (voice + text)</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🎯 Interview Dashboard")

    if "questions" in st.session_state:
        st.write(f"Progress: {st.session_state.q_index}/{len(st.session_state.questions)}")

    st.markdown("---")

    if st.button("🔄 Restart Interview"):
        st.session_state.clear()

# ---------------- FINAL REPORT ----------------
def generate_final_report(questions, answers):
    combined = ""
    for q, a in zip(questions, answers):
        combined += f"Q: {q}\nA: {a}\n\n"

    prompt = f"""
Analyze this interview:

{combined}

Give:
1. Overall Performance Summary
2. Strong Areas
3. Weak Areas
4. Improvement Plan
"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )

    return response.choices[0].message.content

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success("✅ Resume uploaded successfully!")
    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.write(resume_text[:1000])

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            result = analyze_resume(resume_text)
        st.subheader("🧠 AI Analysis")
        st.write(result)

    st.subheader("🎯 Select Role")
    role = st.selectbox("Choose your role", [
        "Data Analyst", "Machine Learning Engineer",
        "Data Scientist", "AI Engineer",
        "Business Analyst", "Software Engineer"
    ])

    if st.button("Start Interview"):
        st.session_state.questions = generate_questions(resume_text, role, 5)
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.session_state.last_spoken_q = -1
        st.session_state.voice_answer = ""

# ---------------- INTERVIEW LOOP ----------------
if "questions" in st.session_state:
    q_index = st.session_state.q_index
    questions = st.session_state.questions

    st.progress(min(q_index / len(questions), 1.0))
    st.markdown(f"### Question {min(q_index+1, len(questions))} / {len(questions)}")

    if q_index < len(questions):
        question = questions[q_index]
        clean_q = question.lstrip("1234567890. ").strip()

        # 🎨 Question Card
        st.markdown(f"""
        <div style="background:#f0f6ff;padding:15px;border-radius:10px;border-left:5px solid #4CAF50;">
        <b>Question {q_index+1}</b><br><br>{clean_q}
        </div>
        """, unsafe_allow_html=True)

        # Speak once
        if st.session_state.last_spoken_q != q_index:
            speak(clean_q)
            st.session_state.last_spoken_q = q_index

        text_answer = st.text_input("✍️ Your Answer", key=f"text_{q_index}")

        # 🎤 Voice
        if st.button("🎤 Record Answer", key=f"voice_{q_index}"):
            st.warning("🔴 Recording (30 sec)...")
            audio_file = record_audio(duration=30)
            voice_answer = speech_to_text(audio_file)

            st.session_state.voice_answer = voice_answer
            st.success("Voice captured!")
            st.write("🧑", voice_answer)

        # Submit
        if st.button("Submit Answer", key=f"submit_{q_index}"):
            final = text_answer or st.session_state.voice_answer

            if final:
                if len(st.session_state.answers) <= q_index:
                    st.session_state.answers.append(final)
                else:
                    st.session_state.answers[q_index] = final

                st.success("Answer submitted!")
                st.session_state.voice_answer = ""
            else:
                st.warning("Provide an answer first")

        # Next
        if st.button("Next Question", key=f"next_{q_index}"):
            if len(st.session_state.answers) <= q_index:
                st.warning("Submit answer first")
            else:
                st.session_state.q_index += 1

    # ---------------- RESULTS ----------------
    else:
        st.success("🎉 Interview Completed!")

        total = 0

        for i, ans in enumerate(st.session_state.answers):
            st.markdown(f"### Question {i+1}")
            st.write("❓", questions[i])
            st.write("🧑", ans)

            with st.spinner("Evaluating..."):
                feedback = evaluate_answer(questions[i], ans)

            with st.expander("📌 Feedback"):
                st.write(feedback)

            try:
                score = int(feedback.split("Score:")[1].split("/")[0].strip())
                total += score
            except:
                pass

        avg = total / len(st.session_state.answers)
        st.markdown(f"""
        <div style="background:#e8f5e9;padding:20px;border-radius:10px;text-align:center;">
        <h2>🎯 Final Score: {avg:.1f}/10</h2>
        </div>
        """, unsafe_allow_html=True)

        # Final Report
        st.subheader("🧠 Final AI Report")

        try:
            report = generate_final_report(questions, st.session_state.answers)
            st.write(report)

            st.download_button("📄 Download Report", report, "report.txt")

        except Exception as e:
            st.error("Report generation failed (check API key)")