from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

profession_db = {
    "Software Engineer": ["Java", "Python", "C++", "OOP", "SQL", "Git", "DSA"],
    "Data Scientist": ["Python", "Machine Learning", "Statistics", "Pandas", "Deep Learning"],
    "AI Engineer": ["TensorFlow", "PyTorch", "NLP", "Neural Networks", "Deep Learning"],
    "Product Manager": ["Roadmap", "Agile", "Scrum", "User Stories", "Strategy"],
    "UI/UX Designer": ["Figma", "Wireframe", "Prototyping", "Design System", "User Research"],
    "Cybersecurity Analyst": ["Network Security", "Ethical Hacking", "SIEM", "Penetration Testing"],
    "Cloud Architect": ["AWS", "Azure", "GCP", "Cloud Architecture", "Terraform"],
    "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "Linux"],
    "Blockchain Developer": ["Solidity", "Ethereum", "Smart Contracts", "Web3"],
    "Research Scientist": ["Research Papers", "Deep Learning", "Computer Vision", "Experiments"]
}

def detect_experience_level(text):
    text = text.lower()
    years = re.findall(r'(\d+)\s+year', text)

    if years:
        y = max([int(i) for i in years])
        if y <= 1: return "Beginner"
        elif y <= 3: return "Intermediate"
        else: return "Advanced"

    if "intern" in text or "fresher" in text:
        return "Beginner"

    return "Intermediate"

def analyze_resume(resume_text):
    profession_texts = [" ".join(skills) for skills in profession_db.values()]
    documents = profession_texts + [resume_text]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)
    resume_vector = vectors[-1]

    scores = {}
    for i, profession in enumerate(profession_db.keys()):
        similarity = cosine_similarity(resume_vector, vectors[i])[0][0]
        scores[profession] = round(similarity * 100, 2)

    top_professions = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

    skill_count = {}
    for profession, skills in profession_db.items():
        skill_count[profession] = sum(skill.lower() in resume_text.lower() for skill in skills)

    return {
        "top_professions": top_professions,
        "experience": detect_experience_level(resume_text),
        "skill_count": skill_count
    }