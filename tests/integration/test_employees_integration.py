# tests/integration/test_employees_integration.py
from app.models.employee import Employee

def test_create_employee_in_db(test_db):
    emp = Employee(name="Bob", title="Analyst", department="Finance")
    test_db.add(emp)
    test_db.commit()
    test_db.refresh(emp)

    assert emp.emp_id is not None
    assert emp.name == "Bob"
    assert emp.title == "Analyst"
    assert emp.department == "Finance"