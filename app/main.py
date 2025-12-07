from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.payroll import run_payroll

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(
    directory="/home/danat/projects/CS631_final_project/app/templates"
)

# Landing page
@app.get("/", response_class=HTMLResponse, tags=["web"])
async def read_index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

# HR page
@app.get("/hr", response_class=HTMLResponse)
async def read_hr(request: Request):
    return templates.TemplateResponse(request, "hr.html", {"request": request})

# Projects page
@app.get("/projects", response_class=HTMLResponse)
async def read_projects(request: Request):
    return templates.TemplateResponse(request, "projects.html", {"request": request})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/payroll/run")
def payroll_run(db: Session = Depends(get_db)):
    report = run_payroll(db)
    return {"payroll_report": report}

@app.get("/payroll", response_class=HTMLResponse)
def payroll_page(request: Request, db: Session = Depends(get_db)):
    report = run_payroll(db)
    return templates.TemplateResponse(request, "payroll.html", {"request": request, "report": report})