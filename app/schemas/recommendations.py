from pydantic import BaseModel, Field

class RecommendationRequest(BaseModel):
    skill: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)

class CourseMatch(BaseModel):
    id: int
    title: str
    description: str
    provider: str|None
    url: str|None
    similarity: float 

class RecommendationResponse(BaseModel):
    skill: str
    courses: list[CourseMatch]

class RagRecommendationResponse(BaseModel):
    skill: str
    answer: str
    sources: list[CourseMatch]
    