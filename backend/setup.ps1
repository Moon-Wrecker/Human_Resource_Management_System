# Backend Setup Script for Windows PowerShell
# Run this script to set up the backend development environment

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "GenAI HRMS Backend Setup" -ForegroundColor Cyan
Write-Host "===============================================`n" -ForegroundColor Cyan

# Step 1: Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Step 2: Create virtual environment
Write-Host "`n[2/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "[INFO] Virtual environment already exists" -ForegroundColor Blue
} else {
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate virtual environment
Write-Host "`n[3/6] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "[OK] Virtual environment activated" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host "`n[4/6] Installing dependencies..." -ForegroundColor Yellow
Write-Host "[INFO] This may take a few minutes..." -ForegroundColor Blue
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Step 5: Create .env file if it doesn't exist
Write-Host "`n[5/6] Creating environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "[INFO] .env file already exists" -ForegroundColor Blue
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] .env file created from .env.example" -ForegroundColor Green
    Write-Host "[WARNING] Please update SECRET_KEY and JWT_SECRET_KEY in .env for production!" -ForegroundColor Yellow
}

# Step 6: Initialize database
Write-Host "`n[6/6] Initializing database..." -ForegroundColor Yellow
python database.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Database initialized successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to initialize database" -ForegroundColor Red
    exit 1
}

# Success message
Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "===============================================`n" -ForegroundColor Cyan

Write-Host "To start the development server, run:" -ForegroundColor Yellow
Write-Host "  python main.py" -ForegroundColor White
Write-Host "`nOr with uvicorn:" -ForegroundColor Yellow
Write-Host "  uvicorn main:app --reload`n" -ForegroundColor White

Write-Host "API will be available at:" -ForegroundColor Yellow
Write-Host "  - API: http://localhost:8000" -ForegroundColor White
Write-Host "  - Docs: http://localhost:8000/api/docs" -ForegroundColor White
Write-Host "  - Health: http://localhost:8000/health`n" -ForegroundColor White

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Review and update .env file" -ForegroundColor White
Write-Host "  2. Run: python main.py" -ForegroundColor White
Write-Host "  3. Visit: http://localhost:8000/api/docs`n" -ForegroundColor White

