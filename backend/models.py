from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum

Base = declarative_base()

# Enums for consistent data
class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    HR = "hr"
    MANAGER = "manager"
    ADMIN = "admin"

class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    HIRED = "hired"

class AttendanceStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LEAVE = "leave"
    WFH = "wfh"
    HOLIDAY = "holiday"

class LeaveType(enum.Enum):
    CASUAL = "casual"
    SICK = "sick"
    ANNUAL = "annual"
    MATERNITY = "maternity"
    PATERNITY = "paternity"

class LeaveStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class GoalStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Core User/Employee Model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    
    # Employee details
    employee_id = Column(String(20), unique=True)
    department = Column(String(50))
    job_role = Column(String(100))
    team_name = Column(String(100))
    manager_id = Column(Integer, ForeignKey('users.id'))
    hire_date = Column(Date)
    salary = Column(Float)
    
    # Document paths
    aadhar_document_path = Column(String(255))
    pan_document_path = Column(String(255))
    profile_image_path = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    manager = relationship("User", remote_side=[id])
    team_members = relationship("User", back_populates="manager")
    applications = relationship("Application", back_populates="applicant")
    attendance_records = relationship("Attendance", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee")
    payslips = relationship("Payslip", back_populates="employee")
    goals = relationship("Goal", back_populates="employee")
    skill_developments = relationship("SkillDevelopment", back_populates="employee")

# Job Listings Model
class JobListing(Base):
    __tablename__ = 'job_listings'
    
    id = Column(Integer, primary_key=True)
    position = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    experience_required = Column(String(50))
    skills_required = Column(Text)
    description = Column(Text)
    ai_generated_description = Column(Text)
    location = Column(String(100))
    employment_type = Column(String(20))  # full-time, part-time, contract
    salary_range = Column(String(50))
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    posted_by = Column(Integer, ForeignKey('users.id'))
    posted_date = Column(DateTime, default=datetime.utcnow)
    application_deadline = Column(Date)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posted_by_user = relationship("User")
    applications = relationship("Application", back_populates="job")

# Job Applications Model
class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('job_listings.id'), nullable=False)
    applicant_id = Column(Integer, ForeignKey('users.id'))
    
    # Application details
    applicant_name = Column(String(100))  # For external applicants
    applicant_email = Column(String(100))
    applicant_phone = Column(String(20))
    resume_path = Column(String(255))
    cover_letter = Column(Text)
    source = Column(String(50))  # referral, self-applied, recruitment
    
    # Status and screening
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    screening_score = Column(Float)
    screening_notes = Column(Text)
    
    # Timestamps
    applied_date = Column(DateTime, default=datetime.utcnow)
    reviewed_date = Column(DateTime)
    
    # Relationships
    job = relationship("JobListing", back_populates="applications")
    applicant = relationship("User", back_populates="applications")

# Announcements Model
class Announcement(Base):
    __tablename__ = 'announcements'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String(500))
    
    # Targeting
    target_departments = Column(String(200))  # JSON or comma-separated
    target_roles = Column(String(200))  # JSON or comma-separated
    is_urgent = Column(Boolean, default=False)
    
    # Metadata
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    published_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    created_by_user = relationship("User")

# Attendance Model
class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    
    # Time tracking
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)
    hours_worked = Column(Float)
    
    # Location and notes
    location = Column(String(100))  # office, home, client-site
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", back_populates="attendance_records")

# Leave Requests Model
class LeaveRequest(Base):
    __tablename__ = 'leave_requests'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Leave details
    leave_type = Column(Enum(LeaveType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days_requested = Column(Integer, nullable=False)
    
    # Request details
    reason = Column(Text)
    subject = Column(String(200))
    description = Column(Text)
    
    # Approval workflow
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by = Column(Integer, ForeignKey('users.id'))
    approved_date = Column(DateTime)
    rejection_reason = Column(Text)
    
    # Timestamps
    requested_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", back_populates="leave_requests")
    approver = relationship("User", foreign_keys=[approved_by])

# Payslips Model
class Payslip(Base):
    __tablename__ = 'payslips'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Pay period
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    pay_date = Column(Date, nullable=False)
    
    # Salary components
    basic_salary = Column(Float, nullable=False)
    allowances = Column(Float, default=0.0)
    overtime_pay = Column(Float, default=0.0)
    bonus = Column(Float, default=0.0)
    gross_salary = Column(Float, nullable=False)
    
    # Deductions
    tax_deduction = Column(Float, default=0.0)
    pf_deduction = Column(Float, default=0.0)
    insurance_deduction = Column(Float, default=0.0)
    other_deductions = Column(Float, default=0.0)
    total_deductions = Column(Float, default=0.0)
    
    # Net pay
    net_salary = Column(Float, nullable=False)
    
    # Document
    payslip_file_path = Column(String(255))
    
    # Timestamps
    generated_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", back_populates="payslips")

# Goals and Performance Model
class Goal(Base):
    __tablename__ = 'goals'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Goal details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # learning, performance, project
    
    # Timeline
    start_date = Column(Date, nullable=False)
    target_date = Column(Date, nullable=False)
    completion_date = Column(Date)
    
    # Progress tracking
    status = Column(Enum(GoalStatus), default=GoalStatus.NOT_STARTED)
    progress_percentage = Column(Float, default=0.0)
    
    # Metadata
    assigned_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", back_populates="goals")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])
    checkpoints = relationship("GoalCheckpoint", back_populates="goal")

# Goal Checkpoints Model
class GoalCheckpoint(Base):
    __tablename__ = 'goal_checkpoints'
    
    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer, ForeignKey('goals.id'), nullable=False)
    
    # Checkpoint details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    sequence_number = Column(Integer, nullable=False)
    
    # Status
    is_completed = Column(Boolean, default=False)
    completed_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    goal = relationship("Goal", back_populates="checkpoints")

# Skill Development Model
class SkillDevelopment(Base):
    __tablename__ = 'skill_developments'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Course/Module details
    module_name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    skill_areas = Column(String(500))  # JSON or comma-separated
    
    # Progress
    total_modules = Column(Integer, default=1)
    completed_modules = Column(Integer, default=0)
    progress_percentage = Column(Float, default=0.0)
    
    # Timeline
    enrolled_date = Column(Date, nullable=False)
    target_completion_date = Column(Date)
    completion_date = Column(Date)
    
    # Certification
    certificate_path = Column(String(255))
    is_certified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", back_populates="skill_developments")

# Policies Model
class Policy(Base):
    __tablename__ = 'policies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    content = Column(Text, nullable=False)
    
    # Categorization
    category = Column(String(100))  # HR, IT, Finance, etc.
    version = Column(String(20), default="1.0")
    
    # Status and dates
    is_active = Column(Boolean, default=True)
    effective_date = Column(Date, nullable=False)
    review_date = Column(Date)
    
    # Document
    document_path = Column(String(255))
    
    # Metadata
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    created_by_user = relationship("User")

# Resume Screening Results Model
class ResumeScreeningResult(Base):
    __tablename__ = 'resume_screening_results'
    
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    
    # Screening details
    job_description_path = Column(String(255))
    resume_path = Column(String(255), nullable=False)
    screening_model_version = Column(String(50))
    
    # Scores and analysis
    overall_score = Column(Float)
    technical_skills_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    
    # Detailed analysis
    matched_keywords = Column(Text)  # JSON
    missing_keywords = Column(Text)  # JSON
    strengths = Column(Text)
    weaknesses = Column(Text)
    recommendation = Column(String(50))  # recommend, maybe, reject
    
    # Timestamps
    screened_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    application = relationship("Application")

# Performance Reports Model (for dashboard analytics)
class PerformanceReport(Base):
    __tablename__ = 'performance_reports'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Report period
    report_period_start = Column(Date, nullable=False)
    report_period_end = Column(Date, nullable=False)
    report_type = Column(String(50))  # quarterly, annual, project-based
    
    # Metrics
    overall_rating = Column(Float)
    goals_completion_rate = Column(Float)
    attendance_rate = Column(Float)
    training_completion_rate = Column(Float)
    
    # Feedback
    manager_feedback = Column(Text)
    self_assessment = Column(Text)
    development_areas = Column(Text)
    achievements = Column(Text)
    
    # Metadata
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("User")
    created_by_user = relationship("User", foreign_keys=[created_by])

# Database setup
def create_database(database_url="sqlite:///./hr_system.db"):
    """Create database and tables"""
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Get database session"""
    Session = sessionmaker(bind=engine)
    return Session()

# Example usage and initialization
if __name__ == "__main__":
    # Create database
    engine = create_database()
    session = get_session(engine)
    
    print("Database and tables created successfully!")
    print("Models available:")
    print("- User (employees, HR, managers)")
    print("- JobListing")
    print("- Application")  
    print("- Announcement")
    print("- Attendance")
    print("- LeaveRequest")
    print("- Payslip")
    print("- Goal & GoalCheckpoint")
    print("- SkillDevelopment")
    print("- Policy")
    print("- ResumeScreeningResult")
    print("- PerformanceReport")
    
    session.close()
