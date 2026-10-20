from pydantic import BaseModel, Field

class SkillExtractionRequest(BaseModel):
    text: str = Field(min_length=1, description= "CV or job ad text",)

class SkillExtractionResponse(BaseModel):
    skills: list[str]
    skill_count: int

    