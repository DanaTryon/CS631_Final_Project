# tests/integration/test_employees_routes.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # If you have a test DB init function, call it here
    # For now, just ensure migrations are applied before tests
    # alembic upgrade head could be run in CI before pytest
    yield

def test_employees_json_list_empty():
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_employee_json():
    payload = {"name": "Alice", "title": "Engineer", "department": "R&D"}
    response = client.post("/employees", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["title"] == "Engineer"
    assert data["department"] == "R&D"

def test_employees_page_template():
    response = client.get("/employees_page")
    assert response.status_code == 200
    assert "<h1>Employee Directory</h1>" in response.text

def test_add_employee_form_submission():
    response = client.post(
        "/employees_page",
        data={"name": "Bob", "title": "Manager", "department": "HR"},
        follow_redirects=True
    )
    assert response.status_code == 200
    # After redirect, the page should contain the new employee
    assert "Bob" in response.text
    assert "Manager" in response.text
    assert "HR" in response.text