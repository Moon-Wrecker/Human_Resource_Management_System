"""
Announcement service - Business logic for announcement operations
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from models import Announcement, User, UserRole
from schemas.announcement_schemas import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse


class AnnouncementService:
    """Announcement service class"""
    
    @staticmethod
    def create_announcement(
        db: Session,
        announcement_data: AnnouncementCreate,
        created_by_user: User
    ) -> Announcement:
        """
        Create a new announcement
        
        Args:
            db: Database session
            announcement_data: Announcement data from request
            created_by_user: User creating the announcement
            
        Returns:
            Announcement: Created announcement object
        """
        # Create announcement
        new_announcement = Announcement(
            title=announcement_data.title,
            message=announcement_data.message,
            link=announcement_data.link,
            target_departments=announcement_data.target_departments,
            target_roles=announcement_data.target_roles,
            is_urgent=announcement_data.is_urgent,
            expiry_date=announcement_data.expiry_date,
            created_by=created_by_user.id,
            created_at=datetime.utcnow(),
            published_date=datetime.utcnow(),
            is_active=True
        )
        
        db.add(new_announcement)
        db.commit()
        db.refresh(new_announcement)
        
        return new_announcement
    
    @staticmethod
    def get_announcements(
        db: Session,
        current_user: User,
        include_expired: bool = False,
        include_inactive: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Announcement], int, int, int]:
        """
        Get all announcements
        
        Args:
            db: Database session
            current_user: Current user (for filtering by role/department)
            include_expired: Include expired announcements
            include_inactive: Include inactive announcements
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (announcements, total_count, active_count, urgent_count)
        """
        # Build query
        query = db.query(Announcement)
        
        # Filter by active status (unless including inactive)
        if not include_inactive:
            query = query.filter(Announcement.is_active == True)
        
        # Filter by expiry date (unless including expired)
        if not include_expired:
            query = query.filter(
                or_(
                    Announcement.expiry_date == None,
                    Announcement.expiry_date > datetime.utcnow()
                )
            )
        
        # Filter by target roles and departments
        # If announcement has specific targets, check if user matches
        # Otherwise, show to everyone
        
        # Order by urgent first, then by published date (newest first)
        query = query.order_by(
            Announcement.is_urgent.desc(),
            Announcement.published_date.desc()
        )
        
        # Get total count
        total_count = query.count()
        
        # Get active count
        active_query = db.query(Announcement).filter(
            Announcement.is_active == True,
            or_(
                Announcement.expiry_date == None,
                Announcement.expiry_date > datetime.utcnow()
            )
        )
        active_count = active_query.count()
        
        # Get urgent count
        urgent_count = active_query.filter(Announcement.is_urgent == True).count()
        
        # Apply pagination
        announcements = query.offset(skip).limit(limit).all()
        
        return announcements, total_count, active_count, urgent_count
    
    @staticmethod
    def get_announcement_by_id(
        db: Session,
        announcement_id: int
    ) -> Optional[Announcement]:
        """
        Get announcement by ID
        
        Args:
            db: Database session
            announcement_id: Announcement ID
            
        Returns:
            Announcement or None if not found
        """
        return db.query(Announcement).filter(
            Announcement.id == announcement_id
        ).first()
    
    @staticmethod
    def update_announcement(
        db: Session,
        announcement_id: int,
        update_data: AnnouncementUpdate
    ) -> Optional[Announcement]:
        """
        Update announcement
        
        Args:
            db: Database session
            announcement_id: Announcement ID
            update_data: Update data
            
        Returns:
            Updated announcement or None if not found
        """
        announcement = db.query(Announcement).filter(
            Announcement.id == announcement_id
        ).first()
        
        if not announcement:
            return None
        
        # Update fields that are provided
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(announcement, field, value)
        
        db.commit()
        db.refresh(announcement)
        
        return announcement
    
    @staticmethod
    def delete_announcement(
        db: Session,
        announcement_id: int,
        soft_delete: bool = True
    ) -> bool:
        """
        Delete announcement (soft delete by default)
        
        Args:
            db: Database session
            announcement_id: Announcement ID
            soft_delete: If True, set is_active to False; if False, actually delete
            
        Returns:
            True if deleted, False if not found
        """
        announcement = db.query(Announcement).filter(
            Announcement.id == announcement_id
        ).first()
        
        if not announcement:
            return False
        
        if soft_delete:
            # Soft delete: set is_active to False
            announcement.is_active = False
            db.commit()
        else:
            # Hard delete: remove from database
            db.delete(announcement)
            db.commit()
        
        return True
    
    @staticmethod
    def format_announcement_response(
        announcement: Announcement,
        db: Session
    ) -> AnnouncementResponse:
        """
        Format announcement for response with additional fields
        
        Args:
            announcement: Announcement object
            db: Database session (to fetch creator name)
            
        Returns:
            AnnouncementResponse with formatted data
        """
        # Get creator name
        creator = db.query(User).filter(User.id == announcement.created_by).first()
        creator_name = creator.name if creator else "Unknown"
        
        # Check if expired
        is_expired = False
        if announcement.expiry_date:
            is_expired = announcement.expiry_date < datetime.utcnow()
        
        return AnnouncementResponse(
            id=announcement.id,
            title=announcement.title,
            message=announcement.message,
            link=announcement.link,
            target_departments=announcement.target_departments,
            target_roles=announcement.target_roles,
            is_urgent=announcement.is_urgent,
            created_by=announcement.created_by,
            created_by_name=creator_name,
            created_at=announcement.created_at,
            published_date=announcement.published_date,
            expiry_date=announcement.expiry_date,
            is_active=announcement.is_active,
            is_expired=is_expired
        )
    
    @staticmethod
    def get_stats(db: Session) -> dict:
        """
        Get announcement statistics
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with statistics
        """
        total = db.query(Announcement).count()
        
        active = db.query(Announcement).filter(
            Announcement.is_active == True,
            or_(
                Announcement.expiry_date == None,
                Announcement.expiry_date > datetime.utcnow()
            )
        ).count()
        
        urgent = db.query(Announcement).filter(
            Announcement.is_active == True,
            Announcement.is_urgent == True,
            or_(
                Announcement.expiry_date == None,
                Announcement.expiry_date > datetime.utcnow()
            )
        ).count()
        
        expired = db.query(Announcement).filter(
            Announcement.expiry_date != None,
            Announcement.expiry_date < datetime.utcnow()
        ).count()
        
        inactive = db.query(Announcement).filter(
            Announcement.is_active == False
        ).count()
        
        return {
            "total": total,
            "active": active,
            "urgent": urgent,
            "expired": expired,
            "inactive": inactive
        }

