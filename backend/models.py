from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum

# Import Base from database.py for consistency
try:
    from database import Base
except ImportError:
    # Fallback if database.py not available
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

class RequestType(enum.Enum):
    WFH = "wfh"
    LEAVE = "leave"
    EQUIPMENT = "equipment"
    TRAVEL = "travel"
    OTHER = "other"

class ModuleStatus(enum.Enum):
    NOT_STARTED = "not_started"
    PENDING = "pending"
    COMPLETED = "completed"

# Department Model (for HR Dashboard department-wise data)
class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(20), unique=True)
    description = Column(Text)
    head_id = Column(Integer, ForeignKey('users.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    head = relationship("User", foreign_keys=[head_id], back_populates="headed_department")
    employees = relationship("User", foreign_keys="User.department_id", back_populates="department_obj")
    teams = relationship("Team", back_populates="department")

# Team Model (for Manager Dashboard team overview)
class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey('departments.id'))
    manager_id = Column(Integer, ForeignKey('users.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="teams")
    manager = relationship("User", foreign_keys=[manager_id], back_populates="managed_team")
    members = relationship("User", foreign_keys="User.team_id", back_populates="team_obj")

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
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_role = Column(String(100))
    job_level = Column(String(50))  # e.g., "Junior", "Mid-level", "Senior", "Lead", "Principal"
    hierarchy_level = Column(Integer, default=5)  # 1=Top (CEO), 2=VP/Director, 3=Manager, 4=Lead, 5=Senior, 6=Mid, 7=Junior
    team_id = Column(Integer, ForeignKey('teams.id'))
    manager_id = Column(Integer, ForeignKey('users.id'))
    hire_date = Column(Date)
    salary = Column(Float)
    
    # Leave balances (shown in frontend dashboards)
    casual_leave_balance = Column(Integer, default=12)
    sick_leave_balance = Column(Integer, default=12)
    annual_leave_balance = Column(Integer, default=15)
    wfh_balance = Column(Integer, default=24)
    
    # Document paths
    aadhar_document_path = Column(String(255))
    pan_document_path = Column(String(255))
    profile_image_path = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    manager = relationship("User", remote_side=[id], foreign_keys=[manager_id])
    team_members = relationship("User", back_populates="manager", foreign_keys="User.manager_id")
    
    # Organization relationships
    department_obj = relationship("Department", foreign_keys=[department_id], back_populates="employees")
    team_obj = relationship("Team", foreign_keys=[team_id], back_populates="members")
    headed_department = relationship("Department", foreign_keys="Department.head_id", back_populates="head", uselist=False)
    managed_team = relationship("Team", foreign_keys="Team.manager_id", back_populates="manager", uselist=False)
    
    # Activity relationships
    applications = relationship("Application", foreign_keys="Application.applicant_id", back_populates="applicant")
    referred_applications = relationship("Application", foreign_keys="Application.referred_by", back_populates="referrer")
    attendance_records = relationship("Attendance", back_populates="employee")
    leave_requests = relationship("LeaveRequest", foreign_keys="LeaveRequest.employee_id", back_populates="employee")
    requests = relationship("Request", foreign_keys="Request.employee_id", back_populates="employee")
    payslips = relationship("Payslip", back_populates="employee")
    goals = relationship("Goal", foreign_keys="Goal.employee_id", back_populates="employee")
    skill_developments = relationship("SkillDevelopment", back_populates="employee")
    skill_enrollments = relationship("SkillModuleEnrollment", back_populates="employee")
    feedback_received = relationship("Feedback", foreign_keys="Feedback.employee_id", back_populates="employee")
    feedback_given = relationship("Feedback", foreign_keys="Feedback.given_by", back_populates="given_by_user")
    notifications = relationship("Notification", back_populates="user")

# Job Listings Model
class JobListing(Base):
    __tablename__ = 'job_listings'
    
    id = Column(Integer, primary_key=True)
    position = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
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
    department = relationship("Department")
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
    referred_by = Column(Integer, ForeignKey('users.id'))
    
    # Status and screening
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    screening_score = Column(Float)
    screening_notes = Column(Text)
    
    # Timestamps
    applied_date = Column(DateTime, default=datetime.utcnow)
    reviewed_date = Column(DateTime)
    
    # Relationships
    job = relationship("JobListing", back_populates="applications")
    applicant = relationship("User", foreign_keys=[applicant_id], back_populates="applications")
    referrer = relationship("User", foreign_keys=[referred_by], back_populates="referred_applications")
    screening_result = relationship("ResumeScreeningResult", back_populates="application", uselist=False)

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
    employee = relationship("User", foreign_keys=[employee_id], back_populates="leave_requests")
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
    
    # Metadata
    issued_by = Column(Integer, ForeignKey('users.id'))
    issued_at = Column(DateTime, default=datetime.utcnow)
    generated_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", foreign_keys=[employee_id], back_populates="payslips")
    issued_by_user = relationship("User", foreign_keys=[issued_by])

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
    employee = relationship("User", foreign_keys=[employee_id], back_populates="goals")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])
    checkpoints = relationship("GoalCheckpoint", back_populates="goal", cascade="all, delete-orphan")

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
    acknowledgments = relationship("PolicyAcknowledgment", back_populates="policy", cascade="all, delete-orphan")

# Policy Acknowledgment Model (for tracking who has acknowledged policies)
class PolicyAcknowledgment(Base):
    __tablename__ = 'policy_acknowledgments'
    
    id = Column(Integer, primary_key=True)
    policy_id = Column(Integer, ForeignKey('policies.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    acknowledged_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    policy = relationship("Policy", back_populates="acknowledgments")
    user = relationship("User")

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
    application = relationship("Application", back_populates="screening_result")

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
    employee = relationship("User", foreign_keys=[employee_id])
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

# Holiday Model (for dashboard "Upcoming holidays")
class Holiday(Base):
    __tablename__ = 'holidays'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    holiday_type = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    created_by_user = relationship("User")

# Request Model (for Manager's "Team requests" page)
class Request(Base):
    __tablename__ = 'requests'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    request_type = Column(Enum(RequestType), nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    request_date = Column(Date)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by = Column(Integer, ForeignKey('users.id'))
    approved_date = Column(DateTime)
    rejection_reason = Column(Text)
    submitted_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", foreign_keys=[employee_id], back_populates="requests")
    approver = relationship("User", foreign_keys=[approved_by])

# Feedback Model (for FeedbackPage.tsx and FeedbackReport.tsx)
class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    given_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    feedback_type = Column(String(50))
    rating = Column(Float)
    given_on = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", foreign_keys=[employee_id], back_populates="feedback_received")
    given_by_user = relationship("User", foreign_keys=[given_by], back_populates="feedback_given")

# Notification Model (for better UX)
class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50))
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="notifications")

# Skill Module Master (for detailed module tracking)
class SkillModule(Base):
    __tablename__ = 'skill_modules'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    module_link = Column(String(500))
    duration_hours = Column(Float)
    difficulty_level = Column(String(20))
    skill_areas = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = relationship("SkillModuleEnrollment", back_populates="module")

# Skill Module Enrollment (for tracking individual module progress)
class SkillModuleEnrollment(Base):
    __tablename__ = 'skill_module_enrollments'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('skill_modules.id'), nullable=False)
    status = Column(Enum(ModuleStatus), default=ModuleStatus.NOT_STARTED)
    progress_percentage = Column(Float, default=0.0)
    enrolled_date = Column(Date, default=datetime.utcnow)
    started_date = Column(Date)
    completed_date = Column(Date)
    target_completion_date = Column(Date)
    certificate_path = Column(String(255))
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", back_populates="skill_enrollments")
    module = relationship("SkillModule", back_populates="enrollments")
