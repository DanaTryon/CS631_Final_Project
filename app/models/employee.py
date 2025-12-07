# app/models/employee.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    emp_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    title = Column(String(50), nullable=False)

    # Relationships
    job_history = relationship("JobHistory", back_populates="employee")
    project_history = relationship("ProjectHistory", back_populates="employee")
    milestones = relationship("Milestone", back_populates="responsible_emp")