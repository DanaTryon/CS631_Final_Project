# tests/e2e/test_employees_e2e.py
def test_create_employee_endpoint(client):
    # Use correct schema fields (dept_id, division_id, office_id, current_project_id)
    response = client.post("/employees", json={
        "name": "Charlie",
        "title": "Manager",
        "dept_id": 1,
        "division_id": 1,
        "office_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["Name"] == "Charlie"
    assert data["Title"] == "Manager"


def test_list_employees_endpoint(client):
    # First, create an employee with valid schema
    client.post("/employees", json={
        "name": "Dana",
        "title": "Developer",
        "dept_id": 1,
        "division_id": 1,
        "office_id": 1
    })

    # Then, list employees
    response = client.get("/employees")
    assert response.status_code == 200
    employees = response.json()
    # Adjust to match schema alias keys ("Name" not "name")
    assert any(emp["Name"] == "Dana" for emp in employees)