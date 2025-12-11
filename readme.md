# CS631 Final Project – Personnel Portal

This project is a **FastAPI-based personnel management portal** developed for NJIT CS631, Data Management System Design.  
It demonstrates a vertical slice implementation of an HR payroll system, with backend logic, database integration, and frontend templates.

---

## 🚀 Features
- **FastAPI backend** with SQLAlchemy ORM
- **MySQL database** for dev/prod and isolated **MySQL test database** for testing
- **Alembic migrations** for schema management
- **Jinja2 templates** for frontend pages (`index`, `hr`, `projects`, `payroll`)
- **Static assets** served via FastAPI (`/static/styles.css`)
- **Automated testing** with `pytest` and coverage reports
- **Seed scripts** for baseline test data (`scripts/seed_test_data.py`)
- **CI/CD ready** with GitHub Actions, including:
  - MySQL service container for tests
  - Alembic migrations in CI
  - Test data seeding
  - Security scanning with **Trivy** and **Bandit**

---

## 📦 Installation

Clone the repository over HTTPS:

```bash
git clone https://github.com/DanaTryon/CS631_final_project.git
cd CS631_final_project
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Locally

Start the FastAPI app with Uvicorn:

```bash
uvicorn app.main:app --reload
```

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

Available routes:
- `/` → Landing page
- `/hr` → HR page
- `/projects` → Projects page
- `/payroll` → Payroll report page
- `/payroll/run` → JSON API endpoint for payroll

---

## 🧪 Local Testing

Run the full test suite:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Test categories:
- **Unit tests** → `tests/unit/`
- **Integration tests** → `tests/integration/`
- **End-to-End tests** → `tests/e2e/`

### Environment Separation
- **Dev/Prod** → `.env` (uses `cs631_db`)
- **Testing** → `.env.test` (uses `cs631_test`)

Pytest automatically loads `.env.test` and runs against the isolated test DB.

---

## 🔒 Security Scanning

### Trivy (dependency and container scan)
If you have Trivy installed locally:

```bash
trivy fs .
```

### Bandit (Python code security linter)
Run Bandit locally:

```bash
bandit -r app -ll
```

---

## 📂 Project Structure

```
app/
  ├── main.py              # FastAPI entrypoint
  ├── core/                # Config and database setup
  ├── models/              # SQLAlchemy models
  ├── services/            # Business logic (e.g., payroll)
  ├── schemas/             # Pydantic schemas
  └── templates/           # Jinja2 HTML templates
scripts/
  └── seed_test_data.py    # Baseline test data seeding
tests/
  ├── unit/                # Unit tests
  ├── integration/         # Integration tests
  └── e2e/                 # End-to-end tests
migrations/                # Alembic migration files
```

---

## 📖 Notes
- **Dev/Prod DB**: MySQL (`cs631_db`)
- **Test DB**: MySQL (`cs631_test`) isolated via `.env.test`
- **CI/CD**: GitHub Actions workflows run migrations, seed test data, execute pytest, and perform security scans

---

## 👨‍💻 Author
Developed by **Dana Tryon**, Computer Science Masters Graduate Student for NJIT CS631 (Data Management System Design).
```

---

This version highlights:
- Dual environment strategy (`.env` vs `.env.test`)
- MySQL test DB in CI/CD
- Alembic migrations
- Seed script
- Security scanning with Trivy + Bandit


