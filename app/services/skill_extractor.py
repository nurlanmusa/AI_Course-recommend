import re

SKILL_CATALOGUE = [
    "Python",
    "SQL",
    "FastAPI",
    "Docker",
    "Git",
    "GitHub",
    "PostgreSQL",
    "Machine Learning",
    "Natural Language Processing",
]

def extract_skills(text: str) -> list[str]:
    found_skills=[]

    for skill in SKILL_CATALOGUE:
        pattern = rf"\b{re.escape(skill)}\b"

        if re.search(pattern, text, flags=re.IGNORECASE):
            found_skills.append(skill)
    return found_skills

