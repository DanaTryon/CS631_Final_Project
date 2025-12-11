# app/core/database.py
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from app.core.config import settings

# Load environment variables (defaults to .env)
load_dotenv()

# Decide DB URL
DATABASE_URL = settings.database_url

# Safety guard: prevent accidental use of test DB in non-pytest runs
if settings.TESTING and "pytest" not in sys.argv[0]:
    raise RuntimeError(
        "Application attempted to start with TESTING=true outside pytest. "
        "Refusing to connect to the test database."
    )

# Create engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()