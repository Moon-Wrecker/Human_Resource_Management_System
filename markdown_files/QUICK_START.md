# Backend Quick Start Guide

## 🚀 5-Minute Setup

### Windows (PowerShell)

```powershell
# Navigate to backend folder
cd backend

# Run setup script (automated)
.\setup.ps1

# Start development server
python main.py
```

### Manual Setup (All Platforms)

#### 1. Create Virtual Environment

```bash
# Navigate to backend
cd backend

# Create venv
python -m venv venv

# Activate venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# Linux/Mac:
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Setup Environment

```bash
# Copy environment template (Windows)
copy .env.example .env

# Copy environment template (Linux/Mac)
cp .env.example .env

# Edit .env and update SECRET_KEY and JWT_SECRET_KEY
```

#### 4. Initialize Database

```bash
python database.py
```

#### 5. Start Server

```bash
# Method 1: Using main.py
python main.py

# Method 2: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📍 Endpoints

Once running, access:

- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation (Swagger)**: http://localhost:8000/api/docs
- **API Documentation (ReDoc)**: http://localhost:8000/api/redoc

## ✅ Verify Setup

```bash
# Run verification script
python verify_setup.py

# Test health endpoint
curl http://localhost:8000/health
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "environment": "development",
    "version": "1.0.0"
  }
}
```

## 🔧 Common Commands

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell
source venv/bin/activate      # Linux/Mac

# Install new package
pip install package-name
pip freeze > requirements.txt  # Update requirements

# Run server with auto-reload
python main.py

# Run tests (when implemented)
pytest

# Check code formatting
black .

# Verify setup
python verify_setup.py
```

## 📝 Environment Variables

Key variables in `.env`:

```env
# Change these in production!
SECRET_KEY=your-secret-key-here-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-here-min-32-chars

# Database (SQLite for dev, PostgreSQL for prod)
DATABASE_URL=sqlite:///./hr_system.db

# CORS (add your frontend URLs)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError

**Solution**: Activate virtual environment and install dependencies
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Database not found

**Solution**: Initialize database
```bash
python database.py
```

### Issue: Port 8000 already in use

**Solution**: Kill existing process or use different port
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

### Issue: CORS errors from frontend

**Solution**: Add frontend URL to CORS_ORIGINS in .env
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://your-frontend-url
```

## 📚 Next Steps

1. ✅ Complete Step 1 (Setup) - **DONE**
2. ⏳ Step 2: Implement Authentication APIs
3. ⏳ Step 3: Create Dashboard APIs
4. ⏳ Step 4: Build remaining endpoints

See `step_1.md` for detailed documentation.

## 🆘 Need Help?

- Check `README.md` for full documentation
- Check `step_1.md` for setup details
- Review `README_BACKEND.md` for API specifications
- Check FastAPI docs: https://fastapi.tiangolo.com/

