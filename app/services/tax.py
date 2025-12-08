# app/services/tax.py
from app.models.tax_report import TaxReport
from app.database import SessionLocal

FEDERAL_RATE = 0.10
STATE_RATE = 0.05
OTHER_RATE = 0.03

def generate_tax_report(payroll_records, period):
    session = SessionLocal()
    reports = []
    for record in payroll_records:
        gross = record.gross_pay
        federal = gross * FEDERAL_RATE
        state = gross * STATE_RATE
        other = gross * OTHER_RATE
        net = gross - (federal + state + other)

        report = TaxReport(
            emp_id=record.emp_id,
            period=period,
            gross_pay=gross,
            federal_tax=federal,
            state_tax=state,
            other_tax=other,
            net_pay=net,
        )
        session.add(report)
        reports.append(report)
    session.commit()
    return reports