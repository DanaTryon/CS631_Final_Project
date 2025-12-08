# app/services/payroll.py
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.employee import Employee
from app.models.job_history import JobHistory
from app.schemas.payroll import PayrollRecord

# Use Decimal for precise financial calculations
FEDERAL_TAX = Decimal("0.10")
STATE_TAX = Decimal("0.05")
OTHER_TAX = Decimal("0.03")

def run_payroll(db: Session):
    employees = db.query(Employee).all()
    report = []

    for emp in employees:
        # Get latest job history for salary
        latest_job = (
            db.query(JobHistory)
            .filter(JobHistory.EmpID == emp.EmpID)
            .order_by(JobHistory.StartDate.desc())
            .first()
        )

        if latest_job:
            gross = latest_job.Salary  # already a Decimal from DB
            total_tax_rate = FEDERAL_TAX + STATE_TAX + OTHER_TAX
            deductions = gross * total_tax_rate
            net_pay = gross - deductions

            record = PayrollRecord(
                emp_id=emp.EmpID,
                name=emp.Name,
                gross=gross,
                deductions=deductions,
                net_pay=net_pay
            )
            report.append(record)

    return report