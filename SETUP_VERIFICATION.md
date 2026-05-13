# Server Setup & Verification Guide

This document provides everything you need to start, configure, and troubleshoot the Student Management System.

---

## 1. Quick Start (Recommended)

The easiest way to start the server on Windows is using the provided startup scripts. These scripts automatically activate the virtual environment, run system checks, and start the server.

### Option A: PowerShell (Recommended)
```powershell
.\run_server.ps1
```

### Option B: Command Prompt
```cmd
run_server.bat
```

**Expected Output:**
```
System check identified no issues (0 silenced).
Django version 4.2.30, using settings 'student_management_system.settings'
Starting development server at http://127.0.0.1:8000/
```

**To Stop the Server:** Press `CTRL + C` in the terminal.

---

## 2. Manual Setup & Installation (Complete Guide)

If the startup scripts don't work, or you are setting up the project for the first time, follow these steps:

### Prerequisites ✅
- [x] Python 3.8+ installed
- [x] Git Version Control installed

### Step 1: Verify Python Installation
```bash
python --version
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
- **Windows PowerShell:** `venv\Scripts\Activate.ps1`
- **Windows CMD:** `venv\Scripts\activate.bat`
- **Mac/Linux:** `source venv/bin/activate`

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Django Checks & Apply Migrations
```bash
python manage.py check
python manage.py migrate
```

### Step 6: Start the Server
```bash
python manage.py runserver
```

---

## 3. Accessing the Application

- **Home Page / Login:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

*Note: To run the server on a different port, use:*
```bash
python manage.py runserver 8001
# or
python manage.py runserver 0.0.0.0:9000
```

---

## 4. Default Login Credentials

| User Type | Email | Password |
|-----------|-------|----------|
| **Admin/HOD** | admin@demo.com | admin |
| **Staff** | staff@demo.com | staff |
| **Student** | student@demo.com | student |

### Create a New Admin User
```bash
python manage.py createsuperuser
```
Then follow the prompts to enter your email and password.

---

## 5. Troubleshooting & Common Errors

| Problem / Error Message | Cause & Solution |
|-------------------------|------------------|
| **"venv not found"** | Virtual environment isn't created. Run: `python -m venv venv` |
| **"No module named 'django'"** | venv is not activated or dependencies missing. Activate venv, then run: `pip install -r requirements.txt` |
| **"manage.py not found"** | You are not in the correct directory. Make sure you are in the project root directory. |
| **"Port 8000 already in use"** | Another process is using the port. Run: `python manage.py runserver 8001` |
| **"Command not found: python"** | Python not in PATH. Use `python3` instead or fix Python installation. |
| **"TemplateDoesNotExist"** | Run: `python manage.py collectstatic --noinput` |
| **"migrate" needed** | Database changes detected. Run: `python manage.py migrate` |

---

## 6. Project Details & Best Practices

### Important Notes
- Always keep the virtual environment activated (`(venv)`) while working on the project.
- Never commit the `venv/` folder to version control.
- The default database is stored locally in `db.sqlite3`.

### Environment Variables (Optional for Production)
For production deployment, consider creating a `.env` file:
```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Project Structure
```text
student-management-using-django/
├── manage.py              # Django management script
├── db.sqlite3             # Database file
├── requirements.txt       # Python dependencies
├── run_server.bat         # Windows batch startup script
├── run_server.ps1         # Windows PowerShell startup script
├── SETUP_VERIFICATION.md  # Server setup and running guide
├── student_management_system/  # Main project settings
├── main_app/              # Main application (models, views, urls)
└── venv/                  # Virtual environment (do not commit)
```
