"""
EduGenie - Google Gemini Powered Learning Assistant
Single-file Streamlit application.

Setup:
1. pip install streamlit google-genai python-dotenv
2. Create a .env file containing:
   GEMINI_API_KEY=your_api_key_here
3. Run:
   streamlit run EduGenie.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

st.set_page_config(
    page_title="EduGenie",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduGenie")
st.caption("Google Gemini Powered Learning Assistant")

if not API_KEY:
    st.error(
        "Gemini API key not found. Create a .env file in the same folder "
        "with GEMINI_API_KEY=your_api_key_here"
    )
    st.stop()

client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text or "Sorry, no response was generated."
    except Exception as e:
        return f"Gemini API error: {e}"


def tutor_prompt(question, level):
    return f"""
You are EduGenie, a friendly AI tutor.

Student level: {level}
Question: {question}

Answer clearly and accurately.
Explain step by step when appropriate.
Use simple examples.
Help the student understand instead of only giving a final answer.
"""


def explanation_prompt(topic, level):
    return f"""
You are EduGenie, an educational AI assistant.

Explain this concept to a {level}-level student:

{topic}

Use this structure:
1. Simple definition
2. Detailed explanation
3. Real-world example
4. Important points
5. One quick practice question
"""


def summary_prompt(material, level):
    return f"""
You are EduGenie, a study-notes assistant.

Summarize the following material for a {level}-level student:

{material}

Provide:
- Short overview
- Key points
- Important terms and definitions
- Exam/revision points
- 3 quick review questions
"""


def quiz_prompt(topic, count, difficulty):
    return f"""
You are EduGenie, an educational quiz generator.

Create {count} multiple-choice questions about:
Topic: {topic}
Difficulty: {difficulty}

For every question provide:
- Question
- Four options A, B, C, D
- Correct answer
- Short explanation

Do not repeat questions.
Make every answer factually accurate.
"""


with st.sidebar:
    st.header("📚 Learning Tools")

    mode = st.selectbox(
        "Choose a tool",
        [
            "AI Tutor",
            "Concept Explainer",
            "Summarizer",
            "Quiz Generator",
            "Study Planner"
        ]
    )

    level = st.selectbox(
        "Learning Level",
        ["Beginner", "Intermediate", "Advanced"]
    )


if mode == "AI Tutor":
    st.subheader("💬 AI Tutor")

    question = st.text_area(
        "Ask your question",
        placeholder="Example: Explain Newton's second law."
    )

    if st.button("Ask EduGenie", type="primary"):
        if question.strip():
            with st.spinner("Thinking..."):
                st.markdown(ask_gemini(tutor_prompt(question, level)))
        else:
            st.warning("Please enter a question.")


elif mode == "Concept Explainer":
    st.subheader("📖 Concept Explainer")

    topic = st.text_input(
        "Enter a concept",
        placeholder="Example: Photosynthesis"
    )

    if st.button("Explain Concept", type="primary"):
        if topic.strip():
            with st.spinner("Generating explanation..."):
                st.markdown(ask_gemini(explanation_prompt(topic, level)))
        else:
            st.warning("Please enter a concept.")


elif mode == "Summarizer":
    st.subheader("📝 Study Material Summarizer")

    material = st.text_area(
        "Paste your study material",
        height=300
    )

    if st.button("Summarize", type="primary"):
        if material.strip():
            with st.spinner("Creating notes..."):
                st.markdown(ask_gemini(summary_prompt(material, level)))
        else:
            st.warning("Please enter study material.")


elif mode == "Quiz Generator":
    st.subheader("❓ Quiz Generator")

    topic = st.text_input(
        "Quiz Topic",
        placeholder="Example: Python Programming"
    )

    count = st.slider(
        "Number of Questions",
        min_value=1,
        max_value=10,
        value=5
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("Generate Quiz", type="primary"):
        if topic.strip():
            with st.spinner("Generating quiz..."):
                st.markdown(
                    ask_gemini(
                        quiz_prompt(topic, count, difficulty)
                    )
                )
        else:
            st.warning("Please enter a quiz topic.")


elif mode == "Study Planner":
    st.subheader("🎯 Personalized Study Planner")

    subject = st.text_input("Subject")

    topics = st.text_area(
        "Topics to study",
        placeholder="Chapter 1\nChapter 2\nChapter 3"
    )

    hours = st.number_input(
        "Available hours per day",
        min_value=1,
        max_value=12,
        value=2
    )

    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=30,
        value=7
    )

    if st.button("Create Study Plan", type="primary"):
        if subject.strip() and topics.strip():
            prompt = f"""
You are EduGenie, a personalized study planner.

Create a realistic study plan.

Subject: {subject}

Topics:
{topics}

Available study time: {hours} hours per day
Duration: {days} days
Student level: {level}

Include:
1. Day-by-day schedule
2. Topics for each day
3. Revision sessions
4. Practice/test sessions
5. Short study tips

Make the plan practical and easy to follow.
"""

            with st.spinner("Creating study plan..."):
                st.markdown(ask_gemini(prompt))
        else:
            st.warning("Please enter the subject and topics.")


st.divider()
st.caption("EduGenie • AI-powered educational assistance")
