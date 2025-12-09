# tests/integration/test_employees_route.py
def test_get_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# tests/integration/test_payroll_route.py
def test_run_payroll_route(client):
    response = client.post("/payroll/run", json={"year": 2025})
    assert response.status_code == 200
    data = response.json()
    assert "net_pay" in data[0] if isinstance(data, list) else data


# tests/integration/test_tax_route.py
def test_run_tax_route(client):
    response = client.post("/tax_report/run?year=2025")
    assert response.status_code == 200
    data = response.json()
    assert "tax_report" in data