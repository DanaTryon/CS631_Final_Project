# tests/e2e/test_employees_e2e.py
def test_create_employee_endpoint(client):
    response = client.post("/employees", json={"name": "Charlie", "title": "Manager", "department": "HR"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Charlie"
    assert data["title"] == "Manager"
    assert data["department"] == "HR"

def test_list_employees_endpoint(client):
    # First, create an employee
    client.post("/employees", json={"name": "Dana", "title": "Developer", "department": "IT"})

    # Then, list employees
    response = client.get("/employees")
    assert response.status_code == 200
    employees = response.json()
    assert any(emp["name"] == "Dana" for emp in employees)