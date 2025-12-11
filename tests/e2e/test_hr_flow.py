# tests/e2e/test_hr_flow.py
from datetime import date
from decimal import Decimal
from app.models.job_history import JobHistory

def test_full_hr_flow(client, db_session):
    # 1. Create employee via API
    payload = {
        "name": "E2E Tester",
        "title": "QA Engineer",
        "dept_id": 1,
        "division_id": 1,
        "office_id": 1
    }
    resp = client.post("/employees", json=payload)
    assert resp.status_code == 200
    emp_data = resp.json()
    emp_id = emp_data["EmpID"]

    # 2. Add job history directly in DB
    job = JobHistory(
        EmpID=emp_id,
        Title="QA Engineer",
        StartDate=date.today(),
        Salary=Decimal("6000.00")
    )
    db_session.add(job)
    db_session.commit()

    # 3. Run payroll
    resp = client.post("/payroll/run")
    assert resp.status_code == 200
    payroll = resp.json()["payroll_report"]
    record = next(r for r in payroll if r["emp_id"] == emp_id)
    assert record["net_pay"] == str(Decimal("6000.00") * Decimal("0.82"))

    # 4. Run tax report
    resp = client.post("/tax_report/run?year=2025")
    assert resp.status_code == 200
    tax = resp.json()["tax_report"]
    record = next(r for r in tax if r["emp_id"] == emp_id)
    assert record["federal"] == str(Decimal("6000.00") * Decimal("0.10"))

    # 5. Navigate to employees page and check name
    resp = client.get("/employees_page")
    assert resp.status_code == 200
    assert "E2E Tester" in resp.text