# app/routes/payroll.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.templates import templates
from app.services.payroll import run_payroll
from app.schemas.payroll import PayrollReport

router = APIRouter()

# JSON API endpoint (programmatic clients)
@router.post("/payroll/run", response_model=PayrollReport)
def run_payroll_endpoint(db: Session = Depends(get_db)):
    report = run_payroll(db)
    return PayrollReport(payroll_report=report)

# HTML frontend page
@router.get("/payroll", response_class=HTMLResponse)
def payroll_page(request: Request, db: Session = Depends(get_db)):
    report = run_payroll(db)
    return templates.TemplateResponse(
        "payroll.html", {"request": request, "payroll_records": report}
    )