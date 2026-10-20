from datetime import datetime

from pydantic import BaseModel, ConfigDict

class CourseCreate(BaseModel):
    title: str
    description: str
    provider: str|None=None
    url: str|None=None

class CourseResponse(CourseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int 
    created_at: datetime 