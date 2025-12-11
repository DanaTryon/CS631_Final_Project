# tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from alembic import command
from alembic.config import Config

from app.main import app
from app.core.database import get_db
from app.models.building import Building
from app.models.room import Room
from app.models.office import Office

# Explicitly load test environment variables
load_dotenv(dotenv_path=".env.test")

# Force TESTING mode
os.environ["TESTING"] = "true"

# Build test DB URL from test env vars
TEST_SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('TEST_DB_USER')}:{os.getenv('TEST_DB_PASSWORD')}"
    f"@{os.getenv('TEST_DB_HOST','localhost')}:{os.getenv('TEST_DB_PORT','3306')}/{os.getenv('TEST_DB_NAME','cs631_test')}"
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


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """Run Alembic migrations against the test DB before any tests."""
    base_dir = os.path.dirname(os.path.dirname(__file__))  # project root
    alembic_ini_path = os.path.join(base_dir, "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_SQLALCHEMY_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")
    yield


@pytest.fixture(scope="module")
def client():
    # Seed only baseline structural data
    session = TestingSessionLocal()

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

    room = session.query(Room).first()
    if not room:
        room = Room(
            BuildingCode=building.BuildingCode,
            RoomNumber=101,
            RoomType="Office",
        )
        session.add(room)
        session.commit()

    office = session.query(Office).first()
    if not office:
        office = Office(AreaSqFt=500)
        session.add(office)
        session.commit()

    session.close()

    with TestClient(app) as c:
        yield c


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