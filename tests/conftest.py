# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

@pytest.fixture(autouse=True)
def clean_database():
    # Drop and recreate schema before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def test_db(db_session):
    return db_session

@pytest.fixture(scope="module")
def client():
    # Provide a TestClient for e2e tests
    with TestClient(app) as c:
        yield c