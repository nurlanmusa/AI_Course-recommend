from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.course import Course
from app.services.embedding_service import create_embeddings

def search_courses(
    database_session: Session,
    skill: str,
    limit: int,
) -> list[tuple[Course, float]]:
    query_embedding = create_embeddings([skill])[0]

    distance = Course.embedding.cosine_distance(query_embedding).label("distance")

    statement = (
    select(Course, distance)
    .where(Course.embedding.is_not(None))
    .order_by(distance)
    .limit(limit)
)

    rows = database_session.execute(statement).all()

    return[
        (course, 1 - float(distance_value))
        for course, distance_value in rows
    ]
    