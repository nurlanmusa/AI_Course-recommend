from sqlalchemy import select 

from app.db.session import SessionLocal
from app.models.course import Course 
from app.services.embedding_service import create_embeddings 

def generate_course_embeddings():
    with SessionLocal() as database_session:
        courses = database_session.scalars(select(Course).where(Course.embedding.is_(None))).all()

        if not courses:
            print("No courses need embeddings.")
            return
        
        course_texts = [
            f"{course.title}. {course.description}"
            for course in courses
        ]

        embeddings = create_embeddings(course_texts)

        for course, embedding in zip(courses, embeddings):
            course.embedding=embedding

        database_session.commit()

    print(f"Generated embedding for {len(courses)} courses")

if __name__=="__main__":
    generate_course_embeddings()