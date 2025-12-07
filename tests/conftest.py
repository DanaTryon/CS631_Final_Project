# tests/conftest.py
import pytest
from app.database import Base, engine, SessionLocal

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create all tables at the start of the test session,
    and drop them at the end.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    """
    Provide a fresh database session for each test.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Alias so tests can request `test_db`
@pytest.fixture()
def test_db(db_session):
    return db_session
