import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

from app.db.session import get_db
from app.schemas.recommendations import (CourseMatch, RagRecommendationResponse, RecommendationRequest)
from app.services.course_search import search_courses 
from app.services.llm_service import generate_answer

router = APIRouter(prefix = "/api/v1/rag", tags=["RAG"],)

@router.post(
    "/recommendations",
    response_model = RagRecommendationResponse
)

def generate_rag_recommendation(
    request: RecommendationRequest,
    database_session: Session = Depends(get_db)
) -> RagRecommendationResponse:

    search_results = search_courses(
        database_session = database_session,
        skill = request.skill,
        limit = request.limit
    )

    sources = [
        CourseMatch(
            id=course.id,
            title=course.title,
            description=course.description,
            provider=course.provider,
            url=course.url,
            similarity=round(similarity, 4),
        )
        for course, similarity in search_results
    ]

    context = "\n\n".join(
        (
            f"Course: {source.title}\n"
            f"Description: {source.description}\n"
            f"Provider: {source.provider}\n"
            f"URL: {source.url}"
        )
        for source in sources
    )

    try:
        answer = generate_answer(
            question=f"I want to learn {request.skill}.",
            context= context,
        )
    except httpx.HTTPError as error:
        raise HTTPException(
            status_code = 503,
            detail="The local language model is unavailable; please try again later."
        ) from error
    
    return RagRecommendationResponse(
        skill=request.skill,
        answer = answer,
        sources = sources,
    )