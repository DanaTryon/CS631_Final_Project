# scripts/seed_test_data.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.models.building import Building
from app.models.room import Room
from app.models.office import Office
from app.models.employee import Employee
from app.models.division import Division
from app.models.department import Department
from app.models.project import Project
from app.models.milestones import Milestone

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed():
    session = SessionLocal()

    # 1. Building
    building = session.query(Building).first()
    if not building:
        building = Building(
            BuildingCode="B001",
            Name="HQ Building",
            YearBuilt=1990,
            Cost=1000000.00,
        )
        session.add(building)
        session.commit()

    # 2. Room linked to Building
    room = session.query(Room).first()
    if not room:
        room = Room(
            BuildingCode=building.BuildingCode,
            RoomNumber=101,
            RoomType="Office",
        )
        session.add(room)
        session.commit()

    # 3. Office
    office = session.query(Office).first()
    if not office:
        office = Office(AreaSqFt=500)
        session.add(office)
        session.commit()

    # 4. Employee (needed for Division, Department, Project)
    employee = session.query(Employee).first()
    if not employee:
        employee = Employee(
            Name="Alice",
            Title="Engineer",
            OfficeID=office.OfficeID,
        )
        session.add(employee)
        session.commit()

    # 5. Division (needs Employee for DivHeadID)
    division = session.query(Division).first()
    if not division:
        division = Division(Name="Corporate", DivHeadID=employee.EmpID)
        session.add(division)
        session.commit()

    # 6. Department (needs Division + Employee for DeptHeadID)
    department = session.query(Department).first()
    if not department:
        department = Department(
            Name="Engineering",
            Budget=500000.00,
            DivisionID=division.DivisionID,
            DeptHeadID=employee.EmpID,
        )
        session.add(department)
        session.commit()

    # 7. Project (needs Employee for ManagerID)
    project = session.query(Project).first()
    if not project:
        project = Project(
            Name="Test Project",
            Description="Demo project for integration tests",
            Budget=250000.00,
            StartDate="2025-01-01",
            EndDate="2025-12-31",
            ManagerID=employee.EmpID,
        )
        session.add(project)
        session.commit()

    # 8. Milestone (linked to Project + Employee)
    milestone = session.query(Milestone).first()
    if not milestone:
        milestone = Milestone(
            Description="Initial planning phase",
            Status="pending",
            DueDate="2025-03-01",
            ProjectID=project.ProjectID,
            ResponsibleEmpID=employee.EmpID,
        )
        session.add(milestone)
        session.commit()

    session.close()

if __name__ == "__main__":
    seed()