#  Task Management Application (Django – No ORM)

##  Project Overview

This is a **Task Management Web Application** built using **Django** that provides RESTful APIs and a simple web interface for managing tasks.  
The application supports full **CRUD operations** on tasks using **raw SQL queries** (Django ORM and Generic ViewSets are NOT used).

---

##  Features

- Create, Read, Update, Delete (CRUD) tasks
- RESTful APIs that accept and return JSON
- HTML templates for task listing and task creation
- SQLite database (can be replaced with any SQL database)
- Raw SQL for database interaction (No ORM)
- Logging and exception handling
- Automated API testing using Pytest
- Clear API documentation

---

##  Tech Stack

- **Backend:** Django
- **Database:** SQLite
- **Frontend:** HTML Templates
- **Testing:** Pytest
- **Logging:** Python Logging Module

---
## Quick Start

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd TODO_LIST
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Migrate & Run
```bash
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```
The server will run at **http://127.0.0.1:8000/**.

---

## API Endpoints

### TODO
| Method | URL                               | Description               |
|--------|-----------------------------------|---------------------------|
| POST   | `/api/`                           | Create the Tasks
| GET    | `/api/tasks/`                     | Get a list of tasks       |
| PATCH  | `/api/tasks/{task.id}/update/`    | Update the tasks          |
| DELETE | `/api/tasks/<int:task_id>/delete/`| Delete the tasks          |


## Running Tests
Run all included tests:


