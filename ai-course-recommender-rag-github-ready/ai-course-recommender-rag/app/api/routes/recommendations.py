from fastapi import APIRouter, Depends
from sqlalchemy import select 
from sqlalchemy.orm import Session 

from app.db.session import get_db 
from app.models.course import Course 
from app.schemas.recommendations import (
    CourseMatch,
    RecommendationRequest,
    RecommendationResponse,
)
from app.services.embedding_service import create_embeddings

router = APIRouter(prefix="/api/v1/recommendations",
                tags=["Recommendations"],)

@router.post("", response_model = RecommendationResponse)
def recommend_courses(request: RecommendationRequest, database_session: Session = Depends(get_db),)->RecommendationResponse:
    query_embedding = create_embeddings([request.skill])[0]

    distance = Course.embedding.cosine_distance(query_embedding).label("distance")

    statement = (
        select(Course, distance).where(Course.embedding.is_not(None)).order_by(distance).limit(request.limit))
    
    rows = database_session.execute(statement).all()

    matches = [
        CourseMatch(
            id=course.id,
            title=course.title,
            description=course.description,
            provider=course.provider,
            url=course.url,
            similarity=round(1-float(distance_value),4),
        )
        for course, distance_value in rows
    ]
    return RecommendationResponse(skill=request.skill, courses=matches,)