"""
Pydantic schemas for policies
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class PolicyBase(BaseModel):
    """Base policy schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Policy title")
    description: Optional[str] = Field(None, description="Policy description")
    content: str = Field(..., min_length=1, description="Policy content/text")
    category: Optional[str] = Field(None, max_length=100, description="Policy category (HR, IT, Finance, etc.)")
    version: str = Field(default="1.0", max_length=20, description="Policy version")
    effective_date: date = Field(..., description="Policy effective date")
    review_date: Optional[date] = Field(None, description="Policy review date")


class PolicyCreate(PolicyBase):
    """Schema for creating policy (metadata only, file uploaded separately)"""
    require_acknowledgment: bool = Field(default=False, description="Require employee acknowledgment")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Remote Work Policy 2025",
                "description": "Guidelines for remote work arrangements",
                "content": "This policy outlines the company's remote work guidelines...",
                "category": "HR",
                "version": "2.0",
                "effective_date": "2025-01-01",
                "review_date": "2026-01-01",
                "require_acknowledgment": True
            }
        }


class PolicyUpdate(BaseModel):
    """Schema for updating policy"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, max_length=100)
    version: Optional[str] = Field(None, max_length=20)
    effective_date: Optional[date] = None
    review_date: Optional[date] = None
    is_active: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Remote Work Policy",
                "version": "2.1",
                "review_date": "2027-01-01"
            }
        }


class PolicyResponse(BaseModel):
    """Schema for policy response"""
    id: int
    title: str
    description: Optional[str]
    content: str
    category: Optional[str]
    version: str
    is_active: bool
    effective_date: date
    review_date: Optional[date]
    document_path: Optional[str]
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    # Additional fields
    created_by_name: Optional[str] = None
    has_document: bool = False
    document_url: Optional[str] = None
    acknowledgment_count: int = 0
    is_acknowledged_by_user: bool = False
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Remote Work Policy 2025",
                "description": "Guidelines for remote work arrangements",
                "content": "This policy outlines...",
                "category": "HR",
                "version": "2.0",
                "is_active": True,
                "effective_date": "2025-01-01",
                "review_date": "2026-01-01",
                "document_path": "uploads/policies/remote-work-policy-2025.pdf",
                "created_by": 1,
                "created_by_name": "Sarah Johnson",
                "created_at": "2025-01-01T10:00:00",
                "updated_at": "2025-01-01T10:00:00",
                "has_document": True,
                "document_url": "/uploads/policies/remote-work-policy-2025.pdf",
                "acknowledgment_count": 45,
                "is_acknowledged_by_user": True
            }
        }


class PolicyListResponse(BaseModel):
    """Schema for list of policies"""
    policies: List[PolicyResponse]
    total: int
    active: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "policies": [
                    {
                        "id": 1,
                        "title": "Remote Work Policy",
                        "description": "Guidelines for remote work",
                        "version": "2.0",
                        "category": "HR",
                        "is_active": True,
                        "has_document": True
                    }
                ],
                "total": 10,
                "active": 8
            }
        }


class PolicyAcknowledgmentResponse(BaseModel):
    """Schema for policy acknowledgment response"""
    id: int
    policy_id: int
    user_id: int
    acknowledged_date: datetime
    policy_title: Optional[str] = None
    user_name: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "policy_id": 1,
                "user_id": 5,
                "acknowledged_date": "2025-11-14T15:30:00",
                "policy_title": "Remote Work Policy",
                "user_name": "John Doe"
            }
        }


class PolicyAcknowledgmentListResponse(BaseModel):
    """Schema for list of policy acknowledgments"""
    acknowledgments: List[PolicyAcknowledgmentResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "acknowledgments": [
                    {
                        "id": 1,
                        "policy_id": 1,
                        "user_id": 5,
                        "acknowledged_date": "2025-11-14T15:30:00",
                        "policy_title": "Remote Work Policy",
                        "user_name": "John Doe"
                    }
                ],
                "total": 45
            }
        }


class PolicyUploadResponse(BaseModel):
    """Schema for file upload response"""
    policy_id: int
    file_name: str
    file_path: str
    file_size: int
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "policy_id": 1,
                "file_name": "remote-work-policy.pdf",
                "file_path": "uploads/policies/remote-work-policy-2025.pdf",
                "file_size": 245678,
                "message": "Policy document uploaded successfully"
            }
        }


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully"
            }
        }

