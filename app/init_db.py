# app/init_db.py
from app.core.database import Base, engine
#from app.models import employee, job_history, project, project_history, milestones
from app.models import Employee, JobHistory, Project, ProjectHistory, Milestone

def init_db():
    # Create all tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")