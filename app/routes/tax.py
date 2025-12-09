# app/routes/tax.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.templates import templates
from app.services.tax import run_tax_report
from app.schemas.tax import TaxReport

router = APIRouter()

@router.post("/tax_report/run", response_model=TaxReport)
def run_tax_endpoint(year: int, db: Session = Depends(get_db)):
    report = run_tax_report(db, year)
    return TaxReport(tax_report=report)

@router.get("/tax_report", response_class=HTMLResponse)
def tax_page(request: Request, db: Session = Depends(get_db)):
    # Default to current year for demo
    report = run_tax_report(db, year=2025)
    return templates.TemplateResponse(
        "tax.html", {"request": request, "tax_records": report}
    )