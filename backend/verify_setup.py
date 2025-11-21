"""
Verification script to check if backend setup is complete
Run this after completing Step 1
"""
import os
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}")
        return True
    else:
        print(f"[MISSING] {description}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"[OK] {description}")
        return True
    else:
        print(f"[MISSING] {description}")
        return False

def main():
    """Run all verification checks"""
    print("="*70)
    print("Backend Setup Verification")
    print("="*70)
    
    checks = []
    
    print("\n1. Checking Core Files...")
    checks.append(check_file("main.py", "FastAPI application (main.py)"))
    checks.append(check_file("config.py", "Configuration (config.py)"))
    checks.append(check_file("database.py", "Database connection (database.py)"))
    checks.append(check_file("models.py", "Database models (models.py)"))
    checks.append(check_file("requirements.txt", "Dependencies (requirements.txt)"))
    checks.append(check_file(".env", "Environment variables (.env)"))
    checks.append(check_file(".gitignore", "Git ignore (.gitignore)"))
    checks.append(check_file("README.md", "Documentation (README.md)"))
    
    print("\n2. Checking Directories...")
    checks.append(check_directory("routes", "Routes directory"))
    checks.append(check_directory("services", "Services directory"))
    checks.append(check_directory("utils", "Utils directory"))
    checks.append(check_directory("tests", "Tests directory"))
    checks.append(check_directory("uploads", "Uploads directory"))
    
    print("\n3. Checking Upload Subdirectories...")
    checks.append(check_directory("uploads/resumes", "Resumes directory"))
    checks.append(check_directory("uploads/documents", "Documents directory"))
    checks.append(check_directory("uploads/profiles", "Profiles directory"))
    checks.append(check_directory("uploads/policies", "Policies directory"))
    checks.append(check_directory("uploads/payslips", "Payslips directory"))
    checks.append(check_directory("uploads/certificates", "Certificates directory"))
    
    print("\n4. Checking Python Packages...")
    try:
        import fastapi
        print(f"[OK] FastAPI installed (version {fastapi.__version__})")
        checks.append(True)
    except ImportError:
        print("[MISSING] FastAPI not installed")
        checks.append(False)
    
    try:
        import uvicorn
        print(f"[OK] Uvicorn installed")
        checks.append(True)
    except ImportError:
        print("[MISSING] Uvicorn not installed")
        checks.append(False)
    
    try:
        import sqlalchemy
        print(f"[OK] SQLAlchemy installed (version {sqlalchemy.__version__})")
        checks.append(True)
    except ImportError:
        print("[MISSING] SQLAlchemy not installed")
        checks.append(False)
    
    try:
        import pydantic
        print(f"[OK] Pydantic installed")
        checks.append(True)
    except ImportError:
        print("[MISSING] Pydantic not installed")
        checks.append(False)
    
    print("\n5. Checking Database...")
    if os.path.exists("hr_system.db"):
        print("[OK] Database file exists (hr_system.db)")
        checks.append(True)
    else:
        print("[INFO] Database not created yet (run: python database.py)")
        checks.append(False)
    
    print("\n" + "="*70)
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100
    
    print(f"Verification Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    
    if passed == total:
        print("[SUCCESS] All checks passed! Backend setup is complete.")
        print("\nNext Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create database: python database.py")
        print("3. Run server: python main.py")
        print("4. Visit: http://localhost:8000/api/docs")
        return 0
    else:
        print("[WARNING] Some checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

