# app/models/tax_report.py
from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.core.database import Base

class TaxReport(Base):
    __tablename__ = "tax_reports"

    ReportID = Column(Integer, primary_key=True, autoincrement=True)
    EmpID = Column(Integer, ForeignKey("Employee.EmpID"), nullable=False)
    Year = Column(Integer, nullable=False)
    FederalTax = Column(DECIMAL(10, 2), nullable=False)
    StateTax = Column(DECIMAL(10, 2), nullable=False)
    OtherTax = Column(DECIMAL(10, 2), nullable=False)

    employee = relationship("Employee", back_populates="tax_reports")