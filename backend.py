import os
import random
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

PROFILES = {
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NumPy", "Pandas", "Scikit-Learn"],
    "Data Analyst": ["Excel", "SQL", "Python", "Power BI", "Statistics", "Tableau"],
    "Backend Developer": ["Python", "FastAPI", "SQL", "API", "Docker", "Git"],
    "NLP Engineer": ["Python", "NLP", "Transformers", "LLM", "Text Processing", "HuggingFace"],
    "Computer Vision Engineer": ["Python", "OpenCV", "Deep Learning", "PyTorch", "Image Processing"],
    "Cybersecurity Analyst": ["Linux", "Networking", "Wireshark", "Python", "Penetration Testing"],
    "Mobile Developer": ["Flutter", "Dart", "Swift", "Kotlin", "Git", "API"],
    "Cloud Engineer": ["AWS", "Docker", "Kubernetes", "Linux", "Terraform", "Git"],
    "DevOps Engineer": ["Linux", "Docker", "Jenkins", "Kubernetes", "CI/CD", "Git", "Ansible"],
    "Automation Developer": ["Python", "Selenium", "Bash", "Linux", "Git", "Robot Framework"]
}

ARCHETYPES = [
    ("Data Enthusiast", lambda s: "Machine Learning" in s or ("Python" in s and "SQL" in s)),
    ("Frontend Leaning", lambda s: "React" in s or "JavaScript" in s),
    ("Infrastructure Focused", lambda s: "Docker" in s or "AWS" in s),
    ("Generalist Developer", lambda s: True),  # fallback
]

SKILL_WEIGHTS = {
    "Machine Learning": 2.0,
    "AWS": 1.8,
    "Docker": 1.5,
    "React": 1.5,
    "Python": 1.2,
    "JavaScript": 1.2,
    "Java": 1.2,
    "C#": 1.2,
    "SQL": 1.0,
    "Git": 0.8,  # table stakes — less differentiating
}

# Extract all unique skills and sort them alphabetically for the dropdown
VOCAB = sorted(list(set(s for sub in PROFILES.values() for s in sub)))
DB_PATH = "synthetic_data.csv"


def vectorize(user_skills):
    vec = [0] * len(VOCAB)
    user_skills = [s.strip() for s in user_skills]
    for s in user_skills:
        if s in VOCAB:
            vec[VOCAB.index(s)] = 1
    return vec


def get_gap(user_skills, role):
    if role not in PROFILES:
        return []
    user_set = set(s.strip() for s in user_skills)
    return sorted(list(set(PROFILES[role]) - user_set))


def init_mock_data():
    if os.path.exists(DB_PATH):
        return
    rows = []
    for _ in range(200):
        base = random.choice(list(PROFILES.values()))
        sample = random.sample(base, random.randint(3, len(base)))
        # Mix in random skills so the clustering centroids deal with messy real-world logic
        if random.random() > 0.4:
            sample.append(random.choice(VOCAB))
        rows.append(vectorize(sample))

    df = pd.DataFrame(rows, columns=VOCAB)
    df.to_csv(DB_PATH, index=False)


def get_cluster(user_skills: list[str]) -> str:
    """Assigns a developer persona based on current skill signals."""
    if not user_skills:
        return "Beginner (No Data)"
    skill_set = set(user_skills)
    for label, condition in ARCHETYPES:
        if condition(skill_set):
            return label


def get_scores(user_skills: list[str]) -> dict[str, float]:
    """Calculates weighted compatibility score for each career track."""
    user_set = set(user_skills)
    scores = {}
    for career, required in PROFILES.items():
        if not required:
            scores[career] = 0.0
            continue
        total_weight = sum(SKILL_WEIGHTS.get(s, 1.0) for s in required)
        matched_weight = sum(SKILL_WEIGHTS.get(s, 1.0) for s in required if s in user_set)
        scores[career] = round((matched_weight / total_weight) * 100, 1)

    # Sort the dictionary so the highest match is at the top of the UI
    return dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))