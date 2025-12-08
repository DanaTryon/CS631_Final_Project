# app/models/milestones.py
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Milestone(Base):
    __tablename__ = "Milestone"

    MilestoneID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(150), nullable=False)
    Description = Column(Text, nullable=True)
    DueDate = Column(Date, nullable=True)
    ProjectID = Column(Integer, ForeignKey("Project.ProjectID"))
    ResponsibleEmpID = Column(Integer, ForeignKey("Employee.EmpID"))

    # Relationships
    project = relationship("Project", back_populates="milestones", foreign_keys=[ProjectID])
    responsible_emp = relationship("Employee", back_populates="milestones", foreign_keys=[ResponsibleEmpID])