# app/models/devision.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Division(Base):
    __tablename__ = "Division"   # must match the MySQL table name exactly

    DivisionID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(100), nullable=False)
    DivHeadID = Column(Integer, ForeignKey("Employee.EmpID"))

    # Relationships
    div_head = relationship("Employee", foreign_keys=[DivHeadID])
    departments = relationship("Department", back_populates="division")
    employees = relationship("Employee", back_populates="division", foreign_keys="Employee.DivisionID")