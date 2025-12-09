# tests/unit/test_employees_unit.py
from app.models.employee import Employee

def test_employee_model_fields():
    emp = Employee(Name="Alice", Title="Engineer", DeptID=1)

    assert emp.Name == "Alice"
    assert emp.Title == "Engineer"
    assert emp.DeptID == 1


