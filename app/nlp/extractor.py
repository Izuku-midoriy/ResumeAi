# NLP skill/entity extraction will be implemented here.
#
# Planned:
# - Skill extraction
# - Education extraction
# - Experience extraction
# - Project extraction
# - Certification extraction
# - Named Entity Recognition
import re


# Skills that our system can currently recognize
SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "html",
    "css",
    "react",
    "node.js",
    "nodejs",
    "django",
    "flask",
    "fastapi",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "jenkins",
    "devops",
    "data science",
    "data analysis",
]


def normalize_text(text):
    """Clean and normalize resume text."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text):
    """Extract known technical skills from resume text."""
    normalized_text = normalize_text(text)

    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return sorted(found_skills)


def extract_email(text):
    """Extract email address."""
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:com|in|org|net|edu|gov|io|co|me|ai|info|dev|tech|[A-Za-z]{2,4})\b"

    match = re.search(pattern, text, flags=re.IGNORECASE)

    if match:
        return match.group(0)

    return None


def extract_phone(text):
    """Extract phone number."""
    # Matches a wide variety of international and local phone number formats
    pattern = r"(?:(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\b\d{10}\b|\+?\d{2,3}[\s.-]?\d{4,5}[\s.-]?\d{4,5})"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def find_section(text, section_name):
    """Extract text belonging to a resume section."""

    pattern = (
        rf"{section_name}\s*:?\s*"
        rf"(.*?)(?="
        rf"\b(?:skills|education|experience|work experience|"
        rf"projects|certifications|achievements|"
        rf"summary|profile|objective)\b|$)"
    )

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def extract_resume_information(text):
    """Extract structured information from a resume."""

    information = {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": find_section(text, "education"),
        "experience": find_section(text, "experience"),
        "projects": find_section(text, "projects"),
        "certifications": find_section(text, "certifications"),
    }

    return information