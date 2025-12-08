# app/models/phone.py
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Phone(Base):
    __tablename__ = "Phone"

    PhoneNumber = Column(String(15), primary_key=True, index=True)
    OfficeID = Column(Integer, ForeignKey("Office.OfficeID"))
    EmpID = Column(Integer, ForeignKey("Employee.EmpID"))

    # Relationships
    office = relationship("Office", back_populates="phones", foreign_keys=[OfficeID])
    employee = relationship("Employee", back_populates="phones", foreign_keys=[EmpID])
