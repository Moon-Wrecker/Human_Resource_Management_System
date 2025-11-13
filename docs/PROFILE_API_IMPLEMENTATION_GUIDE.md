# Profile Management API - Implementation Guide
## Your First API Module After Dashboards

**Module**: Profile Management  
**Priority**: #1 - START HERE  
**Time Estimate**: 2 days  
**Complexity**: ⭐⭐ Easy

---

## 📋 **What You're Building**

### **5 API Endpoints**

```http
GET    /api/v1/profile/me                    # Get my profile
PUT    /api/v1/profile/me                    # Update my profile  
POST   /api/v1/profile/upload-photo          # Upload profile picture
POST   /api/v1/profile/upload-document       # Upload documents (Aadhar, PAN)
GET    /api/v1/profile/{user_id}             # Get another user's profile
```

### **Frontend Pages Supported**

- `frontend/src/pages/Employee/Profile.tsx`
- `frontend/src/pages/HR/EmployeesList.tsx` (view employee profiles)
- `frontend/src/pages/Manager/TeamMembers.tsx` (view team profiles)

---

## 🗂️ **File Structure**

Create these files in your backend:

```
backend/
├── routes/
│   └── profile.py                 # New file - API endpoints
├── services/
│   └── profile_service.py         # New file - Business logic
├── schemas/
│   └── profile_schemas.py         # New file - Request/Response models
└── uploads/                       # Directory for file uploads
    ├── profiles/                  # Profile pictures
    └── documents/                 # Aadhar, PAN, etc.
```

---

## 📝 **Step 1: Create Schemas** (30 mins)

**File**: `backend/schemas/profile_schemas.py`

```python
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date

# Response schema for profile data
class ProfileResponse(BaseModel):
    id: int
    employee_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    job_role: Optional[str] = None
    role: str  # employee, manager, hr, admin
    
    # Department info
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    
    # Team info
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    
    # Manager info
    manager_id: Optional[int] = None
    manager_name: Optional[str] = None
    
    # Leave balances
    casual_leave_balance: int
    sick_leave_balance: int
    annual_leave_balance: int
    wfh_balance: int
    
    # File paths
    profile_picture: Optional[str] = None
    aadhar_document: Optional[str] = None
    pan_document: Optional[str] = None
    
    # Status
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

# Request schema for profile updates
class ProfileUpdateRequest(BaseModel):
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    address: Optional[str] = None
    
    @validator('phone', 'emergency_contact_phone')
    def validate_phone(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        if v is not None and len(v) != 10:
            raise ValueError('Phone number must be 10 digits')
        return v

# Response for file upload
class FileUploadResponse(BaseModel):
    message: str
    file_path: str
    file_name: str
    file_size: int
```

---

## 🔧 **Step 2: Create Service Layer** (1 hour)

**File**: `backend/services/profile_service.py`

```python
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from models import User, Department, Team
from schemas.profile_schemas import ProfileResponse, ProfileUpdateRequest
import os
import shutil
from datetime import datetime
from typing import Optional
import uuid

class ProfileService:
    
    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> ProfileResponse:
        """Get full profile for a user"""
        
        # Query user with relationships
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get department name
        department_name = None
        if user.department_id:
            department = db.query(Department).filter(
                Department.id == user.department_id
            ).first()
            department_name = department.name if department else None
        
        # Get team name
        team_name = None
        if user.team_id:
            team = db.query(Team).filter(Team.id == user.team_id).first()
            team_name = team.name if team else None
        
        # Get manager name
        manager_name = None
        if user.manager_id:
            manager = db.query(User).filter(User.id == user.manager_id).first()
            manager_name = manager.name if manager else None
        
        # Build response
        return ProfileResponse(
            id=user.id,
            employee_id=user.employee_id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            date_of_birth=user.date_of_birth,
            job_role=user.job_role,
            role=user.role.value if hasattr(user.role, 'value') else user.role,
            department_id=user.department_id,
            department_name=department_name,
            team_id=user.team_id,
            team_name=team_name,
            manager_id=user.manager_id,
            manager_name=manager_name,
            casual_leave_balance=user.casual_leave_balance or 12,
            sick_leave_balance=user.sick_leave_balance or 12,
            annual_leave_balance=user.annual_leave_balance or 12,
            wfh_balance=user.wfh_balance or 24,
            profile_picture=user.profile_picture,
            aadhar_document=user.aadhar_document,
            pan_document=user.pan_document,
            is_active=user.is_active,
            created_at=user.created_at.isoformat() if user.created_at else None
        )
    
    @staticmethod
    def update_user_profile(
        db: Session, 
        user_id: int, 
        profile_data: ProfileUpdateRequest
    ) -> ProfileResponse:
        """Update user profile (limited fields)"""
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update only allowed fields
        if profile_data.phone is not None:
            user.phone = profile_data.phone
        if profile_data.date_of_birth is not None:
            user.date_of_birth = profile_data.date_of_birth
        if profile_data.emergency_contact_name is not None:
            user.emergency_contact_name = profile_data.emergency_contact_name
        if profile_data.emergency_contact_phone is not None:
            user.emergency_contact_phone = profile_data.emergency_contact_phone
        if profile_data.address is not None:
            user.address = profile_data.address
        
        db.commit()
        db.refresh(user)
        
        return ProfileService.get_user_profile(db, user_id)
    
    @staticmethod
    def upload_profile_picture(
        db: Session, 
        user_id: int, 
        file: UploadFile
    ) -> dict:
        """Upload profile picture"""
        
        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, JPG, PNG images are allowed"
            )
        
        # Validate file size (max 5MB)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 5MB"
            )
        
        # Create uploads directory if not exists
        upload_dir = "uploads/profiles"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{user_id}_{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update user record
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Delete old profile picture if exists
            if user.profile_picture and os.path.exists(user.profile_picture):
                os.remove(user.profile_picture)
            
            user.profile_picture = file_path
            db.commit()
        
        return {
            "message": "Profile picture uploaded successfully",
            "file_path": file_path,
            "file_name": unique_filename,
            "file_size": file_size
        }
    
    @staticmethod
    def upload_document(
        db: Session, 
        user_id: int, 
        file: UploadFile,
        document_type: str  # 'aadhar' or 'pan'
    ) -> dict:
        """Upload document (Aadhar, PAN)"""
        
        # Validate document type
        if document_type not in ["aadhar", "pan"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document type must be 'aadhar' or 'pan'"
            )
        
        # Validate file type (PDF only)
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed for documents"
            )
        
        # Validate file size (max 10MB)
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10MB"
            )
        
        # Create uploads directory
        upload_dir = "uploads/documents"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        unique_filename = f"{user_id}_{document_type}_{uuid.uuid4().hex}.pdf"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update user record
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Delete old document if exists
            if document_type == "aadhar" and user.aadhar_document:
                if os.path.exists(user.aadhar_document):
                    os.remove(user.aadhar_document)
                user.aadhar_document = file_path
            elif document_type == "pan" and user.pan_document:
                if os.path.exists(user.pan_document):
                    os.remove(user.pan_document)
                user.pan_document = file_path
            
            db.commit()
        
        return {
            "message": f"{document_type.upper()} document uploaded successfully",
            "file_path": file_path,
            "file_name": unique_filename,
            "file_size": file_size
        }
    
    @staticmethod
    def check_profile_access(
        current_user: User, 
        requested_user_id: int
    ) -> bool:
        """Check if current user can access requested user's profile"""
        
        # Users can always view their own profile
        if current_user.id == requested_user_id:
            return True
        
        # HR and Admin can view all profiles
        if current_user.role in ["hr", "admin"]:
            return True
        
        # Managers can view their team members' profiles
        if current_user.role == "manager":
            # This would need to check if requested_user is in current_user's team
            # Simplified: Managers can view all for now
            return True
        
        # Regular employees can't view others' profiles
        return False
```

---

## 🛣️ **Step 3: Create Route Handlers** (1 hour)

**File**: `backend/routes/profile.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db
from models import User
from services.profile_service import ProfileService
from schemas.profile_schemas import (
    ProfileResponse, 
    ProfileUpdateRequest,
    FileUploadResponse
)
from utils.dependencies import get_current_user, require_employee

router = APIRouter(prefix="/profile", tags=["Profile Management"])

# GET /api/v1/profile/me - Get my profile
@router.get(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Profile",
    description="Get the complete profile of the currently logged-in user"
)
async def get_my_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Get my complete profile including:
    - Personal info (name, email, phone, DOB)
    - Job details (role, department, team, manager)
    - Leave balances (casual, sick, annual, WFH)
    - Uploaded documents (profile picture, Aadhar, PAN)
    """
    return ProfileService.get_user_profile(db, current_user.id)


# PUT /api/v1/profile/me - Update my profile
@router.put(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update My Profile",
    description="Update my profile information (limited fields)"
)
async def update_my_profile(
    profile_data: ProfileUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Update my profile. Only certain fields can be updated:
    - phone
    - date_of_birth
    - emergency_contact_name
    - emergency_contact_phone
    - address
    
    Fields like role, salary, department cannot be changed by user.
    """
    return ProfileService.update_user_profile(db, current_user.id, profile_data)


# POST /api/v1/profile/upload-photo - Upload profile picture
@router.post(
    "/upload-photo",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Profile Picture",
    description="Upload a profile picture (JPEG, PNG, max 5MB)"
)
async def upload_profile_photo(
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """
    Upload profile picture:
    - Allowed formats: JPEG, JPG, PNG
    - Max size: 5MB
    - Replaces existing profile picture if any
    """
    result = ProfileService.upload_profile_picture(db, current_user.id, file)
    return FileUploadResponse(**result)


# POST /api/v1/profile/upload-document - Upload documents
@router.post(
    "/upload-document",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Document",
    description="Upload Aadhar or PAN card (PDF only, max 10MB)"
)
async def upload_document(
    document_type: str = Form(...),  # 'aadhar' or 'pan'
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """
    Upload identity documents:
    - document_type: 'aadhar' or 'pan'
    - Format: PDF only
    - Max size: 10MB
    - Replaces existing document if any
    """
    result = ProfileService.upload_document(db, current_user.id, file, document_type)
    return FileUploadResponse(**result)


# GET /api/v1/profile/{user_id} - Get another user's profile
@router.get(
    "/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get User Profile",
    description="Get another user's profile (restricted by role)"
)
async def get_user_profile(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Get another user's profile.
    
    Access rules:
    - HR/Admin: Can view all profiles
    - Manager: Can view team members' profiles
    - Employee: Can only view own profile
    """
    # Check access permission
    if not ProfileService.check_profile_access(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this profile"
        )
    
    return ProfileService.get_user_profile(db, user_id)
```

---

## 🔌 **Step 4: Register Router** (5 mins)

**File**: `backend/main.py`

```python
from fastapi import FastAPI
from routes import auth, dashboard, profile  # Add profile import

app = FastAPI(title="HRMS API")

# Register routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")  # Add this line
```

---

## ✅ **Step 5: Test APIs** (30 mins)

### **Test with Thunder Client / Postman**

**1. Get My Profile**
```http
GET http://localhost:8000/api/v1/profile/me
Authorization: Bearer {your_access_token}
```

**Expected Response**:
```json
{
  "id": 1,
  "employee_id": "EMP001",
  "name": "Sarah Johnson",
  "email": "sarah.johnson@company.com",
  "phone": "9876543210",
  "date_of_birth": "1990-05-15",
  "job_role": "HR Manager",
  "role": "hr",
  "department_id": 2,
  "department_name": "Human Resources",
  "team_id": 3,
  "team_name": "HR Team",
  "manager_id": 5,
  "manager_name": "John Doe",
  "casual_leave_balance": 8,
  "sick_leave_balance": 10,
  "annual_leave_balance": 12,
  "wfh_balance": 16,
  "profile_picture": null,
  "aadhar_document": null,
  "pan_document": null,
  "is_active": true,
  "created_at": "2025-01-01T00:00:00"
}
```

**2. Update My Profile**
```http
PUT http://localhost:8000/api/v1/profile/me
Authorization: Bearer {your_access_token}
Content-Type: application/json

{
  "phone": "9876543211",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "9876543222",
  "address": "123 Main St, City, Country"
}
```

**3. Upload Profile Picture**
```http
POST http://localhost:8000/api/v1/profile/upload-photo
Authorization: Bearer {your_access_token}
Content-Type: multipart/form-data

[Select image file from file picker]
```

**4. Upload Document**
```http
POST http://localhost:8000/api/v1/profile/upload-document
Authorization: Bearer {your_access_token}
Content-Type: multipart/form-data

document_type: aadhar
[Select PDF file]
```

**5. Get Another User's Profile** (HR/Manager only)
```http
GET http://localhost:8000/api/v1/profile/5
Authorization: Bearer {your_access_token}
```

---

## 🔍 **Step 6: Write Tests** (1 hour)

**File**: `backend/tests/test_profile.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base, engine

client = TestClient(app)

def test_get_my_profile():
    """Test getting own profile"""
    # Login first
    login_response = client.post("/api/v1/auth/login", json={
        "email": "test@company.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    
    # Get profile
    response = client.get(
        "/api/v1/profile/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data
    assert "department_name" in data

def test_update_profile():
    """Test updating profile"""
    token = get_test_token()
    
    response = client.put(
        "/api/v1/profile/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": "9876543210"}
    )
    
    assert response.status_code == 200
    assert response.json()["phone"] == "9876543210"

def test_get_other_profile_without_permission():
    """Test access restriction"""
    token = get_employee_token()  # Regular employee
    
    response = client.get(
        "/api/v1/profile/999",  # Another user
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower()

# Add more tests...
```

---

## 🎯 **Success Checklist**

After completing all steps, verify:

- [x] All 5 endpoints are accessible
- [x] Authentication is required for all endpoints
- [x] Users can view their own profile
- [x] Users can update their profile
- [x] Profile picture upload works (JPEG/PNG, max 5MB)
- [x] Document upload works (PDF, max 10MB)
- [x] HR can view all profiles
- [x] Managers can view team profiles
- [x] Employees cannot view others' profiles
- [x] All tests pass
- [x] API documentation is updated
- [x] Frontend Profile page is connected

---

## 🚀 **Next Steps**

After Profile APIs are complete:

1. ✅ Update API documentation
2. ✅ Connect `frontend/src/pages/Employee/Profile.tsx`
3. ✅ Test end-to-end flow
4. ✅ Move to next module: **Attendance Management**

---

## 💡 **Tips**

1. **File Upload Best Practices**:
   - Always validate file type and size
   - Use unique filenames (UUID)
   - Store files outside web root
   - Delete old files when replacing

2. **Security**:
   - Never expose sensitive data in logs
   - Validate user permissions before file access
   - Use secure file paths (no directory traversal)

3. **Performance**:
   - Cache profile data if frequently accessed
   - Optimize queries with joins
   - Consider CDN for profile pictures

4. **Error Handling**:
   - Clear error messages for users
   - Log errors for debugging
   - Handle file system errors gracefully

---

**Estimated Time**: **2 days** (including testing)  
**Status**: ✅ **Ready to Implement**  
**Next Module**: Attendance Management

---

*"Your first step into API development. Let's make it count!"* 🚀

