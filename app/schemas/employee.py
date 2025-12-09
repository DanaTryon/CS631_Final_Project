# app/schemas/employee.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date

# -------------------------
# Job History Schemas
# -------------------------

class JobHistoryBase(BaseModel):
    title: str
    start_date: date
    salary: float

class JobHistoryCreate(JobHistoryBase):
    pass

class JobHistory(JobHistoryBase):
    id: int = Field(alias="JobHistoryID")
    emp_id: int = Field(alias="EmpID")

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Employee Schemas
# -------------------------

class EmployeeBase(BaseModel):
    name: str = Field(alias="Name")
    title: str = Field(alias="Title")

class EmployeeCreate(EmployeeBase):
    department: Optional[str] = Field(alias="DeptID", default=None)

class EmployeeRead(BaseModel):
    emp_id: int = Field(alias="EmpID")
    name: str = Field(alias="Name")
    title: str = Field(alias="Title")
    department: Optional[str] = Field(alias="DeptID", default=None)

    model_config = ConfigDict(from_attributes=True)

class Employee(EmployeeBase):
    emp_id: int = Field(alias="EmpID")
    job_history: List[JobHistory] = []

    model_config = ConfigDict(from_attributes=True)