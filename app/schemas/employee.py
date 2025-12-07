from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class JobHistoryBase(BaseModel):
    title: str
    start_date: date
    salary: float

class JobHistoryCreate(JobHistoryBase):
    pass

class JobHistory(JobHistoryBase):
    id: int
    emp_id: int

    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    name: str
    title: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    emp_id: int
    job_history: List[JobHistory] = []

    class Config:
        orm_mode = True