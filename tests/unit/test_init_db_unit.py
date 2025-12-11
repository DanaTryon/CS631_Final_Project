# tests/unit/test_init_db_unit.py
from app.core.database import Base, engine
import app.init_db

def test_init_db_creates_tables():
    # Call the init_db function
    app.init_db.init_db()
    # Verify metadata has tables
    assert "Employee" in Base.metadata.tables
    assert "tax_reports" in Base.metadata.tables