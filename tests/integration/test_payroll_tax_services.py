# tests/integration/test_payroll_tax_services.py
import pytest
from decimal import Decimal
from sqlalchemy.orm import Session
from app.services.payroll import run_payroll
from app.services.tax import run_tax_report
from app.models.employee import Employee
from app.models.job_history import JobHistory

@pytest.fixture
def seed_employee(client):
    # Use the same DB session override
    from tests.conftest import TestingSessionLocal
    session: Session = TestingSessionLocal()

    emp = session.query(Employee).first()
    if not emp:
        emp = Employee(Name="Bob", Title="Developer", OfficeID=1)
        session.add(emp)
        session.commit()

    session.close()
    return emp

def test_run_payroll(seed_employee):
    from tests.conftest import TestingSessionLocal
    session: Session = TestingSessionLocal()

    # Clear any existing job history to avoid PK collisions
    session.query(JobHistory).filter(JobHistory.EmpID == seed_employee.EmpID).delete()
    session.commit()

    # Insert job history with a unique StartDate
    job = JobHistory(
        EmpID=seed_employee.EmpID,
        Title="Developer",
        StartDate="2025-01-01",
        Salary=Decimal("5000.00")
    )
    session.add(job)
    session.commit()

    report = run_payroll(session)
    assert len(report) >= 1
    record = report[0]

    assert record.gross == Decimal("5000.00")
    assert record.deductions == Decimal("5000.00") * Decimal("0.18")
    assert record.net_pay == Decimal("5000.00") - record.deductions

    session.close()

def test_run_tax_report(seed_employee):
    from tests.conftest import TestingSessionLocal
    session: Session = TestingSessionLocal()

    # Clear any existing job history to avoid PK collisions
    session.query(JobHistory).filter(JobHistory.EmpID == seed_employee.EmpID).delete()
    session.commit()

    # Insert job history with a different StartDate
    job = JobHistory(
        EmpID=seed_employee.EmpID,
        Title="Developer",
        StartDate="2025-02-01",
        Salary=Decimal("5000.00")
    )
    session.add(job)
    session.commit()

    report = run_tax_report(session, year=2025)
    assert len(report) >= 1
    record = report[0]

    assert record.federal == Decimal("5000.00") * Decimal("0.10")
    assert record.state == Decimal("5000.00") * Decimal("0.05")
    assert record.other == Decimal("5000.00") * Decimal("0.03")
    assert record.year == 2025

    session.close()