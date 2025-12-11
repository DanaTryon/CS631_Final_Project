# tests/integration/test_payroll_integration.py
from datetime import date
from decimal import Decimal
from app.models.employee import Employee
from app.models.job_history import JobHistory
from app.services.payroll import run_payroll

def test_run_payroll_with_db(test_db):
    # Create employee
    emp = Employee(Name="TestUser", Title="Engineer", OfficeID=1)
    test_db.add(emp)
    test_db.commit()

    # Add job history
    job = JobHistory(
        EmpID=emp.EmpID,
        Title="Engineer",
        StartDate=date.today(),
        Salary=Decimal("5000.00")
    )
    test_db.add(job)
    test_db.commit()

    # Run payroll
    report = run_payroll(test_db)
    record = next(r for r in report if r.emp_id == emp.EmpID)

    assert record.gross == Decimal("5000.00")
    assert record.net_pay == Decimal("4100.00")  # 82% of gross