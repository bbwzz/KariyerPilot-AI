import os
import random
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

PROFILES = {
    "AI Engineer": ["python", "machine learning", "deep learning", "numpy", "pandas", "scikit-learn"],
    "Data Analyst": ["excel", "sql", "python", "power bi", "statistics", "tableau"],
    "Backend Developer": ["python", "fastapi", "sql", "api", "docker", "git"],
    "NLP Engineer": ["python", "nlp", "transformers", "llm", "text processing", "huggingface"],
    "Computer Vision Engineer": ["python", "opencv", "deep learning", "pytorch", "image processing"],
    "Cybersecurity Analyst": ["linux", "networking", "wireshark", "python", "penetration testing"],
    "Mobile Developer": ["flutter", "dart", "swift", "kotlin", "git", "api"],
    "Cloud Engineer": ["aws", "docker", "kubernetes", "linux", "terraform", "git"],
    "DevOps Engineer": ["linux", "docker", "jenkins", "kubernetes", "cicd", "git", "ansible"],
    "Automation Developer": ["python", "selenium", "bash", "linux", "git", "robot framework"]
}

VOCAB = sorted(list(set(s for sub in PROFILES.values() for s in sub)))
DB_PATH = "synthetic_data.csv"


def vectorize(user_skills):
    vec = [0] * len(VOCAB)
    user_skills = [s.strip().lower() for s in user_skills]
    for s in user_skills:
        if s in VOCAB:
            vec[VOCAB.index(s)] = 1
    return vec


def get_scores(user_skills):
    user_set = set(s.strip().lower() for s in user_skills)
    res = {}
    for role, reqs in PROFILES.items():
        role_set = set(reqs)
        inter = len(user_set & role_set)
        union = len(user_set | role_set)
        res[role] = round((inter / union) * 100, 1) if union > 0 else 0.0
    return dict(sorted(res.items(), key=lambda x: x[1], reverse=True))


def get_gap(user_skills, role):
    if role not in PROFILES:
        return []
    user_set = set(s.strip().lower() for s in user_skills)
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


def get_cluster(user_skills):
    init_mock_data()
    df = pd.read_csv(DB_PATH)

    # Fixed seed protects the UI from wildly remapping cluster definitions on hot reloads
    model = KMeans(n_clusters=5, random_state=42, n_init="auto")
    model.fit(df.values)

    user_vec = np.array(vectorize(user_skills)).reshape(1, -1)
    idx = model.predict(user_vec)[0]

    mapping = {
        0: "The Intelligent Systems Architect (AI/ML Focus)",
        1: "The Core Infrastructure Guardian (Cloud/DevOps Focus)",
        2: "The Modern Product Architect (Web/Mobile Focus)",
        3: "The Data Insights Strategy Pilot (Analytics Focus)",
        4: "The Security & Automation Investigator (Cyber/Scripting Focus)"
    }
    return mapping.get(idx, "The General Technologist")