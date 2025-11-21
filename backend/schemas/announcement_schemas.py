"""
Pydantic schemas for announcements
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class AnnouncementBase(BaseModel):
    """Base announcement schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Announcement title")
    message: str = Field(..., min_length=1, description="Announcement message/description")
    link: Optional[str] = Field(None, max_length=500, description="Optional link for more details")


class AnnouncementCreate(AnnouncementBase):
    """Schema for creating announcement"""
    target_departments: Optional[str] = Field(None, description="Target departments (comma-separated IDs)")
    target_roles: Optional[str] = Field(None, description="Target roles (comma-separated)")
    is_urgent: bool = Field(False, description="Mark as urgent announcement")
    expiry_date: Optional[datetime] = Field(None, description="Expiry date for announcement")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Office Closed for Diwali",
                "message": "All branches will remain closed from November 14–16 for Diwali celebrations. Wishing everyone a joyous festival!",
                "link": "https://intranet.company.com/holiday-calendar",
                "is_urgent": False,
                "expiry_date": "2025-11-20T00:00:00"
            }
        }


class AnnouncementUpdate(BaseModel):
    """Schema for updating announcement"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    message: Optional[str] = Field(None, min_length=1)
    link: Optional[str] = Field(None, max_length=500)
    target_departments: Optional[str] = None
    target_roles: Optional[str] = None
    is_urgent: Optional[bool] = None
    expiry_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated: Office Closed for Diwali",
                "message": "All branches will remain closed from November 14–17 for Diwali celebrations.",
                "is_urgent": True
            }
        }


class AnnouncementResponse(BaseModel):
    """Schema for announcement response"""
    id: int
    title: str
    message: str
    link: Optional[str]
    target_departments: Optional[str]
    target_roles: Optional[str]
    is_urgent: bool
    created_by: int
    created_at: datetime
    published_date: datetime
    expiry_date: Optional[datetime]
    is_active: bool
    
    # Additional fields
    created_by_name: Optional[str] = None
    is_expired: bool = False
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Office Closed for Diwali",
                "message": "All branches will remain closed from November 14–16 for Diwali celebrations.",
                "link": "https://intranet.company.com/holiday-calendar",
                "target_departments": None,
                "target_roles": None,
                "is_urgent": False,
                "created_by": 1,
                "created_by_name": "Sarah Johnson",
                "created_at": "2025-11-02T10:00:00",
                "published_date": "2025-11-02T10:00:00",
                "expiry_date": None,
                "is_active": True,
                "is_expired": False
            }
        }


class AnnouncementListResponse(BaseModel):
    """Schema for list of announcements"""
    announcements: List[AnnouncementResponse]
    total: int
    active: int
    urgent: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "announcements": [
                    {
                        "id": 1,
                        "title": "Office Closed for Diwali",
                        "message": "All branches will remain closed...",
                        "link": "https://intranet.company.com/holiday-calendar",
                        "is_urgent": False,
                        "created_by": 1,
                        "created_by_name": "Sarah Johnson",
                        "created_at": "2025-11-02T10:00:00",
                        "published_date": "2025-11-02T10:00:00",
                        "is_active": True
                    }
                ],
                "total": 10,
                "active": 8,
                "urgent": 2
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

