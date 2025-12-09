# app/models/employee.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Employee(Base):
    __tablename__ = "Employee"

    EmpID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(100), nullable=False)
    Title = Column(String(100))
    OfficeID = Column(Integer, ForeignKey("Office.OfficeID"))
    DeptID = Column(Integer, ForeignKey("Department.DeptID"), nullable=True)
    DivisionID = Column(Integer, ForeignKey("Division.DivisionID"), nullable=True)
    CurrentProjectID = Column(Integer, ForeignKey("Project.ProjectID"), nullable=True)

    # Relationships (optional, for ORM joins)
    office = relationship("Office", back_populates="employees", foreign_keys=[OfficeID])
    department = relationship("Department", back_populates="employees", foreign_keys=[DeptID])
    division = relationship("Division", back_populates="employees", foreign_keys=[DivisionID])
    job_history = relationship("JobHistory", back_populates="employee")
    project_history = relationship("ProjectHistory", back_populates="employee")
    milestones = relationship("Milestone", back_populates="responsible_emp", foreign_keys="Milestone.ResponsibleEmpID")
    current_project = relationship("Project", back_populates="employees", foreign_keys=[CurrentProjectID])
    phones = relationship("Phone", back_populates="employee", foreign_keys="Phone.EmpID")
    tax_reports = relationship("TaxReport", back_populates="employee", foreign_keys="TaxReport.EmpID")