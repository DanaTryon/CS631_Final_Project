# tests/integration/test_employees_routes.py
def test_employees_json_list_empty(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []

def test_create_employee_json(client):
    payload = {"name": "Alice", "title": "Engineer", "dept_id": 1}
    response = client.post("/employees", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["title"] == "Engineer"
    assert data["dept_id"] == 1

def test_employees_page_template(client):
    response = client.get("/employees_page")
    assert response.status_code == 200
    assert "<h1>Employee Directory</h1>" in response.text

def test_add_employee_form_submission(client):
    response = client.post(
        "/employees_page",
        data={"name": "Bob", "title": "Manager", "dept_id": 1},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Bob" in response.text
    assert "Manager" in response.text