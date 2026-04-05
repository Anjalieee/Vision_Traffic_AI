import os
import streamlit as st
import pandas as pd
from core.parser import extract_resume_text
from core.matcher import match_skills

# ---------- SETTINGS ----------
RESUMES_DIR = r"F:\resume_skill_data\resumes"  # change to your F: drive path
JOB_DESC_FILE = r"F:\resume_skill_data\job_descriptions\jd.txt"

# ---------- JOB DESCRIPTION LEVELS ----------
JD_LEVELS = {
    "junior": [
        "Python", "SQL", "data visualization", "statistics",
        "feature engineering", "documentation", "internships", "coursework"
    ],
    "associate": [
        "Python", "SQL", "machine learning", "data visualization",
        "databases", "REST APIs", "feature engineering", "UI performance"
    ],
    "senior": [
        "Python", "SQL", "machine learning", "model deployment",
        "CI/CD", "scalability", "databases", "team management", "project planning"
    ]
}

CATEGORY_TO_LEVEL = {
    "data_scientist": "associate",
    "data_analyst": "junior",
    "ml_engineer": "senior",
    "backend_dev": "associate",
    "frontend_dev": "associate",
    "non_tech": "junior",
    "fresher": "junior",
    "career_switcher": "junior"
}

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Resume Skill Matcher", layout="centered")
st.title("📄 Resume Skill Matcher")
st.write("All resumes are loaded automatically. Scoring is category + level specific.")

# ---------- Load Resumes ----------
resume_files = []
for root, dirs, files in os.walk(RESUMES_DIR):
    for file in files:
        if file.lower().endswith((".pdf", ".docx", ".txt")):
            resume_files.append(os.path.join(root, file))

if not resume_files:
    st.warning("No resumes found! Please check your resumes folder.")
else:
    st.success(f"Loaded {len(resume_files)} resumes.")

# ---------- Load Job Description ----------
if not os.path.exists(JOB_DESC_FILE):
    st.error(f"Job description file not found at {JOB_DESC_FILE}")
else:
    with open(JOB_DESC_FILE, "r", encoding="utf-8") as f:
        jd_text = f.read()

# ---------- Process Resumes ----------
results = []

for resume_path in resume_files:
    category = os.path.basename(os.path.dirname(resume_path))
    level = CATEGORY_TO_LEVEL.get(category, "junior")
    jd_skills = JD_LEVELS[level]

    resume_text = extract_resume_text(resume_path)

    result = match_skills(resume_text, jd_text, skills=jd_skills)

    results.append({
        "Resume Name": os.path.basename(resume_path),
        "Category": category,
        "Level": level,
        "Score (%)": result["score"],
        "Matched Skills": ", ".join(result["matched_skills"]),
        "Total Skills": result["total_skills"]
    })

# ---------- Display Results ----------
if results:
    df = pd.DataFrame(results)
    df_sorted = df.sort_values(by=["Level", "Score (%)"], ascending=[True, False])

    st.subheader("📄 Resume Match Results")
    st.dataframe(df, use_container_width=True)

    st.subheader("🏆 Ranked Resumes by Level")
    st.dataframe(df_sorted, use_container_width=True)
