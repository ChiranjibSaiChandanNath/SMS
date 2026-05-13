# Student Management System - Django Server Startup PowerShell Script

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Student Management System - Django Server Startup" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path "manage.py")) {
    Write-Host "Error: manage.py not found." -ForegroundColor Red
    Write-Host "Please run this script from the project root directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Check if activation was successful
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found." -ForegroundColor Red
    Write-Host "Please ensure the venv directory exists." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Performing Django system checks..." -ForegroundColor Yellow
python manage.py check
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Django system check failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "Starting Django Development Server..." -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host "Server will be available at: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "Press CTRL+C to stop the server." -ForegroundColor Green
Write-Host ""

# Run the development server
python manage.py runserver

Read-Host "Press Enter to exit"
