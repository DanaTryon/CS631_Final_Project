from datetime import date
from app.models import Employee, JobHistory
from app.services.payroll import run_payroll

def test_run_payroll_with_db(test_db):
    emp = Employee(emp_id=1, name="Alice", title="Engineer")
    job = JobHistory(emp_id=1, title="Engineer", start_date=date.today(), salary=5000)
    test_db.add(emp)
    test_db.add(job)
    test_db.commit()

    report = run_payroll(test_db)
    assert report[0].net_pay == 4100.0  # 5000 * 0.82