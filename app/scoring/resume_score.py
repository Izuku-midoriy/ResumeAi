# Resume/ATS scoring logic will be implemented here.
#
# Planned score components:
# - Skills
# - Experience
# - Education
# - Projects
# - Keywords
# - Resume structure

def calculate_resume_score(information, raw_text):
    """
    Calculate an ATS-style resume score out of 100.
    """

    score = 0
    breakdown = {}

    # -------------------------
    # 1. Contact Information
    # -------------------------

    contact_score = 0

    if information.get("email"):
        contact_score += 5

    if information.get("phone"):
        contact_score += 5

    score += contact_score
    breakdown["Contact Information"] = contact_score

    # -------------------------
    # 2. Skills
    # -------------------------

    skills = information.get("skills", [])

    if len(skills) >= 8:
        skill_score = 25
    elif len(skills) >= 5:
        skill_score = 20
    elif len(skills) >= 3:
        skill_score = 15
    elif len(skills) >= 1:
        skill_score = 10
    else:
        skill_score = 0

    score += skill_score
    breakdown["Skills"] = skill_score

    # -------------------------
    # 3. Education
    # -------------------------

    education = information.get("education", "")

    if education:
        education_score = 15
    else:
        education_score = 0

    score += education_score
    breakdown["Education"] = education_score

    # -------------------------
    # 4. Experience
    # -------------------------

    experience = information.get("experience", "")

    if experience:
        experience_score = 20
    else:
        experience_score = 0

    score += experience_score
    breakdown["Experience"] = experience_score

    # -------------------------
    # 5. Projects
    # -------------------------

    projects = information.get("projects", "")

    if projects:
        project_score = 15
    else:
        project_score = 0

    score += project_score
    breakdown["Projects"] = project_score

    # -------------------------
    # 6. Certifications
    # -------------------------

    certifications = information.get("certifications", "")

    if certifications:
        certification_score = 10
    else:
        certification_score = 0

    score += certification_score
    breakdown["Certifications"] = certification_score

    # -------------------------
    # 7. Resume Length
    # -------------------------

    word_count = len(raw_text.split())

    if word_count >= 500:
        length_score = 5
    elif word_count >= 300:
        length_score = 3
    else:
        length_score = 0

    score += length_score
    breakdown["Resume Content"] = length_score

    return score, breakdown


def get_score_category(score):
    """Convert numerical score into a category."""

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Good"

    if score >= 50:
        return "Average"

    return "Needs Improvement"
