from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "CS631 Personnel Portal" in response.text

def test_hr_route():
    response = client.get("/hr")
    assert response.status_code == 200
    assert "Human Resources Management" in response.text

def test_projects_route():
    response = client.get("/projects")
    assert response.status_code == 200
    assert "Project Management" in response.text