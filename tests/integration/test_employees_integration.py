# tests/integration/test_employees_integration.py
from app.models.employee import Employee

def test_create_employee_in_db(db_session):
    emp = Employee(Name="Bob", Title="Analyst", DeptID=1)
    db_session.add(emp)
    db_session.commit()
    db_session.refresh(emp)

    assert emp.EmpID is not None
    assert emp.Name == "Bob"
    assert emp.Title == "Analyst"
    assert emp.DeptID == 1