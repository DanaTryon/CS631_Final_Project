# app/models/project_history.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProjectHistory(Base):
    __tablename__ = "ProjectHistory"

    EmpID = Column(Integer, ForeignKey("Employee.EmpID"), primary_key=True)
    ProjectID = Column(Integer, ForeignKey("Project.ProjectID"), primary_key=True)
    Role = Column(String(100), nullable=False)
    TimeSpent = Column(Integer, nullable=True)

    # Relationships back to Employee and Project
    employee = relationship("Employee", back_populates="project_history")
    project = relationship("Project", back_populates="project_history")