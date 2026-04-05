from parse_resumes import parse_resume
from text_cleaner import clean_text

path = r"F:\resume_skill_data\resumes\data_scientist\data_scientist_0.pdf"
raw = parse_resume(path)
cleaned = clean_text(raw)

print("\nRAW SAMPLE:\n", raw[:300])
print("\nCLEANED SAMPLE:\n", cleaned[:300])
