def match_skills(resume_text, jd_text, skills):
    matched = []

    for skill in skills:
        if skill in resume_text and skill in jd_text:
            matched.append(skill)

    score = len(matched)

    return {
        "score": score,
        "matched_skills": matched,
        "total_skills": len(skills)
    }
