# tests/integration/test_payroll_tax_routes.py
import pytest
from decimal import Decimal
from app.models.employee import Employee
from app.models.job_history import JobHistory
from datetime import date


def test_payroll_json(client):
    # Hit the JSON API endpoint
    response = client.post("/payroll/run")
    assert response.status_code == 200
    data = response.json()

    # The schema wraps the report in "payroll_report"
    assert "payroll_report" in data
    records = data["payroll_report"]
    assert isinstance(records, list)
    assert len(records) >= 1

    record = records[0]
    assert "emp_id" in record
    assert "name" in record
    assert "gross" in record
    assert "deductions" in record
    assert "net_pay" in record

    gross = Decimal(str(record["gross"]))
    deductions = Decimal(str(record["deductions"]))
    net = Decimal(str(record["net_pay"]))
    assert net == gross - deductions

def test_tax_json(client, test_db):
    emp = Employee(Name="TaxUser", Title="Analyst", OfficeID=1)
    test_db.add(emp)
    test_db.commit()

    job = JobHistory(
        EmpID=emp.EmpID,
        Title="Analyst",
        StartDate=date.today(),
        Salary=Decimal("5000.00")
    )
    test_db.add(job)
    test_db.commit()

    response = client.post("/tax_report/run?year=2025")
    data = response.json()
    record = next(r for r in data["tax_report"] if r["emp_id"] == emp.EmpID)

    assert Decimal(str(record["federal"])) == Decimal("500.00")  # 10% of 5000
