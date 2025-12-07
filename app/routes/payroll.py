from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.payroll import run_payroll
from app.schemas.payroll import PayrollReport

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/run", response_model=PayrollReport)
def run_payroll_endpoint(db: Session = Depends(get_db)):
    report = run_payroll(db)
    return {"payroll_report": report}