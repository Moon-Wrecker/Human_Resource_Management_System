"""
Payslips routes - API endpoints for payslip management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Annotated, Optional, List
from database import get_db
from models import User
from utils.dependencies import get_current_active_user, require_hr
from services.payslip_service import PayslipService
from schemas.payslip_schemas import (
    PayslipCreate,
    PayslipUpdate,
    PayslipResponse,
    PayslipListResponse,
    PayslipGenerateRequest,
    PayslipStatsResponse,
    PayslipUploadResponse,
    MessageResponse
)

router = APIRouter(prefix="/payslips", tags=["Payslips"])


@router.get(
    "/me",
    response_model=PayslipListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Payslips",
    description="Get all payslips for the authenticated user"
)
async def get_my_payslips(
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=500, description="Page size"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month"),
    year: Optional[int] = Query(None, ge=2020, description="Filter by year"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all payslips for the authenticated user.
    
    **Filters**:
    - `month`: Filter by specific month (1-12)
    - `year`: Filter by specific year
    """
    payslips, total = PayslipService.get_payslips_for_employee(
        db=db,
        employee_id=current_user.id,
        current_user=current_user,
        skip=skip,
        limit=limit,
        month=month,
        year=year
    )
    
    return PayslipListResponse(
        payslips=payslips,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get(
    "/employee/{employee_id}",
    response_model=PayslipListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee Payslips",
    description="Get all payslips for a specific employee (HR only)"
)
async def get_employee_payslips(
    employee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020),
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get all payslips for a specific employee.
    
    **Access**: HR only
    """
    payslips, total = PayslipService.get_payslips_for_employee(
        db=db,
        employee_id=employee_id,
        current_user=current_user,
        skip=skip,
        limit=limit,
        month=month,
        year=year
    )
    
    return PayslipListResponse(
        payslips=payslips,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get(
    "",
    response_model=PayslipListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Payslips",
    description="Get all payslips in the system (HR only)"
)
async def get_all_payslips(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    employee_id: Optional[int] = Query(None, description="Filter by employee"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month"),
    year: Optional[int] = Query(None, ge=2020, description="Filter by year"),
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get all payslips with filters.
    
    **Access**: HR only
    
    **Filters**:
    - `employee_id`: Show payslips for specific employee
    - `month`: Filter by month (1-12)
    - `year`: Filter by year
    """
    payslips, total = PayslipService.get_all_payslips(
        db=db,
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        month=month,
        year=year
    )
    
    return PayslipListResponse(
        payslips=payslips,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get(
    "/{payslip_id}",
    response_model=PayslipResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Payslip by ID",
    description="Get specific payslip details"
)
async def get_payslip(
    payslip_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get payslip by ID.
    
    **Access**: Employee (own payslips) or HR (all payslips)
    """
    return PayslipService.get_payslip_by_id(
        db=db,
        payslip_id=payslip_id,
        current_user=current_user
    )


@router.post(
    "",
    response_model=PayslipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Payslip",
    description="Create new payslip for an employee (HR only)"
)
async def create_payslip(
    payslip_data: PayslipCreate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Create new payslip for an employee.
    
    **Access**: HR only
    
    **Automatic Calculations**:
    - Gross Salary = Basic + Allowances + Overtime + Bonus
    - Total Deductions = Tax + PF + Insurance + Other
    - Net Salary = Gross - Deductions
    
    **Validations**:
    - Pay period end must be after start
    - Pay date should be on or after period end
    - No duplicate payslips for same period
    """
    return PayslipService.create_payslip(
        db=db,
        payslip_data=payslip_data,
        issued_by_user_id=current_user.id
    )


@router.post(
    "/generate",
    response_model=List[PayslipResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Generate Monthly Payslips",
    description="Generate payslips for all active employees for a specific month (HR only)"
)
async def generate_monthly_payslips(
    generate_data: PayslipGenerateRequest,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Generate payslips for all active employees for a specific month.
    
    **Access**: HR only
    
    **Process**:
    - Gets all active employees
    - Creates payslip for each employee
    - Skips employees who already have payslip for this period
    - Uses employee's base salary from profile
    - Applies standard deductions (15% tax, 12% PF)
    
    **Returns**: List of created payslips
    """
    return PayslipService.generate_monthly_payslips(
        db=db,
        generate_data=generate_data,
        issued_by_user_id=current_user.id
    )


@router.put(
    "/{payslip_id}",
    response_model=PayslipResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Payslip",
    description="Update payslip details (HR only)"
)
async def update_payslip(
    payslip_id: int,
    payslip_data: PayslipUpdate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Update existing payslip.
    
    **Access**: HR only
    
    **Note**: Gross, total deductions, and net salary are automatically recalculated
    """
    return PayslipService.update_payslip(
        db=db,
        payslip_id=payslip_id,
        payslip_data=payslip_data
    )


@router.delete(
    "/{payslip_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Payslip",
    description="Delete payslip (HR only)"
)
async def delete_payslip(
    payslip_id: int,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Delete payslip and associated document file.
    
    **Access**: HR only
    """
    PayslipService.delete_payslip(db=db, payslip_id=payslip_id)
    return MessageResponse(message=f"Payslip {payslip_id} deleted successfully")


@router.post(
    "/{payslip_id}/upload",
    response_model=PayslipUploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload Payslip Document",
    description="Upload PDF document for payslip (HR only)"
)
async def upload_payslip_document(
    payslip_id: int,
    file: UploadFile = File(..., description="Payslip PDF file"),
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Upload payslip PDF document.
    
    **Access**: HR only
    
    **Validations**:
    - Only PDF files allowed
    - Maximum file size: 5MB
    - Replaces old file if exists
    
    **Storage**: `uploads/payslips/payslip_{id}_{uuid}.pdf`
    """
    return await PayslipService.upload_payslip_document(
        db=db,
        payslip_id=payslip_id,
        file=file
    )


@router.get(
    "/{payslip_id}/download",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    summary="Download Payslip Document",
    description="Download payslip PDF document"
)
async def download_payslip_document(
    payslip_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Download payslip PDF document.
    
    **Access**: Employee (own payslips) or HR (all payslips)
    
    **Returns**: PDF file with proper content-type
    """
    file_path = PayslipService.get_payslip_document_path(
        db=db,
        payslip_id=payslip_id,
        current_user=current_user
    )
    
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"payslip_{payslip_id}.pdf"
    )


@router.get(
    "/stats/summary",
    response_model=PayslipStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Payslip Statistics",
    description="Get payslip statistics (HR only)"
)
async def get_payslip_stats(
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get payslip statistics.
    
    **Access**: HR only
    
    **Returns**:
    - Total payslips count
    - Payslips issued this month
    - Total payout this month
    - Average salary
    - Employees paid this month
    - Pending payslips (employees without payslip)
    """
    return PayslipService.get_payslip_stats(db=db)

