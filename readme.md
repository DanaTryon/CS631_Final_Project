# CS631 Final Project – Personnel Portal

This project is a **FastAPI-based personnel management portal** developed for NJIT CS631, Data Management System Design.  
It demonstrates a vertical slice implementation of an HR payroll system, with backend logic, database integration, and frontend templates.

---

## 🚀 Features
- **FastAPI backend** with SQLAlchemy ORM
- **SQLite in-memory testing** (production-ready with MySQL)
- **Jinja2 templates** for frontend pages (`index`, `hr`, `projects`, `payroll`)
- **Static assets** served via FastAPI (`/static/styles.css`)
- **Automated testing** with `pytest` and coverage reports
- **CI/CD ready** with GitHub Actions and Trivy security scanning

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

All tests use **SQLite in-memory** to avoid interfering with the production MySQL database.

---

## 🔒 Security Scanning (Trivy)

If you have Trivy installed locally:

```bash
trivy fs .
```

This scans the project for vulnerabilities in dependencies and configuration.

---

## 📂 Project Structure

```
app/
  ├── main.py              # FastAPI entrypoint
  ├── database.py          # DB session setup
  ├── models/              # SQLAlchemy models
  ├── services/            # Business logic (e.g., payroll)
  ├── schemas/             # Pydantic schemas
  └── templates/           # Jinja2 HTML templates
tests/
  ├── unit/                # Unit tests
  ├── integration/         # Integration tests
  └── e2e/                 # End-to-end tests
```

---

## 📖 Notes
- Production DB: MySQL  
- Testing DB: SQLite (in-memory)  
- CI/CD: GitHub Actions workflows for automated testing and Trivy security scanning

---

## 👨‍💻 Author
Developed by **Dana Tryon** , Computer Science Masters Graduate Student for NJIT CS631 (Data Management System Design).



