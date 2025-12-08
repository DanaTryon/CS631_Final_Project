# app/models/job_history.py
from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class JobHistory(Base):
    __tablename__ = "JobHistory"

    EmpID = Column(Integer, ForeignKey("Employee.EmpID"), primary_key=True)
    StartDate = Column(Date, primary_key=True)
    Title = Column(String(100), nullable=False)
    Salary = Column(DECIMAL(12, 2), nullable=False)

    # Relationship back to Employee
    employee = relationship("Employee", back_populates="job_history")