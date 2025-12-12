# tests/unit/test_job_hist_route.py
import pytest
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.job_history import JobHistory

client = TestClient(app)

def test_update_salary_inserts_new_record(db_session: Session):
    # Arrange
    emp_id = 1
    title = "Software Engineer"
    salary = 90000.00
    start_date = "2025-01-01"

    # Act
    response = client.post(
        "/update_salary",
        data={
            "emp_id": emp_id,
            "title": title,
            "salary": salary,
            "start_date": start_date,
        },
        allow_redirects=False,
    )

    # Assert
    assert response.status_code == 303
    record = db_session.query(JobHistory).filter_by(EmpID=emp_id, StartDate=date(2025, 1, 1)).first()
    assert record is not None
    assert record.Title == title
    assert float(record.Salary) == salary

def test_update_salary_with_invalid_employee(db_session):
    response = client.post(
        "/update_salary",
        data={
            "emp_id": 9999,  # deliberately invalid
            "title": "Ghost Employee",
            "salary": 50000.00,
            "start_date": "2025-03-01",
        },
        follow_redirects=False,
    )
    assert response.status_code == 400  # now consistent

    record = db_session.query(JobHistory).filter_by(EmpID=9999).first()
    assert record is None