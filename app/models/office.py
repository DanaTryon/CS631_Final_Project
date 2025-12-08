# app/models/office.py
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class Office(Base):
    __tablename__ = "Office"

    OfficeID = Column(Integer, primary_key=True, autoincrement=True)
    AreaSqFt = Column(Integer, nullable=False)

    # Relationship back to Employee
    employees = relationship("Employee", back_populates="office", foreign_keys='Employee.OfficeID')
    phones = relationship("Phone", back_populates="office")