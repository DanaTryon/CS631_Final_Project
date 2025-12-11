# app/schemas/project.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date

# --- ProjectHistory ---
class ProjectHistoryBase(BaseModel):
    role: str = Field(alias="Role")
    time_spent: Optional[int] = Field(default=None, alias="TimeSpent")

class ProjectHistoryCreate(ProjectHistoryBase):
    emp_id: int = Field(alias="EmpID")
    project_id: int = Field(alias="ProjectID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class ProjectHistory(ProjectHistoryBase):
    emp_id: int = Field(alias="EmpID")
    project_id: int = Field(alias="ProjectID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# --- Milestone ---
class MilestoneBase(BaseModel):
    description: str = Field(alias="Description")
    status: str = Field(alias="Status")
    due_date: Optional[date] = Field(default=None, alias="DueDate")

class MilestoneCreate(MilestoneBase):
    project_id: int = Field(alias="ProjectID")
    responsible_emp_id: int = Field(alias="ResponsibleEmpID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class Milestone(MilestoneBase):
    milestone_id: int = Field(alias="MilestoneID")
    project_id: int = Field(alias="ProjectID")
    responsible_emp_id: int = Field(alias="ResponsibleEmpID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# --- Project ---
class ProjectBase(BaseModel):
    name: str = Field(alias="Name")
    budget: Optional[float] = Field(default=None, alias="Budget")
    start_date: Optional[date] = Field(default=None, alias="StartDate")
    end_date: Optional[date] = Field(default=None, alias="EndDate")

class ProjectCreate(ProjectBase):
    manager_id: Optional[int] = Field(default=None, alias="ManagerID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class Project(ProjectBase):
    project_id: int = Field(alias="ProjectID")
    manager_id: Optional[int] = Field(default=None, alias="ManagerID")
    milestones: List[Milestone] = []
    team: List[ProjectHistory] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)