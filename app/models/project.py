# app/models/project.py
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Project(Base):
    __tablename__ = "Project"

    ProjectID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(150), nullable=False)
    Description = Column(Text, nullable=True)
    Budget = Column(DECIMAL(12, 2), nullable=True)
    StartDate = Column(Date, nullable=True)
    EndDate = Column(Date, nullable=True)
    ManagerID = Column(Integer, ForeignKey("Employee.EmpID"))

    # Relationships
    manager = relationship("Employee", foreign_keys=[ManagerID])
    project_history = relationship("ProjectHistory", back_populates="project")
    employees = relationship("Employee", back_populates="current_project", foreign_keys="Employee.CurrentProjectID")
    milestones = relationship("Milestone", back_populates="project", foreign_keys="Milestone.ProjectID")