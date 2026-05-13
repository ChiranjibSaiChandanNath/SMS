@echo off
echo ================================================================
echo Student Management System - Django Server Startup
echo ================================================================
echo.

REM Check if we're in the correct directory
if not exist "manage.py" (
    echo Error: manage.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment.
    echo Please ensure the venv directory exists.
    pause
    exit /b 1
)

echo.
echo Performing Django system checks...
python manage.py check
if errorlevel 1 (
    echo Error: Django system check failed.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo Starting Django Development Server...
echo ================================================================
echo Server will be available at: http://127.0.0.1:8000/
echo Press CTRL+C to stop the server.
echo.

REM Run the development server
python manage.py runserver

pause
