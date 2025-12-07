# tests/e2e/test_frontend_e2e.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_landing_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "CS631 Personnel Portal" in response.text

def test_hr_page_navigation():
    response = client.get("/hr")
    assert response.status_code == 200
    assert "Human Resources" in response.text

def test_projects_page_navigation():
    response = client.get("/projects")
    assert response.status_code == 200
    assert "Project Management" in response.text