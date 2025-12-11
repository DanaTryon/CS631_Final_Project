# app/models/milestones.py
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Milestone(Base):
    __tablename__ = "Milestone"

    MilestoneID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Description = Column(Text, nullable=False)   # milestone description
    Status = Column(String(50), nullable=False, default="pending")  # track progress state
    DueDate = Column(Date, nullable=True)
    ProjectID = Column(Integer, ForeignKey("Project.ProjectID"))
    ResponsibleEmpID = Column(Integer, ForeignKey("Employee.EmpID"))

    # Relationships
    project = relationship("Project", back_populates="milestones")
    # Only keep back_populates here if Employee has a reciprocal milestones relationship
    responsible_emp = relationship("Employee", foreign_keys=[ResponsibleEmpID])