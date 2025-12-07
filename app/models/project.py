# app/models/project.py
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    budget = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    # Relationships
    manager_id = Column(Integer, ForeignKey("employees.emp_id"))
    manager = relationship("Employee")
    milestones = relationship("Milestone", back_populates="project")
    team = relationship("ProjectHistory", back_populates="project")