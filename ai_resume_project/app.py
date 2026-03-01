from flask import Flask, render_template, request, redirect, url_for
import os
from resume_parser import extract_text
from analyzer import analyze_resume

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    resume_file = request.files['resume']

    if resume_file.filename == "":
        return redirect(url_for('home'))

    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    resume_file.save(resume_path)

    resume_text = extract_text(resume_path)
    result = analyze_resume(resume_text)

    return render_template("results.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)