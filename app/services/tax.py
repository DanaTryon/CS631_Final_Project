# app/services/tax.py
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.employee import Employee
from app.models.job_history import JobHistory
from app.schemas.tax import TaxRecord

FEDERAL_TAX = Decimal("0.10")
STATE_TAX = Decimal("0.05")
OTHER_TAX = Decimal("0.03")

def run_tax_report(db: Session, year: int):
    employees = db.query(Employee).all()
    report = []

    for emp in employees:
        latest_job = (
            db.query(JobHistory)
            .filter(JobHistory.EmpID == emp.EmpID)
            .order_by(JobHistory.StartDate.desc())
            .first()
        )

        if latest_job:
            gross = latest_job.Salary
            federal = gross * FEDERAL_TAX
            state = gross * STATE_TAX
            other = gross * OTHER_TAX

            record = TaxRecord(
                emp_id=emp.EmpID,
                name=emp.Name,
                year=year,
                federal=federal,
                state=state,
                other=other
            )
            report.append(record)

    return report