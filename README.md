# TaskManager — Django Portfolio Project

A production-style full-stack Task Manager built with Django, PostgreSQL, and Bootstrap 5.

## Architecture Overview

The project uses a **multi-app Django architecture** that separates concerns clearly:

| App | Responsibility |
|-----|---------------|
| `accounts` | User registration, login, logout, password reset |
| `tasks` | Task CRUD, personal dashboard, search/filter |
| `dashboard` | Admin-only system overview, user list, all tasks |
| `config` | Project settings, root URLs, WSGI/ASGI |

Templates are split between a global `templates/` folder (base layout, partials) and each app's own `templates/<app>/` folder.

---

## Features

### Regular Users
- Register and login
- Password reset via email
- Personal dashboard with task statistics
- Create, view, edit, delete their own tasks
- Search tasks by title/description
- Filter tasks by status and priority

### Admin (staff/superuser)
- Admin dashboard with system-wide statistics
- View all registered users with task counts
- View all tasks from all users
- Filter/search across all tasks

---

## Quick Start

### 1. Prerequisites

- Python 3.10+
- PostgreSQL 14+

### 2. Clone and set up virtual environment

```bash
git clone <your-repo>
cd task_manager
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials and a real SECRET_KEY
```

Generate a secret key:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Create the PostgreSQL database

```sql
-- In psql:
CREATE DATABASE task_manager_db;
-- If needed:
CREATE USER postgres WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE task_manager_db TO postgres;
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## Project Structure

```
task_manager/
│
├── manage.py
├── requirements.txt
├── .env.example
│
├── config/                     # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                   # Authentication app
│   ├── forms.py                # RegisterForm, LoginForm
│   ├── views.py                # RegisterView, CustomLoginView
│   ├── urls.py                 # Login, register, password reset URLs
│   └── templates/accounts/     # Auth templates
│
├── tasks/                      # Task management app
│   ├── models.py               # Task model (status, priority, due_date)
│   ├── forms.py                # TaskForm, TaskFilterForm
│   ├── views.py                # CRUD views (ownership enforced)
│   ├── urls.py
│   └── templates/tasks/        # Task templates
│
├── dashboard/                  # Admin dashboard app
│   ├── mixins.py               # StaffRequiredMixin
│   ├── views.py                # System-wide views
│   ├── urls.py
│   └── templates/dashboard/    # Admin templates
│
├── templates/                  # Global templates
│   ├── base.html
│   └── includes/
│       ├── navbar.html
│       ├── messages.html
│       └── footer.html
│
└── static/
    └── css/main.css
```

---

## Security Design

| Protection | Implementation |
|-----------|---------------|
| Authentication | `LoginRequiredMixin` on all user views |
| Ownership | `get_queryset()` always filters by `user=request.user` |
| Admin access | `StaffRequiredMixin` → checks `is_staff` or `is_superuser` |
| CSRF | Django's `{% csrf_token %}` in all POST forms |
| Password reset | Django's built-in token-based flow |
| SQL injection | Django ORM parameterized queries |

---

## Password Reset (Development)

In development, reset emails are printed to the console (`EmailBackend`).
Look for the reset link in your terminal output after submitting the reset form.

For production, configure SMTP settings in `.env`:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=you@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## URL Reference

| URL | View | Access |
|-----|------|--------|
| `/accounts/login/` | Login | Public |
| `/accounts/register/` | Register | Public |
| `/accounts/logout/` | Logout | Auth |
| `/accounts/password-reset/` | Password Reset | Public |
| `/tasks/dashboard/` | User Dashboard | Auth |
| `/tasks/` | Task List | Auth |
| `/tasks/create/` | Create Task | Auth |
| `/tasks/<pk>/` | Task Detail | Auth (owner) |
| `/tasks/<pk>/edit/` | Edit Task | Auth (owner) |
| `/tasks/<pk>/delete/` | Delete Task | Auth (owner) |
| `/dashboard/` | Admin Overview | Staff only |
| `/dashboard/users/` | All Users | Staff only |
| `/dashboard/tasks/` | All Tasks | Staff only |
| `/admin/` | Django Admin | Superuser |

---

## Future Improvements

- Custom `AbstractUser` model for user profiles (avatar, bio)
- Task categories / labels
- Task assignment (assign tasks to other users)
- Email notifications for due dates
- REST API with Django REST Framework
- Docker + docker-compose setup
- CI/CD pipeline with GitHub Actions
- Unit and integration tests with pytest-django
