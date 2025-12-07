# app/models/project_history.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProjectHistory(Base):
    __tablename__ = "project_history"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"))
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    role = Column(String(50), nullable=False)
    time_spent = Column(Integer, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="project_history")
    project = relationship("Project", back_populates="team")