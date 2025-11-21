"""
Pydantic schemas for Payslip API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime


# Request Schemas
class PayslipCreate(BaseModel):
    """Schema for creating payslip"""
    employee_id: int = Field(..., description="ID of employee", gt=0)
    pay_period_start: date = Field(..., description="Pay period start date")
    pay_period_end: date = Field(..., description="Pay period end date")
    pay_date: date = Field(..., description="Payment date")
    
    # Salary components
    basic_salary: float = Field(..., ge=0, description="Basic salary")
    allowances: float = Field(0.0, ge=0, description="Total allowances")
    overtime_pay: float = Field(0.0, ge=0, description="Overtime payment")
    bonus: float = Field(0.0, ge=0, description="Bonus amount")
    
    # Deductions
    tax_deduction: float = Field(0.0, ge=0, description="Tax deduction")
    pf_deduction: float = Field(0.0, ge=0, description="Provident fund deduction")
    insurance_deduction: float = Field(0.0, ge=0, description="Insurance deduction")
    other_deductions: float = Field(0.0, ge=0, description="Other deductions")
    
    @validator('pay_period_end')
    def validate_pay_period(cls, v, values):
        if 'pay_period_start' in values and v < values['pay_period_start']:
            raise ValueError('pay_period_end must be after pay_period_start')
        return v
    
    @validator('pay_date')
    def validate_pay_date(cls, v, values):
        if 'pay_period_end' in values and v < values['pay_period_end']:
            raise ValueError('pay_date should be on or after pay_period_end')
        return v


class PayslipUpdate(BaseModel):
    """Schema for updating payslip"""
    pay_period_start: Optional[date] = None
    pay_period_end: Optional[date] = None
    pay_date: Optional[date] = None
    basic_salary: Optional[float] = Field(None, ge=0)
    allowances: Optional[float] = Field(None, ge=0)
    overtime_pay: Optional[float] = Field(None, ge=0)
    bonus: Optional[float] = Field(None, ge=0)
    tax_deduction: Optional[float] = Field(None, ge=0)
    pf_deduction: Optional[float] = Field(None, ge=0)
    insurance_deduction: Optional[float] = Field(None, ge=0)
    other_deductions: Optional[float] = Field(None, ge=0)


class PayslipGenerateRequest(BaseModel):
    """Schema for generating payslip for all employees"""
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    year: int = Field(..., ge=2020, le=2100, description="Year")
    pay_date: Optional[date] = Field(None, description="Payment date (defaults to last day of month)")


# Response Schemas
class PayslipResponse(BaseModel):
    """Schema for payslip response"""
    id: int
    employee_id: int
    employee_name: str
    employee_id_number: str
    
    # Pay period
    pay_period_start: date
    pay_period_end: date
    pay_date: date
    month: int
    year: int
    
    # Salary components
    basic_salary: float
    allowances: float
    overtime_pay: float
    bonus: float
    gross_salary: float
    
    # Deductions
    tax_deduction: float
    pf_deduction: float
    insurance_deduction: float
    other_deductions: float
    total_deductions: float
    
    # Net pay
    net_salary: float
    
    # Document
    payslip_file_path: Optional[str]
    has_document: bool
    
    # Metadata
    issued_at: datetime
    issued_by: Optional[int]
    issued_by_name: Optional[str]
    
    class Config:
        from_attributes = True


class PayslipListResponse(BaseModel):
    """Schema for list of payslips"""
    payslips: List[PayslipResponse]
    total: int
    page: int
    page_size: int


class PayslipStatsResponse(BaseModel):
    """Schema for payslip statistics"""
    total_payslips: int
    this_month: int
    total_payout_this_month: float
    average_salary: float
    employees_paid: int
    pending_payslips: int


class PayslipUploadResponse(BaseModel):
    """Response for payslip document upload"""
    message: str
    payslip_id: int
    file_path: str
    file_name: str


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

