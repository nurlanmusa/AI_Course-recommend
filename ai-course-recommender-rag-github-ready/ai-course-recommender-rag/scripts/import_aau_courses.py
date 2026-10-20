import json
import re
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.course import Course
from app.schemas.courses import CourseCreate


DATA_FILE = Path("data/raw/aau_courses.jsonl")
PROVIDER = "Åbo Akademi University"

PRIMARY_SECTIONS = {
    "Learning objectives and transferable skills",
    "Contents",
}

FALLBACK_SECTIONS = {
    "Further information",
}


def clean_text(text: str) -> str:
    return "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )


def extract_description(record: dict) -> str:
    sections = record["sections"]

    selected_texts = [
        clean_text(section["content"])
        for section in sections
        if section["section_name"] in PRIMARY_SECTIONS
        and section["content"].strip()
    ]

    if not selected_texts:
        selected_texts = [
            clean_text(section["content"])
            for section in sections
            if section["section_name"] in FALLBACK_SECTIONS
            and section["content"].strip()
        ]

    return "\n\n".join(selected_texts) or record["title"]


def load_unique_courses() -> dict[str, CourseCreate]:
    unique_courses = {}

    with DATA_FILE.open(encoding="utf-8") as data_file:
        for line in data_file:
            record = json.loads(line)

            title = record["title"].strip()
            url = record["course_url"].strip()

            # Exclude administrative records worth zero credits.
            if re.search(r",\s*0\s*ECTS\b", title, re.IGNORECASE):
                continue

            # The URL is our unique course identifier.
            unique_courses[url] = CourseCreate(
                title=title,
                description=extract_description(record),
                provider=PROVIDER,
                url=url,
            )

    return unique_courses


def import_courses():
    unique_courses = load_unique_courses()

    with SessionLocal() as database_session:
        existing_urls = set(
            database_session.scalars(
                select(Course.url).where(Course.url.is_not(None))
            ).all()
        )

        new_courses = [
            Course(**course_data.model_dump())
            for url, course_data in unique_courses.items()
            if url not in existing_urls
        ]

        database_session.add_all(new_courses)
        database_session.commit()

    print(f"Found {len(unique_courses)} unique valid courses.")
    print(f"Imported {len(new_courses)} new courses.")


if __name__ == "__main__":
    import_courses()