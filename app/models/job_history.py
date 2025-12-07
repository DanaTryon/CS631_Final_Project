from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class JobHistory(Base):
    __tablename__ = "job_history"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"))
    title = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    salary = Column(Float, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="job_history")