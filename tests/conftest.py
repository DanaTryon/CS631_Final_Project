# tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.main import app
from app.core.database import Base, get_db
from app.models.building import Building
from app.models.room import Room
from app.models.office import Office
from app.models.employee import Employee
from app.models.division import Division
from app.models.department import Department
from app.models.project import Project

# Load environment variables from .env
load_dotenv()

TEST_SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('TEST_DB_USER')}:{os.getenv('TEST_DB_PASSWORD')}"
    f"@{os.getenv('TEST_DB_HOST','localhost')}:{os.getenv('TEST_DB_PORT','3306')}/cs631_test"
)

# Create engine and session factory
test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override FastAPI dependency to use test DB session
def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Ensure schema exists
    Base.metadata.create_all(bind=test_engine, checkfirst=True)

    session = TestingSessionLocal()

    # 1. Building
    building = session.query(Building).first()
    if not building:
        building = Building(
            BuildingCode="B001",
            Name="HQ Building",
            YearBuilt=1990,
            Cost=1000000.00
        )
        session.add(building)
        session.commit()

    # 2. Room linked to Building
    room = session.query(Room).first()
    if not room:
        room = Room(
            BuildingCode=building.BuildingCode,
            RoomNumber=101,
            RoomType="Office"
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
            OfficeID=office.OfficeID
        )
        session.add(employee)
        session.commit()

    # 5. Division (needs Employee for DivHeadID)
    division = session.query(Division).first()
    if not division:
        division = Division(
            Name="Corporate",
            DivHeadID=employee.EmpID
        )
        session.add(division)
        session.commit()

    # 6. Department (needs Division + Employee for DeptHeadID)
    department = session.query(Department).first()
    if not department:
        department = Department(
            Name="Engineering",
            Budget=500000.00,
            DivisionID=division.DivisionID,
            DeptHeadID=employee.EmpID
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
            ManagerID=employee.EmpID
        )
        session.add(project)
        session.commit()

    session.close()

    # Provide FastAPI test client
    with TestClient(app) as c:
        yield c

# Extra fixtures for tests that expect direct DB access
@pytest.fixture
def db_session():
    """Provide a SQLAlchemy session for tests needing direct DB access."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_db(db_session):
    """Alias fixture for compatibility with tests expecting 'test_db'."""
    return db_session