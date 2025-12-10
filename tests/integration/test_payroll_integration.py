# tests/integration/test_payroll_integration.py
from datetime import date
from decimal import Decimal
from app.models import Employee, JobHistory
from app.services.payroll import run_payroll

def test_run_payroll_with_db(test_db):
    # Create an employee with correct attribute names
    emp = Employee(Name="Alice", Title="Engineer", OfficeID=1)
    test_db.add(emp)
    test_db.commit()

    # Add a job history record for that employee
    job = JobHistory(
        EmpID=emp.EmpID,          # use the auto-generated PK
        Title="Engineer",
        StartDate=date.today(),
        Salary=Decimal("5000.00")
    )
    test_db.add(job)
    test_db.commit()

    # Run payroll and check net pay
    report = run_payroll(test_db)
    assert len(report) >= 1
    record = report[0]

    # Gross = 5000, deductions = 18% of gross, net = 82% of gross
    assert record.gross == Decimal("5000.00")
    assert record.net_pay == Decimal("5000.00") * Decimal("0.82")