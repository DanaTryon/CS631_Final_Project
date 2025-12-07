# app/routes/employees.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeRead

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JSON API endpoint (for programmatic clients)
@router.get("/employees", response_model=list[EmployeeRead])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.post("/employees", response_model=EmployeeRead)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_emp = Employee(name=employee.name, title=employee.title, department=employee.department)
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

templates = Jinja2Templates(directory="app/templates")

# HTML frontend page
@router.get("/employees_page", response_class=HTMLResponse)
def employees_page(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return templates.TemplateResponse(request, "employees.html", {"employees": employees})

# HTML form submission handler
@router.post("/employees_page")
def add_employee_form(
    name: str = Form(...),
    title: str = Form(...),
    department: str = Form(None),
    db: Session = Depends(get_db)
):
    new_emp = Employee(name=name, title=title, department=department)
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    # Redirect back to the page so the new employee shows up
    return RedirectResponse(url="/employees_page", status_code=303)