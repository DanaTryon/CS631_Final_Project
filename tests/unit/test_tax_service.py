# tests/unit/test_tax_service.py
from datetime import date
from app.models import Employee, TaxReport, JobHistory
from app.services.tax import run_tax_report

class FakeQuery:
    def __init__(self, items):
        self._items = items

    def all(self):
        return self._items

    def filter(self, condition):
        # Handle TaxReport.Year == year or JobHistory.EmpID == emp.EmpID
        try:
            target_value = condition.right.value
        except AttributeError:
            target_value = condition.right
        attr_name = str(condition.left).split(".")[-1]  # e.g. "Year" or "EmpID"
        filtered = [obj for obj in self._items if getattr(obj, attr_name, None) == target_value]
        return FakeQuery(filtered)

    def order_by(self, *args, **kwargs):
        # Assume ordering by StartDate.desc()
        sorted_items = sorted(
            self._items,
            key=lambda obj: getattr(obj, "StartDate", None),
            reverse=True
        )
        return FakeQuery(sorted_items)

    def first(self):
        return self._items[0] if self._items else None

class FakeDB:
    def __init__(self):
        self._objects = []
    def add(self, obj):
        self._objects.append(obj)
    def commit(self): 
        pass
    def query(self, model):
        return FakeQuery([obj for obj in self._objects if isinstance(obj, model)])

def test_run_tax_report_calculates_taxes():
    db = FakeDB()
    emp = Employee(EmpID=1, Name="Alice", Title="Engineer")
    job = JobHistory(EmpID=1, Title="Engineer", StartDate=date.today(), Salary=5000)
    report = TaxReport(EmpID=1, Year=2025, FederalTax=1000, StateTax=500, OtherTax=200)

    db.add(emp)
    db.add(job)
    db.add(report)
    db.commit()

    result = run_tax_report(db, year=2025)
    assert len(result) == 1
    # Use the schema’s actual field names
    assert result[0].federal == 500   # 5000 * 0.10
    assert result[0].state == 250     # 5000 * 0.05
    assert result[0].other == 150     # 5000 * 0.03

