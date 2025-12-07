from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.job_history import JobHistory
from app.schemas.payroll import PayrollRecord

FEDERAL_TAX = 0.10
STATE_TAX = 0.05
OTHER_TAX = 0.03

def run_payroll(db: Session):
    employees = db.query(Employee).all()
    report = []

    for emp in employees:
        # Get latest job history for salary
        latest_job = (
            db.query(JobHistory)
            .filter(JobHistory.emp_id == emp.emp_id)
            .order_by(JobHistory.start_date.desc())
            .first()
        )

        if latest_job:
            gross = latest_job.salary
            deductions = gross * (FEDERAL_TAX + STATE_TAX + OTHER_TAX)
            net_pay = gross - deductions

            record = PayrollRecord(
                emp_id=emp.emp_id,
                name=emp.name,
                net_pay=net_pay
            )
            report.append(record)

    return report