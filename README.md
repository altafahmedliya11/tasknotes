# TaskNotes Project

A Django REST Framework project for managing **employees and tasks**, alongside a **notes manager with tags** (knowledge management). This project demonstrates **CRUD operations**, **filters**, and **business rules** in a clean, API-first architecture using **SQLite** and **UUIDs** for primary keys.

---

## Features

### Employee & Task Management

* **Employee**

  * `name`, `email` (unique), `department`, `date_joined`
* **Task**

  * `title`, `description`, `due_date`, `status` (`Pending`, `In Progress`, `Completed`), `assigned_to` (employee)
* **Business Rules**

  * Employee emails are unique.
  * Task due date cannot be in the past.
  * `completed_at` is automatically set when task status is `Completed`.
* **APIs**

  * Create Employee
  * Create Task and assign to employee
  * List Tasks (filter by status or employee)
  * Update Task (status, description, assigned employee)
  * Delete Task

### Notes & Tags (Knowledge Manager)

* **Note**

  * `title`, `content`, `tags`, `created_at`, `updated_at`
* **Tag**

  * `name` (unique)
* **Business Rules**

  * Notes can have multiple tags (Many-to-Many)
  * Tags are auto-created if they don’t exist when creating/updating a note
* **APIs**

  * Create Note with tags
  * List Notes (filter by tag or search keyword)
  * Update Note (title/content/tags)
  * Delete Note

---

## Tech Stack

* Python 3.x
* Django 5.x
* Django REST Framework
* SQLite (default DB)
* UUID primary keys for all models

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <https://github.com/altafahmedliya11/tasknotes.git>
cd tasknotes
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **requirements.txt** should include:

```
Django>=5.0
djangorestframework
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

* API Base URL: `http://127.0.0.1:8000/api/`
* Admin Panel: `http://127.0.0.1:8000/admin/`

---

## API Endpoints

### Employees & Tasks

| Action                          | URL                              | Method                     |
| ------------------------------- | -------------------------------- | -------------------------- |
| List/Create Employees           | `/api/employees/`                | GET / POST                 |
| Retrieve/Update/Delete Employee | `/api/employees/<uuid>/`         | GET / PUT / PATCH / DELETE |
| List/Create Tasks               | `/api/tasks/`                    | GET / POST                 |
| Retrieve/Update/Delete Task     | `/api/tasks/<uuid>/`             | GET / PUT / PATCH / DELETE |
| Filter Tasks by Status          | `/api/tasks/?status=Completed`   | GET                        |
| Filter Tasks by Employee        | `/api/tasks/?employee_id=<uuid>` | GET                        |

### Notes & Tags

| Action                      | URL                            | Method                     |
| --------------------------- | ------------------------------ | -------------------------- |
| List/Create Tags            | `/api/tags/`                   | GET / POST                 |
| Retrieve/Update/Delete Tag  | `/api/tags/<uuid>/`            | GET / PUT / PATCH / DELETE |
| List/Create Notes           | `/api/notes/`                  | GET / POST                 |
| Retrieve/Update/Delete Note | `/api/notes/<uuid>/`           | GET / PUT / PATCH / DELETE |
| Filter Notes by Tag         | `/api/notes/?tag=<tagname>`    | GET                        |
| Filter Notes by Keyword     | `/api/notes/?search=<keyword>` | GET                        |

---

## Example `curl` Commands

### Create an Employee

```bash
curl -X POST http://127.0.0.1:8000/api/employees/ \
-H "Content-Type: application/json" \
-d '{"name": "Altaf Ahmed", "email": "altaf@example.com", "department": "Engineering"}'
```

### Create a Task

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
-H "Content-Type: application/json" \
-d '{"title": "Finish API", "description": "Complete Employee-Task API", "due_date": "2025-10-10", "status": "Pending", "assigned_to": "<employee-uuid>"}'
```

### Create a Note with Tags

```bash
curl -X POST http://127.0.0.1:8000/api/notes/ \
-H "Content-Type: application/json" \
-d '{"title": "Django Notes", "content": "Learn DRF", "tag_names": ["django", "api"]}'
```

---

## Tests

Run all tests:

```bash
python manage.py test
```

* Includes tests for **Employees, Tasks, Notes, and Tags**
* Validates **business rules** and API functionality
