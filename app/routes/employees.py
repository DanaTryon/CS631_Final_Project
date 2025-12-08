# app/routes/employees.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.templates import templates
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeRead

router = APIRouter()

# JSON API endpoint (for programmatic clients)
@router.get("/employees", response_model=list[EmployeeRead])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.post("/employees", response_model=EmployeeRead)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_emp = Employee(
        Name=employee.name,
        Title=employee.title,
        DeptID=employee.dept_id,
        DivisionID=employee.division_id,
        OfficeID=employee.office_id,
        CurrentProjectID=employee.current_project_id
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

# HTML frontend page
@router.get("/employees_page", response_class=HTMLResponse)
def employees_page(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return templates.TemplateResponse(
        "employees.html", {"request": request, "employees": employees}
    )

# HTML form submission handler
@router.post("/employees_page")
def add_employee_form(
    name: str = Form(...),
    title: str = Form(...),
    dept_id: int = Form(None),
    division_id: int = Form(None),
    office_id: int = Form(None),
    current_project_id: int = Form(None),
    db: Session = Depends(get_db)
):
    new_emp = Employee(
        Name=name,
        Title=title,
        DeptID=dept_id,
        DivisionID=division_id,
        OfficeID=office_id,
        CurrentProjectID=current_project_id
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return RedirectResponse(url="/employees_page", status_code=303)