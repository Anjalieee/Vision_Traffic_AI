import os
import random
from faker import Faker
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

fake = Faker()

BASE_DIR = r"F:\resume_skill_data\resumes"
RESUMES_PER_ROLE = 2   # realistic count for now

ROLES = {
    "data_scientist": ["Python", "machine learning", "statistics", "feature engineering"],
    "data_analyst": ["SQL", "data visualization", "business analysis"],
    "ml_engineer": ["model deployment", "pipelines", "CI/CD", "ML systems"],
    "backend_dev": ["REST APIs", "databases", "authentication", "scalability"],
    "frontend_dev": ["React", "UI performance", "CSS", "state management"],
    "non_tech": ["operations", "documentation", "stakeholder coordination"],
    "fresher": ["coursework", "academic projects", "internships"],
    "career_switcher": ["domain transition", "upskilling", "self-learning"]
}

FORMATS = ["pdf", "docx", "txt"]  # rotated per candidate


def generate_realistic_resume(role):
    name = fake.name()
    email = fake.email()
    education = random.choice([
        "B.Tech in Computer Engineering",
        "Bachelor of Information Technology",
        "B.Sc in Mathematics",
        "MBA (Operations)",
    ])

    company = fake.company()
    job_title = fake.job()
    duration = f"{random.randint(2019, 2022)} – {random.randint(2023, 2025)}"

    skills = random.sample(ROLES[role], k=min(3, len(ROLES[role])))

    experience = (
        f"Worked as {job_title} at {company} ({duration}). "
        f"Responsible for tasks involving {', '.join(skills)}. "
        f"Contributed to projects that improved efficiency by "
        f"{random.randint(10,40)}% through process optimization."
    )

    project = (
        f"Developed a project focused on {random.choice(skills)}, "
        f"handling real-world constraints and iterative improvements."
    )

    noise = random.choice([
        "Actively participates in workshops and hackathons.",
        "Enjoys mentoring peers and collaborative problem-solving.",
        "Continuously learning emerging tools and technologies."
    ])

    resume_text = f"""
{name}
Email: {email}

Education:
{education}

Experience:
{experience}

Projects:
{project}

Additional Information:
{noise}
"""

    return resume_text.strip()


def save_resume(path, text, fmt):
    if fmt == "txt":
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    elif fmt == "docx":
        doc = Document()
        for line in text.split("\n"):
            doc.add_paragraph(line)
        doc.save(path)

    elif fmt == "pdf":
        c = canvas.Canvas(path, pagesize=A4)
        width, height = A4
        y = height - 40
        for line in text.split("\n"):
            c.drawString(40, y, line)
            y -= 14
            if y < 40:
                c.showPage()
                y = height - 40
        c.save()


def generate_dataset():
    candidate_id = 0

    for role in ROLES:
        role_dir = os.path.join(BASE_DIR, role)
        os.makedirs(role_dir, exist_ok=True)

        for _ in range(RESUMES_PER_ROLE):
            text = generate_realistic_resume(role)
            fmt = FORMATS[candidate_id % len(FORMATS)]

            filename = f"{role}_{candidate_id}.{fmt}"
            save_resume(os.path.join(role_dir, filename), text, fmt)

            print(f"Generated: {filename}")
            candidate_id += 1


if __name__ == "__main__":
    generate_dataset()
