# app/models/tax_report.py
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from app.core.database import Base

class TaxReport(Base):
    __tablename__ = "tax_reports"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("employees.id"))
    period = Column(Date, nullable=False)   # e.g., month or quarter
    gross_pay = Column(Float, nullable=False)
    federal_tax = Column(Float, nullable=False)
    state_tax = Column(Float, nullable=False)
    other_tax = Column(Float, nullable=False)
    net_pay = Column(Float, nullable=False)