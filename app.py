import hashlib

# Patch for OpenSSL issue
original_md5 = hashlib.md5

def fixed_md5(*args, **kwargs):
    kwargs.pop("usedforsecurity", None)
    return original_md5(*args, **kwargs)

hashlib.md5 = fixed_md5

from flask import Flask, render_template, request, send_file
import random
from questions import questions_db
from evaluator import evaluate_answer
from report import generate_report

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

app = Flask(__name__)

def extract_text_from_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def match_skills_tfidf(resume_text):
    skills = list(questions_db.keys())
    corpus = skills + [resume_text]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)

    similarity = cosine_similarity(vectors[-1], vectors[:-1])

    return [skills[i] for i, s in enumerate(similarity[0]) if s > 0.1]


@app.route("/", methods=["GET", "POST"])
def home():
    questions = []
    detected_skills = []

    if request.method == "POST":
        level = request.form["level"]
        num = int(request.form["num_questions"])

        if request.form.get("skills"):
            detected_skills = request.form["skills"].lower().split(",")

        elif "resume" in request.files:
            file = request.files["resume"]
            if file:
                text = extract_text_from_pdf(file)
                detected_skills = match_skills_tfidf(text)

        all_q = []
        for skill in detected_skills:
            skill = skill.strip()
            if skill in questions_db:
                all_q.extend(questions_db[skill][level])

        questions = random.sample(all_q, min(len(all_q), num))

    return render_template("index.html", questions=questions)


@app.route("/evaluate", methods=["POST"])
def evaluate():
    questions = request.form.getlist("questions")
    answers = request.form.getlist("answers")

    results = []
    total = 0

    for q, a in zip(questions, answers):
        score = evaluate_answer(q, a)
        total += score
        results.append({"question": q, "answer": a, "score": score})

    avg = round(total / len(results), 2)

    generate_report(results, avg)

    return render_template("dashboard.html",
                           results=results,
                           avg_score=avg)


@app.route("/download")
def download():
    return send_file("report.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)