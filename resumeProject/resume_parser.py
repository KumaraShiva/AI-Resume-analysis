import pdfplumber
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(filepath):
    text = ''
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text.strip()

def is_resume(text):
    lines = text.lower().split('\n')

    section_headings = [
        "education", "experience", "work experience", "projects", "skills",
        "certifications", "summary", "objective", "achievements"
    ]

    heading_count = sum(1 for line in lines if any(heading in line.strip() for heading in section_headings))

    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone_match = re.search(r"(\+?\d{1,3})?[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}", text)

    return heading_count >= 2 and (email_match or phone_match)

def analyze_resume(text):
    suggestions = []
    feedback_bot = []

    if not is_resume(text):
        return None, [
            "❌ This does not appear to be a resume.",
            "📌 Include important sections like Education, Skills, Experience.",
            "📞 Add contact details such as email and phone number."
        ]

    doc = nlp(text)
    score = 0

    # EDUCATION
    if 'education' in text.lower():
        score += 20
    else:
        suggestions.append("Education section is missing.")
        feedback_bot.append("🎓 I couldn't find an Education section. Add your highest degree, university name, and passing year.")

    # EXPERIENCE
    if 'experience' in text.lower():
        score += 20
    else:
        suggestions.append("Experience section is missing.")
        feedback_bot.append("💼 You don’t seem to have an Experience section. Include internships, jobs, or college projects.")

    # SKILLS
    if 'skills' in text.lower():
        score += 20
    else:
        suggestions.append("Skills section is missing.")
        feedback_bot.append("🛠️ Skills section is important. Mention tools or technologies like Python, Excel, Communication, etc.")

    # PROJECTS
    if 'projects' in text.lower():
        score += 10
    else:
        suggestions.append("Projects section is missing.")
        feedback_bot.append("📁 Try including academic or personal projects to showcase your applied skills.")

    # CERTIFICATIONS
    if 'certifications' in text.lower():
        score += 10
    else:
        suggestions.append("Certifications section is missing.")
        feedback_bot.append("📜 Mention any certifications (Coursera, Udemy, etc.) to strengthen your profile.")

    # ENTITIES (names, orgs, dates)
    if len(doc.ents) > 10:
        score += 10
    else:
        suggestions.append("Not enough detailed information.")
        feedback_bot.append("🧾 Add dates, organization names, and places to give more clarity.")

    # LENGTH
    if len(text) > 1000:
        score += 10
    else:
        suggestions.append("Resume is too short.")
        feedback_bot.append("📝 Try expanding your resume to include more content — like responsibilities, achievements, or awards.")

    # Final score and feedback list
    return score, feedback_bot + suggestions
