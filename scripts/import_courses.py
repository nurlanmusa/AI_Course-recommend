from csv import DictReader
from pathlib import Path 

from app.db.session import SessionLocal 
from app.models.course import Course 
from app.schemas.courses import CourseCreate 

CSV_FILE = Path("data/courses.csv")

def import_courses():
    courses = []
    
    with CSV_FILE.open(
        mode = "r",
        encoding = "utf-8-sig",
        newline = "",) as csv_file: 

        rows=DictReader(csv_file)
        for row in rows:
            course_data = CourseCreate(
                title=row["title"].strip(),
                description=row["description"].strip(),
                provider=row["provider"].strip() or None,
                url=row["url"].strip() or None,
            )

            courses.append(Course(**course_data.model_dump()))
    
    with SessionLocal() as database_session:
        database_session.add_all(courses)
        database_session.commit()
    
    print(f"Imported {len(courses)} courses.")

if __name__=="__main__":
    import_courses()