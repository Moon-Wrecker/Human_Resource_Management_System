"""
Payslip Service - Business logic for payslip management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from fastapi import HTTPException, status, UploadFile
from models import Payslip, User
from schemas.payslip_schemas import (
    PayslipCreate,
    PayslipUpdate,
    PayslipResponse,
    PayslipGenerateRequest,
    PayslipStatsResponse,
    PayslipUploadResponse
)
from typing import List, Optional, Tuple
from datetime import datetime, date, timedelta
from calendar import monthrange
import os
import uuid
import logging

logger = logging.getLogger(__name__)


class PayslipService:
    """Service class for payslip operations"""
    
    @staticmethod
    def create_payslip(
        db: Session,
        payslip_data: PayslipCreate,
        issued_by_user_id: int
    ) -> PayslipResponse:
        """
        Create new payslip
        
        Args:
            db: Database session
            payslip_data: Payslip creation data
            issued_by_user_id: ID of HR user issuing payslip
            
        Returns:
            PayslipResponse with created payslip
        """
        try:
            # Verify employee exists
            employee = db.query(User).filter(User.id == payslip_data.employee_id).first()
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Employee with ID {payslip_data.employee_id} not found"
                )
            
            # Calculate gross salary
            gross_salary = (
                payslip_data.basic_salary +
                payslip_data.allowances +
                payslip_data.overtime_pay +
                payslip_data.bonus
            )
            
            # Calculate total deductions
            total_deductions = (
                payslip_data.tax_deduction +
                payslip_data.pf_deduction +
                payslip_data.insurance_deduction +
                payslip_data.other_deductions
            )
            
            # Calculate net salary
            net_salary = gross_salary - total_deductions
            
            # Check for duplicate payslip for same period
            existing = db.query(Payslip).filter(
                and_(
                    Payslip.employee_id == payslip_data.employee_id,
                    Payslip.pay_period_start == payslip_data.pay_period_start,
                    Payslip.pay_period_end == payslip_data.pay_period_end
                )
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Payslip already exists for this employee for the period {payslip_data.pay_period_start} to {payslip_data.pay_period_end}"
                )
            
            # Create payslip
            new_payslip = Payslip(
                employee_id=payslip_data.employee_id,
                pay_period_start=payslip_data.pay_period_start,
                pay_period_end=payslip_data.pay_period_end,
                pay_date=payslip_data.pay_date,
                basic_salary=payslip_data.basic_salary,
                allowances=payslip_data.allowances,
                overtime_pay=payslip_data.overtime_pay,
                bonus=payslip_data.bonus,
                gross_salary=gross_salary,
                tax_deduction=payslip_data.tax_deduction,
                pf_deduction=payslip_data.pf_deduction,
                insurance_deduction=payslip_data.insurance_deduction,
                other_deductions=payslip_data.other_deductions,
                total_deductions=total_deductions,
                net_salary=net_salary,
                issued_by=issued_by_user_id,
                issued_at=datetime.utcnow()
            )
            
            db.add(new_payslip)
            db.commit()
            db.refresh(new_payslip)
            
            logger.info(f"Payslip created: ID {new_payslip.id} for employee {payslip_data.employee_id}")
            
            return PayslipService._format_payslip_response(new_payslip, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating payslip: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create payslip: {str(e)}"
            )
    
    @staticmethod
    def generate_monthly_payslips(
        db: Session,
        generate_data: PayslipGenerateRequest,
        issued_by_user_id: int
    ) -> List[PayslipResponse]:
        """
        Generate payslips for all active employees for a specific month
        
        Args:
            db: Database session
            generate_data: Generation request with month/year
            issued_by_user_id: ID of HR user
            
        Returns:
            List of created payslips
        """
        try:
            # Get first and last day of month
            _, last_day = monthrange(generate_data.year, generate_data.month)
            pay_period_start = date(generate_data.year, generate_data.month, 1)
            pay_period_end = date(generate_data.year, generate_data.month, last_day)
            
            # Set pay date
            pay_date = generate_data.pay_date if generate_data.pay_date else pay_period_end
            
            # Get all active employees
            active_employees = db.query(User).filter(User.is_active == True).all()
            
            created_payslips = []
            skipped_count = 0
            
            for employee in active_employees:
                # Check if payslip already exists
                existing = db.query(Payslip).filter(
                    and_(
                        Payslip.employee_id == employee.id,
                        Payslip.pay_period_start == pay_period_start,
                        Payslip.pay_period_end == pay_period_end
                    )
                ).first()
                
                if existing:
                    skipped_count += 1
                    continue
                
                # Use employee's base salary if available
                basic_salary = employee.salary if hasattr(employee, 'salary') and employee.salary else 50000.0
                
                # Calculate standard deductions (simplified)
                tax_rate = 0.15
                pf_rate = 0.12
                
                gross_salary = basic_salary
                tax_deduction = gross_salary * tax_rate
                pf_deduction = basic_salary * pf_rate
                total_deductions = tax_deduction + pf_deduction
                net_salary = gross_salary - total_deductions
                
                # Create payslip
                new_payslip = Payslip(
                    employee_id=employee.id,
                    pay_period_start=pay_period_start,
                    pay_period_end=pay_period_end,
                    pay_date=pay_date,
                    basic_salary=basic_salary,
                    allowances=0.0,
                    overtime_pay=0.0,
                    bonus=0.0,
                    gross_salary=gross_salary,
                    tax_deduction=tax_deduction,
                    pf_deduction=pf_deduction,
                    insurance_deduction=0.0,
                    other_deductions=0.0,
                    total_deductions=total_deductions,
                    net_salary=net_salary,
                    issued_by=issued_by_user_id,
                    issued_at=datetime.utcnow()
                )
                
                db.add(new_payslip)
                created_payslips.append(new_payslip)
            
            db.commit()
            
            # Refresh all created payslips
            for payslip in created_payslips:
                db.refresh(payslip)
            
            logger.info(f"Generated {len(created_payslips)} payslips for {generate_data.month}/{generate_data.year}. Skipped: {skipped_count}")
            
            return [PayslipService._format_payslip_response(p, db) for p in created_payslips]
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error generating payslips: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate payslips: {str(e)}"
            )
    
    @staticmethod
    def get_payslip_by_id(
        db: Session,
        payslip_id: int,
        current_user: User
    ) -> PayslipResponse:
        """Get payslip by ID with access control"""
        payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
        
        if not payslip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payslip with ID {payslip_id} not found"
            )
        
        # Access control: Only employee's own payslip or HR
        if current_user.role != "HR" and current_user.id != payslip.employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own payslips"
            )
        
        return PayslipService._format_payslip_response(payslip, db)
    
    @staticmethod
    def get_payslips_for_employee(
        db: Session,
        employee_id: int,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> Tuple[List[PayslipResponse], int]:
        """Get all payslips for a specific employee"""
        # Access control
        if current_user.role == "EMPLOYEE" and current_user.id != employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own payslips"
            )
        
        # Build query
        query = db.query(Payslip).filter(Payslip.employee_id == employee_id)
        
        # Apply filters
        if month and year:
            query = query.filter(
                and_(
                    extract('month', Payslip.pay_period_start) == month,
                    extract('year', Payslip.pay_period_start) == year
                )
            )
        elif year:
            query = query.filter(extract('year', Payslip.pay_period_start) == year)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        payslips = query.order_by(Payslip.pay_date.desc()).offset(skip).limit(limit).all()
        
        # Format responses
        formatted_payslips = [
            PayslipService._format_payslip_response(p, db) for p in payslips
        ]
        
        return formatted_payslips, total
    
    @staticmethod
    def get_all_payslips(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        employee_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> Tuple[List[PayslipResponse], int]:
        """Get all payslips (HR only)"""
        query = db.query(Payslip)
        
        # Apply filters
        if employee_id:
            query = query.filter(Payslip.employee_id == employee_id)
        if month and year:
            query = query.filter(
                and_(
                    extract('month', Payslip.pay_period_start) == month,
                    extract('year', Payslip.pay_period_start) == year
                )
            )
        elif year:
            query = query.filter(extract('year', Payslip.pay_period_start) == year)
        
        total = query.count()
        payslips = query.order_by(Payslip.pay_date.desc()).offset(skip).limit(limit).all()
        
        formatted_payslips = [
            PayslipService._format_payslip_response(p, db) for p in payslips
        ]
        
        return formatted_payslips, total
    
    @staticmethod
    def update_payslip(
        db: Session,
        payslip_id: int,
        payslip_data: PayslipUpdate
    ) -> PayslipResponse:
        """Update payslip (HR only)"""
        payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
        
        if not payslip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payslip with ID {payslip_id} not found"
            )
        
        try:
            # Update fields
            update_data = payslip_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(payslip, field, value)
            
            # Recalculate if salary components changed
            if any(k in update_data for k in ['basic_salary', 'allowances', 'overtime_pay', 'bonus']):
                payslip.gross_salary = (
                    payslip.basic_salary +
                    payslip.allowances +
                    payslip.overtime_pay +
                    payslip.bonus
                )
            
            if any(k in update_data for k in ['tax_deduction', 'pf_deduction', 'insurance_deduction', 'other_deductions']):
                payslip.total_deductions = (
                    payslip.tax_deduction +
                    payslip.pf_deduction +
                    payslip.insurance_deduction +
                    payslip.other_deductions
                )
            
            # Recalculate net salary if needed
            payslip.net_salary = payslip.gross_salary - payslip.total_deductions
            
            db.commit()
            db.refresh(payslip)
            
            logger.info(f"Payslip updated: ID {payslip_id}")
            
            return PayslipService._format_payslip_response(payslip, db)
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating payslip: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update payslip: {str(e)}"
            )
    
    @staticmethod
    def delete_payslip(db: Session, payslip_id: int) -> None:
        """Delete payslip (HR only)"""
        payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
        
        if not payslip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payslip with ID {payslip_id} not found"
            )
        
        try:
            # Delete associated file if exists
            if payslip.payslip_file_path and os.path.exists(payslip.payslip_file_path):
                os.remove(payslip.payslip_file_path)
                logger.info(f"Deleted payslip file: {payslip.payslip_file_path}")
            
            db.delete(payslip)
            db.commit()
            logger.info(f"Payslip deleted: ID {payslip_id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting payslip: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete payslip: {str(e)}"
            )
    
    @staticmethod
    async def upload_payslip_document(
        db: Session,
        payslip_id: int,
        file: UploadFile
    ) -> PayslipUploadResponse:
        """Upload payslip PDF document"""
        payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
        
        if not payslip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payslip with ID {payslip_id} not found"
            )
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed for payslips"
            )
        
        # Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 5MB limit"
            )
        
        try:
            # Create upload directory if it doesn't exist
            upload_dir = "uploads/payslips"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"payslip_{payslip_id}_{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # Delete old file if exists
            if payslip.payslip_file_path and os.path.exists(payslip.payslip_file_path):
                os.remove(payslip.payslip_file_path)
                logger.info(f"Deleted old payslip file: {payslip.payslip_file_path}")
            
            # Save new file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Update database
            payslip.payslip_file_path = file_path
            db.commit()
            
            logger.info(f"Uploaded payslip document for payslip ID {payslip_id}: {file_path}")
            
            return PayslipUploadResponse(
                message="Payslip document uploaded successfully",
                payslip_id=payslip_id,
                file_path=file_path,
                file_name=unique_filename
            )
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error uploading payslip document: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload payslip document: {str(e)}"
            )
    
    @staticmethod
    def get_payslip_document_path(db: Session, payslip_id: int, current_user: User) -> str:
        """Get payslip document path for download"""
        payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
        
        if not payslip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payslip with ID {payslip_id} not found"
            )
        
        # Access control
        if current_user.role != "HR" and current_user.id != payslip.employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only download your own payslips"
            )
        
        if not payslip.payslip_file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No document found for this payslip"
            )
        
        if not os.path.exists(payslip.payslip_file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payslip document file not found on server"
            )
        
        return payslip.payslip_file_path
    
    @staticmethod
    def get_payslip_stats(db: Session) -> PayslipStatsResponse:
        """Get payslip statistics (HR only)"""
        now = datetime.utcnow()
        current_month = now.month
        current_year = now.year
        
        # Total payslips
        total_payslips = db.query(Payslip).count()
        
        # This month
        this_month = db.query(Payslip).filter(
            and_(
                extract('month', Payslip.pay_period_start) == current_month,
                extract('year', Payslip.pay_period_start) == current_year
            )
        ).count()
        
        # Total payout this month
        total_payout = db.query(func.sum(Payslip.net_salary)).filter(
            and_(
                extract('month', Payslip.pay_period_start) == current_month,
                extract('year', Payslip.pay_period_start) == current_year
            )
        ).scalar() or 0.0
        
        # Average salary
        avg_salary = db.query(func.avg(Payslip.net_salary)).scalar() or 0.0
        
        # Employees paid this month
        employees_paid = db.query(func.count(func.distinct(Payslip.employee_id))).filter(
            and_(
                extract('month', Payslip.pay_period_start) == current_month,
                extract('year', Payslip.pay_period_start) == current_year
            )
        ).scalar() or 0
        
        # Pending payslips (active employees without payslip this month)
        total_active = db.query(User).filter(User.is_active == True).count()
        pending_payslips = total_active - employees_paid
        
        return PayslipStatsResponse(
            total_payslips=total_payslips,
            this_month=this_month,
            total_payout_this_month=round(float(total_payout), 2),
            average_salary=round(float(avg_salary), 2),
            employees_paid=employees_paid,
            pending_payslips=max(0, pending_payslips)
        )
    
    @staticmethod
    def _format_payslip_response(payslip: Payslip, db: Session) -> PayslipResponse:
        """Format payslip model to response schema"""
        # Get employee details
        employee = db.query(User).filter(User.id == payslip.employee_id).first()
        
        # Get issued by details
        issued_by_user = None
        issued_by_name = None
        if hasattr(payslip, 'issued_by') and payslip.issued_by:
            issued_by_user = db.query(User).filter(User.id == payslip.issued_by).first()
            issued_by_name = issued_by_user.name if issued_by_user else None
        
        return PayslipResponse(
            id=payslip.id,
            employee_id=payslip.employee_id,
            employee_name=employee.name if employee else "Unknown",
            employee_id_number=employee.employee_id if employee and hasattr(employee, 'employee_id') else f"EMP{payslip.employee_id:03d}",
            pay_period_start=payslip.pay_period_start,
            pay_period_end=payslip.pay_period_end,
            pay_date=payslip.pay_date,
            month=payslip.pay_period_start.month,
            year=payslip.pay_period_start.year,
            basic_salary=payslip.basic_salary,
            allowances=payslip.allowances,
            overtime_pay=payslip.overtime_pay,
            bonus=payslip.bonus,
            gross_salary=payslip.gross_salary,
            tax_deduction=payslip.tax_deduction,
            pf_deduction=payslip.pf_deduction,
            insurance_deduction=payslip.insurance_deduction,
            other_deductions=payslip.other_deductions,
            total_deductions=payslip.total_deductions,
            net_salary=payslip.net_salary,
            payslip_file_path=payslip.payslip_file_path,
            has_document=bool(payslip.payslip_file_path),
            issued_at=payslip.issued_at if hasattr(payslip, 'issued_at') else datetime.utcnow(),
            issued_by=payslip.issued_by if hasattr(payslip, 'issued_by') else None,
            issued_by_name=issued_by_name
        )

