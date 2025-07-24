from flask import Flask, render_template, request
import os
from resume_parser import extract_text_from_pdf, analyze_resume

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask import jsonify
import subprocess
import requests
import json

@app.route('/ask-bot', methods=['POST'])
def ask_bot():
    user_input = request.json.get('question')
    print("QUESTION:", user_input)

    try:
        res = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "tinyllama",
                "prompt": user_input,
                "stream": False,
            },
            timeout=120
        )

        print("STATUS CODE:", res.status_code)
        print("RAW TEXT:", res.text)

        data = res.json()
        print("PARSED JSON:", data)

        return jsonify({'response': data.get("response", "⚠️ No meaningful reply")})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({'response': f"❌ Error: {str(e)}"})


@app.route('/', methods=['GET', 'POST'])
def index():
    text = ''
    score = None
    suggestions = []
    if request.method == 'POST':
        file = request.files['resume']
        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            text = extract_text_from_pdf(filepath)
            score, suggestions = analyze_resume(text)
    return render_template('index.html', text=text, score=score, suggestions=suggestions)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
