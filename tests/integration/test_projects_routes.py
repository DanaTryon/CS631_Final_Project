# tests/integration/test_projects_routes.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.employee import Employee
from app.models.job_history import JobHistory
from datetime import date


# --- Create Project ---
def test_create_project(client):
    payload = {
        "name": "Alpha",
        "budget": 1000,
        "start_date": "2025-01-01",
        "end_date": "2025-06-01",
        "manager_id": 1
    }
    resp = client.post("/projects", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    # Response keys are capitalized because of schema aliases
    assert data["Name"] == "Alpha"
    assert data["Budget"] == 1000
    assert data["ManagerID"] == 1
    assert "ProjectID" in data


# --- Assign Employee to Project ---
def test_assign_employee_to_project(client, test_db):
    # Create employee
    emp = Employee(Name="ProjUser", Title="Developer", OfficeID=1)
    test_db.add(emp)
    test_db.commit()

    # Create project
    project_payload = {"name": "Beta", "budget": 500, "manager_id": emp.EmpID}
    project_resp = client.post("/projects", json=project_payload)
    project_id = project_resp.json()["ProjectID"]

    # Assign employee
    assign_payload = {
        "emp_id": emp.EmpID,
        "project_id": project_id,
        "role": "Developer",
        "time_spent": 40
    }
    resp = client.post("/assign_project", data=assign_payload)
    assert resp.status_code in (200, 303)

    # Verify assignment appears
    page_resp = client.get("/projects")
    assert "Developer" in page_resp.text

# --- Add Milestone ---
def test_add_milestone(client, test_db):
    emp = Employee(Name="MilestoneUser", Title="Tester", OfficeID=1)
    test_db.add(emp)
    test_db.commit()

    project_payload = {"name": "Gamma", "budget": 750, "manager_id": emp.EmpID}
    project_resp = client.post("/projects", json=project_payload)
    project_id = project_resp.json()["ProjectID"]

    milestone_payload = {
        "description": "Design Phase",
        "status": "pending",
        "due_date": "2025-02-01",
        "project_id": project_id,
        "responsible_emp_id": emp.EmpID
    }
    resp = client.post("/add_milestone", data=milestone_payload)
    assert resp.status_code in (200, 303)

    page_resp = client.get("/projects")
    assert "Design Phase" in page_resp.text