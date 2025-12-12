# CS631 Final Project – Personnel Portal

This project is a **FastAPI-based personnel management portal** developed for NJIT CS631, Data Management System Design.  
It demonstrates a vertical slice implementation of an HR payroll system, with backend logic, database integration, migrations, automated testing, and frontend templates.

---

## 🚀 Features
- **FastAPI backend** with SQLAlchemy ORM
- **MySQL database** for dev/prod and isolated **MySQL test database** for testing
- **Alembic migrations** for schema management and reproducible workflows
- **Jinja2 templates** for frontend pages (`index`, `hr`, `projects`, `payroll`, `job_hist`)
- **Job History module** with salary update flow and employee filtering
- **Static assets** served via FastAPI (`/static/styles.css`)
- **Automated testing** with `pytest` (unit, integration, and end-to-end) and coverage reports
- **95%+ test coverage** with robust fixtures and foreign key integrity checks
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
### ⚙️ Environment Variables (Critical Setup)

Before running locally, you **must** create your own `.env` and `.env.test` files in the project root. These files configure database connections and are required for the app and tests to run correctly.

- `.env` → used for development/production (`cs631_db`)
- `.env.test` → used for pytest and CI/CD (`cs631_test`)

Example `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=cs631_db

DATABASE_URL=mysql+pymysql://your_user:your_password@localhost:3306/cs631_db
```

Example `.env.test`:
```env
TESTING=true
TEST_DB_HOST=localhost
TEST_DB_PORT=3306
TEST_DB_USER=your_user
TEST_DB_PASSWORD=your_password
TEST_DB_NAME=cs631_test
```

⚠️ Without these files, Alembic migrations, FastAPI routes, and pytest will fail because the app cannot connect to the correct database.

---

### ⚙️ Database Setup (Creating Tables)

After configuring your `.env` and `.env.test` files with the correct MySQL credentials, you’ll need to initialize the database schema. This project uses **Alembic** migrations to manage tables.

1. **Ensure the database exists**  
   Create the dev/prod database (`cs631_db`) and test database (`cs631_test`) manually in MySQL:
   ```sql
   CREATE DATABASE cs631_db;
   CREATE DATABASE cs631_test;
   ```

2. **Run Alembic migrations**  
   From the project root, apply the migrations to create all tables:
   ```bash
   alembic upgrade head
   ```

   This will:
   - Read your `.env` or `.env.test` connection string.
   - Apply all migration scripts in `migrations/versions/`.
   - Create tables such as `Employee`, `JobHistory`, `Project`, `Milestone`, etc.

3. **Verify tables**  
   In MySQL Workbench or CLI:
   ```sql
   USE cs631_db;
   SHOW TABLES;
   ```
   You should see all the schema objects defined in your models.

4. **(Optional) Seed test data**  
   Run the provided script to insert baseline records:
   ```bash
   python scripts/seed_test_data.py
   ```
   Or if you prefer to manually load some seed data on MySQL workbench, you can find this under
```
CS631_final_project
├── sample_data
    ├── sample_data_inserts_ddl.txt
    └── schema_creation_ddl.txt
```


---

### 📌 Note
- Always run `alembic upgrade head` after cloning or pulling new migrations.  
- If you need to reset, you can drop the database and recreate it, then rerun migrations.  
- The test suite (`pytest`) automatically uses `.env.test` and will run against `cs631_test`.


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
- `/job_hist` → Job History page with employee filter
- `/update_salary` → Form endpoint to insert new salary records

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
- **Coverage**: Current suite achieves ~95% coverage with no errors

---

## 👨‍💻 Author
Developed by **Dana Tryon**, Computer Science Masters Graduate Student for NJIT CS631 (Data Management System Design).



---

This revised README emphasizes:
- The new **Job History feature** and salary update flow.
- The **95% coverage milestone** and robust test suite.
- The environment separation and CI/CD pipeline.
- Clean fixes for migrations and reproducibility.


