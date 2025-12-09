# app/schemas/tax.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class TaxRecord(BaseModel):
    emp_id: int
    name: str
    year: int
    federal: Decimal
    state: Decimal
    other: Decimal

    model_config = ConfigDict(from_attributes=True)

class TaxReport(BaseModel):
    tax_report: list[TaxRecord]