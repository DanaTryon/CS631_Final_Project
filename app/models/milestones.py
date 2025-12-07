# app/models/milestones.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Milestone(Base):
    __tablename__ = "milestones"

    milestone_id = Column(Integer, primary_key=True, index=True)
    description = Column(String(200), nullable=False)
    status = Column(String(20), nullable=False)
    due_date = Column(Date, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.project_id"))
    responsible_emp_id = Column(Integer, ForeignKey("employees.emp_id"))

    # Relationships
    project = relationship("Project", back_populates="milestones")
    responsible_emp = relationship("Employee", back_populates="milestones")