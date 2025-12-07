# app/schemas/payroll.py
from pydantic import BaseModel, ConfigDict

class PayrollRecord(BaseModel):
    emp_id: int
    name: str
    net_pay: float

    model_config = ConfigDict(from_attributes=True)

class PayrollReport(BaseModel):
    payroll_report: list[PayrollRecord]