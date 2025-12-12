# tests/integration/test_job_hist_routes.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.employee import Employee
from app.core.database import get_db

client = TestClient(app)

import pytest
from app.models.employee import Employee

@pytest.fixture
def sample_employee(db_session):
    emp = Employee(
        Name="Dana Tester",
        Title="Software Engineer",
        OfficeID=1,      
        DeptID=1,
        DivisionID=1,
    )
    db_session.add(emp)
    db_session.commit()
    db_session.refresh(emp)
    return emp

def test_job_history_page_loads(sample_employee):
    response = client.get("/job_hist")
    assert response.status_code == 200
    assert "Job History" in response.text

def test_job_history_filter_by_employee(sample_employee):
    response = client.get(f"/job_hist?emp_id={sample_employee.EmpID}")
    assert response.status_code == 200
    assert str(sample_employee.EmpID) in response.text

def test_update_salary_flow(sample_employee):
    response = client.post(
        "/update_salary",
        data={
            "emp_id": sample_employee.EmpID,
            "title": "Senior Engineer",
            "salary": 120000.00,
            "start_date": "2025-02-01",
        },
        allow_redirects=False,
    )
    assert response.status_code == 303

    # Verify salary history shows up
    response2 = client.get(f"/job_hist?emp_id={sample_employee.EmpID}")
    assert "Senior Engineer" in response2.text
    assert "120000.00" in response2.text