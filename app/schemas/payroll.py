# app/schemas/payroll.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class PayrollRecord(BaseModel):
    emp_id: int
    name: str
    gross: Decimal
    deductions: Decimal
    net_pay: Decimal

    model_config = ConfigDict(from_attributes=True)

class PayrollReport(BaseModel):
    payroll_report: list[PayrollRecord]