# app/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Centralized imports
from app.core.database import Base
from app.core.templates import templates
from app.routes import employees, payroll, tax, projects, job_hist
import app.models  # Ensure models are registered

# Print registered tables for verification
print("Registered tables:", Base.metadata.tables.keys())

app = FastAPI()

# Include routers
app.include_router(employees.router)
app.include_router(payroll.router)
app.include_router(tax.router)
app.include_router(projects.router)
app.include_router(job_hist.router)

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Landing page
@app.get("/", response_class=HTMLResponse, tags=["web"])
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# HR page
@app.get("/hr", response_class=HTMLResponse, tags=["web"])
async def read_hr(request: Request):
    return templates.TemplateResponse("hr.html", {"request": request})

# Projects page
@app.get("/projects", response_class=HTMLResponse, tags=["web"])
async def read_projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})