# app/routes/projects.py
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime

from app.core.database import get_db
from app.core.templates import templates
from app.models.project import Project
from app.schemas.project import ProjectCreate, Project as ProjectSchema
from app.models.project_history import ProjectHistory
from app.models.milestones import Milestone

router = APIRouter()

# JSON API endpoint
@router.post("/projects", response_model=ProjectSchema)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(
        Name=project.name,
        Budget=project.budget,
        StartDate=project.start_date,
        EndDate=project.end_date,
        ManagerID=project.manager_id,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# HTML form submission handler
@router.post("/projects_form")
def add_project_form(
    name: str = Form(...),
    budget: float = Form(None),
    start_date: str = Form(None),
    end_date: str = Form(None),
    manager_id: int = Form(None),
    db: Session = Depends(get_db)
):
    new_project = Project(
        Name=name,
        Budget=budget,
        StartDate=start_date,
        EndDate=end_date,
        ManagerID=manager_id,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return RedirectResponse(url="/projects", status_code=303)

# Projects page (reuse existing landing page)
@router.get("/projects", response_class=HTMLResponse)
def projects_page(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    project_data = []

    for proj in projects:
        team = db.query(ProjectHistory).filter_by(ProjectID=proj.ProjectID).all()
        milestones = db.query(Milestone).filter_by(ProjectID=proj.ProjectID).all()
        project_data.append({
            "project": proj,
            "team": team,
            "milestones": milestones,
        })

    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": project_data},
    )

# Assign employee to project
@router.post("/assign_project")
def assign_project(
    emp_id: int = Form(...),
    project_id: int = Form(...),
    role: str = Form(...),
    time_spent: int = Form(0),
    db: Session = Depends(get_db)
):
    assignment = ProjectHistory(
        EmpID=emp_id,
        ProjectID=project_id,
        Role=role,
        TimeSpent=time_spent,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return RedirectResponse(url="/projects", status_code=303)

# Add milestone to a project
@router.post("/add_milestone")
def add_milestone(
    description: str = Form(...),
    status: str = Form(...),
    due_date: str = Form(...),
    project_id: int = Form(...),
    responsible_emp_id: int = Form(...),
    db: Session = Depends(get_db)
):
    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    milestone = Milestone(
        Description=description,
        Status=status,
        DueDate=due_date_obj,
        ProjectID=project_id,
        ResponsibleEmpID=responsible_emp_id,
    )
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return RedirectResponse(url="/projects", status_code=303)


# Project statistics page
@router.get("/project_stats", response_class=HTMLResponse)
def project_stats(request: Request, db: Session = Depends(get_db)):
    # Total hours per project
    hours_data = (
        db.query(Project.ProjectID, Project.Name, func.sum(ProjectHistory.TimeSpent))
        .join(ProjectHistory, Project.ProjectID == ProjectHistory.ProjectID)
        .group_by(Project.ProjectID, Project.Name)
        .all()
    )

    # Milestone completion per project
    milestone_data = (
        db.query(
            Project.ProjectID,
            Project.Name,
            func.count(Milestone.MilestoneID),
            func.sum(case((Milestone.Status == "completed", 1), else_=0))
        )
        .join(Milestone, Project.ProjectID == Milestone.ProjectID)
        .group_by(Project.ProjectID, Project.Name)
        .all()
    )


    return templates.TemplateResponse(
        "projects.html",
        {
            "request": request,
            "projects": db.query(Project).all(),
            "hours_data": hours_data,
            "milestone_data": milestone_data,
        },
    )