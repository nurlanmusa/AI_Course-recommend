from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_extract_skills():
    response = client.post("/api/v1/skills/extract", 
    json={"text": "Experience with Python, SQL, Fastapi and Docker."},)
    assert response.status_code==200
    assert response.json() == {"skills": ["Python", "SQL", "FastAPI", "Docker"],
    "skill_count": 4,}

def test_rejects_empty_text():
    response = client.post("/api/v1/skills/extract", json={"text": ""},)
    assert response.status_code == 422