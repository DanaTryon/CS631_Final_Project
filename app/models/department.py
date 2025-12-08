# app/models/department.py
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Department(Base):
    __tablename__ = "Department"

    DeptID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(100), unique=True, nullable=False)
    Budget = Column(DECIMAL(12, 2), nullable=True)
    DivisionID = Column(Integer, ForeignKey("Division.DivisionID"))
    DeptHeadID = Column(Integer, ForeignKey("Employee.EmpID"))

    # Relationships
    division = relationship("Division", back_populates="departments")
    dept_head = relationship("Employee", foreign_keys=[DeptHeadID])
    employees = relationship("Employee", back_populates="department", foreign_keys="Employee.DeptID")