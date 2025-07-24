# AI-Resume-analysis
🧠 AI Resume Reviewer &amp; Score Generator (with Local Chatbot Support)



This project is a smart, privacy-focused AI tool that:

📄 Parses uploaded resumes (PDF/Docx)

🧠 Scores them based on structure, skills, and keywords

💬 Provides custom suggestions

🤖 Includes an offline AI Chatbot powered by Ollama to help improve resumes with real-time Q&A

🎯 Features
✅ Upload a resume file (PDF or Docx)

🧠 Get an AI-generated score and feedback

⚠️ Warns users if file doesn't look like a resume

💬 Ask resume-related questions to a local LLM bot (no internet required)

🖥 Built with Flask, Python, Ollama, and JavaScript

🛠 Tech Stack
Frontend: HTML, Tailwind CSS, JavaScript

Backend: Python (Flask)

AI Resume Scoring: Regex + NLP rules

Local Chatbot: Ollama + LLMs like tinyllama, phi3, mistral

File Handling: PyMuPDF, python-docx

structure of this project
resumeProject/
├── app.py                 # Flask server
├── resume_parser.py       # Resume scoring logic
├── templates/
│   └── index.html         # Main UI
├── static/
│   └── style.css, bot.js  # Styles and frontend logic

