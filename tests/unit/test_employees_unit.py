# tests/unit/test_employees_unit.py
from app.models.employee import Employee

def test_employee_model_fields():
    emp = Employee(name="Alice", title="Engineer", department="R&D")
    assert emp.name == "Alice"
    assert emp.title == "Engineer"
    assert emp.department == "R&D"