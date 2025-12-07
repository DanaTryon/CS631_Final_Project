from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_payroll_run_endpoint():
    response = client.post("/payroll/run")
    assert response.status_code == 200
    assert "payroll_report" in response.json()

def test_payroll_page_endpoint():
    response = client.get("/payroll")
    assert response.status_code == 200
    assert "<table" in response.text