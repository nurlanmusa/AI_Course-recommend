from fastapi import APIRouter

from app.schemas.skills import (SkillExtractionResponse, SkillExtractionRequest)

from app.services.skill_extractor import extract_skills

router = APIRouter(prefix="/api/v1/skills", tags=["Skills"],)

@router.post("/extract", response_model=SkillExtractionResponse)

def extract_skills_from_text(request: SkillExtractionRequest,) -> SkillExtractionResponse:
    skills = extract_skills(request.text)
    return SkillExtractionResponse(skills=skills, skill_count=len(skills))

