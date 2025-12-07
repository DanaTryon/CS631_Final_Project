from datetime import date
from app.models import Employee, JobHistory
from app.services.payroll import run_payroll

def test_run_payroll_calculates_net_pay(test_db):
    emp = Employee(emp_id=1, name="Bob", title="Analyst")
    job = JobHistory(emp_id=1, title="Analyst", start_date=date.today(), salary=4500)
    test_db.add(emp)
    test_db.add(job)
    test_db.commit()

    report = run_payroll(test_db)
    assert report[0].net_pay == 3690.0  # 4500 * 0.82