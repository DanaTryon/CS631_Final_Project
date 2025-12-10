# tests/integration/test_init_db.py
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.init_db import init_db
from app.models.employee import Employee

@pytest.fixture(scope="module")
def db():
    # Provide a session for tests
    session = SessionLocal()
    yield session
    session.close()

def test_init_db_creates_tables(db):
    # Run your init_db function
    init_db()

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # Assert that expected tables exist
    assert "Building" in tables
    assert "Department" in tables
    assert "Division" in tables
    assert "Employee" in tables
    assert "JobHistory" in tables
    assert "Milestone" in tables
    assert "Office" in tables
    assert "Phone" in tables
    assert "Project" in tables
    assert "ProjectHistory" in tables
    assert "Room" in tables
    assert "tax_reports" in tables
    

