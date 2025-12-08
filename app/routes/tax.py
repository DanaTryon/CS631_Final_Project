# app/routes/tax.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO
import csv

from app.core.database import get_db
from app.core.templates import templates
from app.models.tax_report import TaxReport

router = APIRouter()

@router.get("/tax_reports_page")
def tax_reports_page(request: Request, db: Session = Depends(get_db)):
    reports = db.query(TaxReport).all()
    return templates.TemplateResponse(
        "tax_reports.html", {"request": request, "reports": reports}
    )

@router.get("/tax_reports/export")
def export_tax_reports(db: Session = Depends(get_db)):
    reports = db.query(TaxReport).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Employee ID", "Period", "Gross Pay",
        "Federal Tax", "State Tax", "Other Tax", "Net Pay"
    ])
    for r in reports:
        writer.writerow([
            r.emp_id,
            r.period,
            f"{r.gross_pay:.2f}",
            f"{r.federal_tax:.2f}",
            f"{r.state_tax:.2f}",
            f"{r.other_tax:.2f}",
            f"{r.net_pay:.2f}",
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tax_reports.csv"}
    )