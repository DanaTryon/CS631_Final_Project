# tests/integration/test_payroll_tax_routes.py
import pytest
from decimal import Decimal

def test_payroll_json(client):
    # Hit the JSON API endpoint
    response = client.post("/payroll/run")
    assert response.status_code == 200
    data = response.json()

    # The schema wraps the report in "payroll_report"
    assert "payroll_report" in data
    records = data["payroll_report"]
    assert isinstance(records, list)
    assert len(records) >= 1

    record = records[0]
    assert "emp_id" in record
    assert "name" in record
    assert "gross" in record
    assert "deductions" in record
    assert "net_pay" in record

    gross = Decimal(str(record["gross"]))
    deductions = Decimal(str(record["deductions"]))
    net = Decimal(str(record["net_pay"]))
    assert net == gross - deductions

def test_tax_json(client):
    # Hit the JSON API endpoint with year parameter
    response = client.post("/tax_report/run?year=2025")
    assert response.status_code == 200
    data = response.json()

    # The schema wraps the report in "tax_report"
    assert "tax_report" in data
    records = data["tax_report"]
    assert isinstance(records, list)
    assert len(records) >= 1

    record = records[0]
    assert record["year"] == 2025

    gross = Decimal("5000.00")  # matches seeded job history salary
    assert Decimal(str(record["federal"])) == gross * Decimal("0.10")
    assert Decimal(str(record["state"])) == gross * Decimal("0.05")
    assert Decimal(str(record["other"])) == gross * Decimal("0.03")
