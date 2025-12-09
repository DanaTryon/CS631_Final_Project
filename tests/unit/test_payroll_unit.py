# tests/unit/test_payroll_unit.py
from datetime import date
from app.models import Employee, JobHistory
from app.services.payroll import run_payroll

class FakeQuery:
    def __init__(self, items):
        self._items = items

    def all(self):
        return self._items

    def filter(self, condition):
        # condition is a SQLAlchemy BinaryExpression like JobHistory.EmpID == value
        # Grab the RHS value
        try:
            target_emp_id = condition.right.value
        except AttributeError:
            target_emp_id = condition.right  # fallback if .value not available
        filtered = [obj for obj in self._items if getattr(obj, "EmpID", None) == target_emp_id]
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
    
from datetime import date
from app.models import Employee, JobHistory
from app.services.payroll import run_payroll

def test_run_payroll_calculates_net_pay():
    db = FakeDB()

    emp = Employee(EmpID=1, Name="Bob", Title="Analyst")
    job = JobHistory(EmpID=1, Title="Analyst", StartDate=date.today(), Salary=4500)

    db.add(emp)
    db.add(job)
    db.commit()

    report = run_payroll(db)
    assert report[0].net_pay == 3690.0  # 4500 * 0.82

