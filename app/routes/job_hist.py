# app/routes/job_hist.py
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.core.database import get_db
from app.core.templates import templates
from app.models.job_history import JobHistory
from app.models.employee import Employee

router = APIRouter()

# Job History landing page with optional employee filter
@router.get("/job_hist", response_class=HTMLResponse)
def job_history_page(request: Request, emp_id: int = None, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()

    if emp_id:
        job_histories = (
            db.query(JobHistory)
            .filter(JobHistory.EmpID == emp_id)
            .order_by(JobHistory.StartDate.asc())
            .all()
        )
        # Latest record for this employee
        current_record = (
            db.query(JobHistory)
            .filter(JobHistory.EmpID == emp_id)
            .order_by(JobHistory.StartDate.desc())
            .first()
        )
    else:
        job_histories = db.query(JobHistory).order_by(JobHistory.EmpID, JobHistory.StartDate).all()
        current_record = None  # Only show current record when filtered

    return templates.TemplateResponse(
        "job_hist.html",
        {
            "request": request,
            "employees": employees,
            "job_histories": job_histories,
            "selected_emp": emp_id,
            "current_record": current_record,
        },
    )

# Update salary (insert new record into JobHistory)

@router.post("/update_salary")
def update_salary(
    emp_id: int = Form(...),
    title: str = Form(...),
    salary: float = Form(...),
    start_date: str = Form(...),
    db: Session = Depends(get_db)
):
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()

    new_entry = JobHistory(
        EmpID=emp_id,
        Title=title,
        Salary=salary,
        StartDate=start_date_obj,
    )

    try:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
    except IntegrityError:
        db.rollback()
        # Return a clear error response instead of crashing
        return HTMLResponse("Invalid employee ID", status_code=400)

    return RedirectResponse(url="/job_hist", status_code=303)
