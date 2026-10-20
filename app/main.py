from fastapi import FastAPI 
from app.api.routes.skills import router as skills_router
from app.api.routes.courses import router as courses_router

from app.api.routes.recommendations import router as recommendations_router

from app.api.routes.rag import router as rag_router

app=FastAPI(title="AI Course Recommender API",
version="0.1.0",)
app.include_router(skills_router)
app.include_router(courses_router)

app.include_router(recommendations_router)
app.include_router(rag_router)

@app.get("/health")

def health_check():
    return {"status": "healthy"}

    