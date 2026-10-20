from fastapi import APIRouter, Depends, status 
from sqlalchemy.orm import Session 
from sqlalchemy import select

from app.db.session import get_db 
from app.models.course import Course 
from app.schemas.courses import CourseCreate, CourseResponse 

router = APIRouter(prefix="/api/v1/courses",
tags=["Courses"],)

@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)

def create_course(course_data: CourseCreate,
                database_session: Session=Depends(get_db),)->CourseResponse:
                
                course = Course(**course_data.model_dump())

                database_session.add(course)
                database_session.commit()
                database_session.refresh(course)
                return course

@router.get("", response_model=list[CourseResponse])
def list_courses(database_session: Session = Depends(get_db),
                offset: int=0,
                limit: int=20,)-> list[CourseResponse]:

                statement=(select(Course).order_by(Course.id).offset(offset).limit(limit))

                courses=database_session.scalars(statement).all()
                return list(courses)