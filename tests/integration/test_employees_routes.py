# tests/integration/test_employees_routes.py
def test_employees_json_list(client):
    response = client.get("/employees")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # At least one employee should exist (Bob from form submission)
    assert any(emp["Name"] == "Bob" for emp in data)


def test_create_employee_json(client):
    payload = {
        "name": "Alice",
        "title": "Engineer",
        "dept_id": 1,
        "division_id": 1,
        "office_id": 1,
        "current_project_id": 1
    }
    response = client.post("/employees", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["Name"] == "Alice"
    assert data["Title"] == "Engineer"
    assert data["DeptID"] == 1
    assert data["DivisionID"] == 1
    assert data["OfficeID"] == 1
    assert data["CurrentProjectID"] == 1


def test_employees_page_template(client):
    response = client.get("/employees_page")
    assert response.status_code == 200
    assert "<h1>Employee Directory</h1>" in response.text


def test_add_employee_form_submission(client):
    response = client.post(
        "/employees_page",
        data={"name": "Charlie", "title": "Analyst", "dept_id": 1, "division_id": 1},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Charlie" in response.text
    assert "Analyst" in response.text