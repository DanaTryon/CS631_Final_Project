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
    job_history_id: int = Field(alias="JobHistoryID")
    emp_id: int = Field(alias="EmpID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# -------------------------
# Employee Schemas
# -------------------------

class EmployeeBase(BaseModel):
    name: str = Field(alias="Name")
    title: str = Field(alias="Title")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class EmployeeCreate(EmployeeBase):
    dept_id: int = Field(alias="DeptID")
    division_id: Optional[int] = Field(alias="DivisionID", default=None)
    office_id: Optional[int] = Field(alias="OfficeID", default=None)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class EmployeeRead(BaseModel):
    emp_id: int = Field(alias="EmpID")
    name: str = Field(alias="Name")
    title: str = Field(alias="Title")
    dept_id: Optional[int] = Field(alias="DeptID")
    division_id: Optional[int] = Field(alias="DivisionID")
    office_id: Optional[int] = Field(alias="OfficeID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class Employee(EmployeeBase):
    emp_id: int = Field(alias="EmpID")
    job_history: List[JobHistory] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)