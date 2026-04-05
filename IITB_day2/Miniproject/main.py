import os
from parse_resumes import parse_resume
from text_cleaner import clean_text
from vectorizer import vectorize_texts
from matcher import match_resume

resume_path = r"F:\resume_skill_data\resumes\data_scientist\data_scientist_0.pdf"

job_description = """
Looking for a Data Scientist with Python, Machine Learning,
statistics, pandas, numpy, and model deployment experience.
"""

resume_text = clean_text(parse_resume(resume_path))
job_text = clean_text(job_description)

X, vec = vectorize_texts([resume_text, job_text])

score = match_resume(X[0:1], X[1:2])
print(f"\nResume Match Score: {score}%")
