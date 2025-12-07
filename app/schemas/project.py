from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ProjectHistoryBase(BaseModel):
    role: str
    time_spent: int

class ProjectHistoryCreate(ProjectHistoryBase):
    emp_id: int
    project_id: int

class ProjectHistory(ProjectHistoryBase):
    id: int
    emp_id: int
    project_id: int

    class Config:
        orm_mode = True


class MilestoneBase(BaseModel):
    description: str
    status: str
    due_date: date

class MilestoneCreate(MilestoneBase):
    project_id: int
    responsible_emp_id: int

class Milestone(MilestoneBase):
    milestone_id: int
    project_id: int
    responsible_emp_id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    name: str
    budget: float
    start_date: date
    end_date: Optional[date]

class ProjectCreate(ProjectBase):
    manager_id: int

class Project(ProjectBase):
    project_id: int
    manager_id: int
    milestones: List[Milestone] = []
    team: List[ProjectHistory] = []

    class Config:
        orm_mode = True