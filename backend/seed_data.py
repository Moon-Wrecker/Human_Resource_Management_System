"""
Seed database with realistic dummy data
Run: python seed_data.py
"""
from datetime import datetime, timedelta, date
import random
from database import SessionLocal
from utils.password_utils import hash_password
from models import (
    Department, Team, User, UserRole, JobListing, Application, ApplicationStatus,
    Announcement, Attendance, AttendanceStatus, LeaveRequest, LeaveType, LeaveStatus,
    Payslip, Goal, GoalStatus, GoalCheckpoint, SkillDevelopment, SkillModule, 
    SkillModuleEnrollment, ModuleStatus, Policy, ResumeScreeningResult, 
    PerformanceReport, Holiday, Request, RequestType, Feedback, Notification
)

def clear_database(session):
    """Clear all existing data"""
    print("Clearing existing data...")
    session.query(Notification).delete()
    session.query(Feedback).delete()
    session.query(Request).delete()
    session.query(Holiday).delete()
    session.query(SkillModuleEnrollment).delete()
    session.query(SkillModule).delete()
    session.query(ResumeScreeningResult).delete()
    session.query(PerformanceReport).delete()
    session.query(GoalCheckpoint).delete()
    session.query(Goal).delete()
    session.query(SkillDevelopment).delete()
    session.query(Payslip).delete()
    session.query(LeaveRequest).delete()
    session.query(Attendance).delete()
    session.query(Application).delete()
    session.query(Announcement).delete()
    session.query(Policy).delete()
    session.query(JobListing).delete()
    session.query(User).delete()
    session.query(Team).delete()
    session.query(Department).delete()
    session.commit()
    print("Database cleared!")

def seed_departments(session):
    """Create departments"""
    print("\nCreating departments...")
    departments = [
        Department(name="Engineering", code="ENG", description="Software Development and Engineering"),
        Department(name="Human Resources", code="HR", description="HR and People Operations"),
        Department(name="Finance", code="FIN", description="Finance and Accounting"),
        Department(name="Sales", code="SAL", description="Sales and Business Development"),
        Department(name="Operations", code="OPS", description="Operations and Support"),
    ]
    session.add_all(departments)
    session.commit()
    print(f"Created {len(departments)} departments")
    return departments

def seed_teams(session, departments):
    """Create teams"""
    print("\nCreating teams...")
    teams = [
        Team(name="Backend Team", department_id=departments[0].id, description="Backend development team"),
        Team(name="Frontend Team", department_id=departments[0].id, description="Frontend development team"),
        Team(name="Recruitment", department_id=departments[1].id, description="Talent acquisition team"),
        Team(name="Payroll Team", department_id=departments[2].id, description="Payroll processing team"),
        Team(name="Sales North", department_id=departments[3].id, description="North region sales"),
    ]
    session.add_all(teams)
    session.commit()
    print(f"Created {len(teams)} teams")
    return teams

def seed_users(session, departments, teams):
    """Create users with different roles"""
    print("\nCreating users...")
    
    # Admin/HR users
    hr_manager = User(
        name="Sarah Johnson",
        email="sarah.johnson@company.com",
        phone="+1-555-0101",
        password_hash=hash_password("pass123"),
        role=UserRole.HR,
        employee_id="EMP001",
        department_id=departments[1].id,
        job_role="HR Manager",
        job_level="Manager",
        hierarchy_level=3,  # Level 3 = Manager
        team_id=teams[2].id,
        hire_date=date(2020, 1, 15),
        salary=95000.0,
        casual_leave_balance=12,
        sick_leave_balance=12,
        annual_leave_balance=15,
        wfh_balance=24,
        is_active=True
    )
    
    # Managers
    eng_manager = User(
        name="Michael Chen",
        email="michael.chen@company.com",
        phone="+1-555-0102",
        password_hash=hash_password("pass123"),
        role=UserRole.MANAGER,
        employee_id="EMP002",
        department_id=departments[0].id,
        job_role="Engineering Manager",
        job_level="Manager",
        hierarchy_level=3,  # Level 3 = Manager
        team_id=teams[0].id,
        hire_date=date(2019, 3, 20),
        salary=110000.0,
        casual_leave_balance=10,
        sick_leave_balance=12,
        annual_leave_balance=15,
        wfh_balance=20,
        is_active=True
    )
    
    frontend_manager = User(
        name="Emily Rodriguez",
        email="emily.rodriguez@company.com",
        phone="+1-555-0103",
        password_hash=hash_password("pass123"),
        role=UserRole.MANAGER,
        employee_id="EMP003",
        department_id=departments[0].id,
        job_role="Frontend Lead",
        job_level="Lead",
        hierarchy_level=4,  # Level 4 = Lead
        team_id=teams[1].id,
        hire_date=date(2019, 6, 10),
        salary=105000.0,
        casual_leave_balance=12,
        sick_leave_balance=10,
        annual_leave_balance=15,
        wfh_balance=18,
        is_active=True
    )
    
    # Employees
    employees = [
        User(
            name="John Doe",
            email="john.doe@company.com",
            phone="+1-555-0104",
            password_hash=hash_password("pass123"),
            role=UserRole.EMPLOYEE,
            employee_id="EMP004",
            department_id=departments[0].id,
            job_role="Senior Software Engineer",
            job_level="Senior",
            hierarchy_level=5,  # Level 5 = Senior
            team_id=teams[0].id,
            manager_id=None,  # Will set after commit
            hire_date=date(2021, 4, 12),
            salary=85000.0,
            casual_leave_balance=8,
            sick_leave_balance=12,
            annual_leave_balance=10,
            wfh_balance=15,
            is_active=True
        ),
        User(
            name="Alice Williams",
            email="alice.williams@company.com",
            phone="+1-555-0105",
            password_hash=hash_password("pass123"),
            role=UserRole.EMPLOYEE,
            employee_id="EMP005",
            department_id=departments[0].id,
            job_role="Software Engineer",
            job_level="Mid-level",
            hierarchy_level=6,  # Level 6 = Mid-level
            team_id=teams[0].id,
            hire_date=date(2022, 1, 10),
            salary=75000.0,
            casual_leave_balance=10,
            sick_leave_balance=11,
            annual_leave_balance=12,
            wfh_balance=20,
            is_active=True
        ),
        User(
            name="Robert Kumar",
            email="robert.kumar@company.com",
            phone="+1-555-0106",
            password_hash=hash_password("pass123"),
            role=UserRole.EMPLOYEE,
            employee_id="EMP006",
            department_id=departments[0].id,
            job_role="Frontend Developer",
            job_level="Mid-level",
            hierarchy_level=6,  # Level 6 = Mid-level
            team_id=teams[1].id,
            hire_date=date(2022, 3, 15),
            salary=72000.0,
            casual_leave_balance=11,
            sick_leave_balance=12,
            annual_leave_balance=13,
            wfh_balance=22,
            is_active=True
        ),
        User(
            name="Maria Garcia",
            email="maria.garcia@company.com",
            phone="+1-555-0107",
            password_hash=hash_password("pass123"),
            role=UserRole.EMPLOYEE,
            employee_id="EMP007",
            department_id=departments[0].id,
            job_role="UI/UX Designer",
            job_level="Senior",
            hierarchy_level=5,  # Level 5 = Senior
            team_id=teams[1].id,
            hire_date=date(2021, 9, 5),
            salary=70000.0,
            casual_leave_balance=9,
            sick_leave_balance=10,
            annual_leave_balance=11,
            wfh_balance=18,
            is_active=True
        ),
        User(
            name="David Lee",
            email="david.lee@company.com",
            phone="+1-555-0108",
            password_hash=hash_password("pass123"),
            role=UserRole.EMPLOYEE,
            employee_id="EMP008",
            department_id=departments[1].id,
            job_role="HR Specialist",
            job_level="Mid-level",
            hierarchy_level=6,  # Level 6 = Mid-level
            team_id=teams[2].id,
            hire_date=date(2021, 7, 20),
            salary=65000.0,
            casual_leave_balance=12,
            sick_leave_balance=12,
            annual_leave_balance=15,
            wfh_balance=20,
            is_active=True
        ),
        User(
            name="Jessica Brown",
            email="jessica.brown@company.com",
            phone="+1-555-0109",
            password_hash=hash_password("pass123"),
            role=UserRole.EMPLOYEE,
            employee_id="EMP009",
            department_id=departments[2].id,
            job_role="Financial Analyst",
            job_level="Mid-level",
            hierarchy_level=6,  # Level 6 = Mid-level
            team_id=teams[3].id,
            hire_date=date(2022, 5, 8),
            salary=68000.0,
            casual_leave_balance=10,
            sick_leave_balance=12,
            annual_leave_balance=14,
            wfh_balance=16,
            is_active=True
        ),
        User(
            name="James Wilson",
            email="james.wilson@company.com",
            phone="+1-555-0110",
            password_hash=hash_password("pass123"),
            role=UserRole.EMPLOYEE,
            employee_id="EMP010",
            department_id=departments[3].id,
            job_role="Sales Executive",
            job_level="Junior",
            hierarchy_level=7,  # Level 7 = Junior
            team_id=teams[4].id,
            hire_date=date(2021, 11, 12),
            salary=60000.0,
            casual_leave_balance=8,
            sick_leave_balance=10,
            annual_leave_balance=12,
            wfh_balance=14,
            is_active=True
        ),
    ]
    
    session.add(hr_manager)
    session.add(eng_manager)
    session.add(frontend_manager)
    session.add_all(employees)
    session.commit()
    
    # Update manager relationships and team managers
    employees[0].manager_id = eng_manager.id
    employees[1].manager_id = eng_manager.id
    employees[2].manager_id = frontend_manager.id
    employees[3].manager_id = frontend_manager.id
    employees[4].manager_id = hr_manager.id
    
    teams[0].manager_id = eng_manager.id
    teams[1].manager_id = frontend_manager.id
    teams[2].manager_id = hr_manager.id
    
    session.commit()
    
    all_users = [hr_manager, eng_manager, frontend_manager] + employees
    print(f"Created {len(all_users)} users")
    return all_users

def seed_job_listings(session, departments, users):
    """Create job listings"""
    print("\nCreating job listings...")
    jobs = [
        JobListing(
            position="Senior Full Stack Developer",
            department_id=departments[0].id,
            experience_required="5+ years",
            skills_required="Python, React, PostgreSQL, Docker",
            description="Looking for experienced full stack developer",
            location="Bangalore",
            employment_type="full-time",
            salary_range="15-20 LPA",
            is_active=True,
            posted_by=users[0].id,
            posted_date=datetime.now() - timedelta(days=10),
            application_deadline=date.today() + timedelta(days=20)
        ),
        JobListing(
            position="Frontend Developer",
            department_id=departments[0].id,
            experience_required="2-3 years",
            skills_required="React, TypeScript, Tailwind CSS",
            description="Join our frontend team",
            location="Remote",
            employment_type="full-time",
            salary_range="10-12 LPA",
            is_active=True,
            posted_by=users[0].id,
            posted_date=datetime.now() - timedelta(days=5)
        ),
    ]
    session.add_all(jobs)
    session.commit()
    print(f"Created {len(jobs)} job listings")
    return jobs

def seed_applications(session, jobs, users):
    """Create applications"""
    print("\nCreating applications...")
    applications = [
        Application(
            job_id=jobs[0].id,
            applicant_name="Priya Sharma",
            applicant_email="priya.sharma@email.com",
            applicant_phone="+91-9876543210",
            source="self-applied",
            status=ApplicationStatus.PENDING,
            applied_date=datetime.now() - timedelta(days=3)
        ),
        Application(
            job_id=jobs[0].id,
            applicant_name="Rahul Verma",
            applicant_email="rahul.verma@email.com",
            applicant_phone="+91-9876543211",
            source="referral",
            referred_by=users[3].id,
            status=ApplicationStatus.REVIEWED,
            applied_date=datetime.now() - timedelta(days=5),
            screening_score=85.5
        ),
    ]
    session.add_all(applications)
    session.commit()
    print(f"Created {len(applications)} applications")
    return applications

def seed_attendance(session, users):
    """Create attendance records"""
    print("\nCreating attendance records...")
    attendance_records = []
    
    for user in users[3:]:  # Only employees
        for days_ago in range(10):
            attendance_date = date.today() - timedelta(days=days_ago)
            status = random.choice([AttendanceStatus.PRESENT, AttendanceStatus.PRESENT, AttendanceStatus.PRESENT, AttendanceStatus.WFH])
            
            if status == AttendanceStatus.PRESENT:
                check_in = datetime.combine(attendance_date, datetime.min.time()) + timedelta(hours=9, minutes=random.randint(0, 30))
                check_out = datetime.combine(attendance_date, datetime.min.time()) + timedelta(hours=18, minutes=random.randint(0, 60))
                hours = (check_out - check_in).seconds / 3600
            else:
                check_in = datetime.combine(attendance_date, datetime.min.time()) + timedelta(hours=10, minutes=random.randint(0, 30))
                check_out = datetime.combine(attendance_date, datetime.min.time()) + timedelta(hours=17, minutes=random.randint(0, 60))
                hours = (check_out - check_in).seconds / 3600
            
            attendance_records.append(Attendance(
                employee_id=user.id,
                date=attendance_date,
                status=status,
                check_in_time=check_in,
                check_out_time=check_out,
                hours_worked=hours,
                location="office" if status == AttendanceStatus.PRESENT else "home"
            ))
    
    session.add_all(attendance_records)
    session.commit()
    print(f"Created {len(attendance_records)} attendance records")

def seed_leave_requests(session, users):
    """Create leave requests"""
    print("\nCreating leave requests...")
    leaves = [
        LeaveRequest(
            employee_id=users[3].id,
            leave_type=LeaveType.CASUAL,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=7),
            days_requested=3,
            subject="Family event",
            reason="Attending family wedding",
            status=LeaveStatus.PENDING,
            requested_date=datetime.now()
        ),
        LeaveRequest(
            employee_id=users[4].id,
            leave_type=LeaveType.ANNUAL,
            start_date=date.today() + timedelta(days=15),
            end_date=date.today() + timedelta(days=20),
            days_requested=5,
            subject="Vacation",
            reason="Planned vacation",
            status=LeaveStatus.APPROVED,
            approved_by=users[1].id,
            approved_date=datetime.now() - timedelta(days=1),
            requested_date=datetime.now() - timedelta(days=2)
        ),
    ]
    session.add_all(leaves)
    session.commit()
    print(f"Created {len(leaves)} leave requests")

def seed_holidays(session, users):
    """Create holidays"""
    print("\nCreating holidays...")
    holidays = [
        Holiday(name="Diwali", start_date=date(2024, 11, 1), end_date=date(2024, 11, 1), is_mandatory=True, holiday_type="national", created_by=users[0].id),
        Holiday(name="Christmas", start_date=date(2024, 12, 25), end_date=date(2024, 12, 25), is_mandatory=True, holiday_type="national", created_by=users[0].id),
        Holiday(name="New Year", start_date=date(2025, 1, 1), end_date=date(2025, 1, 1), is_mandatory=True, holiday_type="national", created_by=users[0].id),
        Holiday(name="Republic Day", start_date=date(2025, 1, 26), end_date=date(2025, 1, 26), is_mandatory=True, holiday_type="national", created_by=users[0].id),
    ]
    session.add_all(holidays)
    session.commit()
    print(f"Created {len(holidays)} holidays")

def seed_goals(session, users):
    """Create goals and checkpoints"""
    print("\nCreating goals...")
    goals = [
        Goal(
            employee_id=users[3].id,
            title="Complete React Advanced Course",
            description="Master advanced React patterns and hooks",
            category="learning",
            start_date=date(2024, 10, 1),
            target_date=date(2024, 12, 31),
            status=GoalStatus.IN_PROGRESS,
            progress_percentage=60.0,
            assigned_by=users[1].id
        ),
        Goal(
            employee_id=users[4].id,
            title="Improve Code Quality",
            description="Reduce technical debt in legacy codebase",
            category="performance",
            start_date=date(2024, 11, 1),
            target_date=date(2025, 1, 31),
            status=GoalStatus.NOT_STARTED,
            progress_percentage=0.0,
            assigned_by=users[1].id
        ),
    ]
    session.add_all(goals)
    session.commit()
    
    # Add checkpoints
    checkpoints = [
        GoalCheckpoint(goal_id=goals[0].id, title="Complete basic modules", sequence_number=1, is_completed=True, completed_date=datetime.now() - timedelta(days=10)),
        GoalCheckpoint(goal_id=goals[0].id, title="Build sample project", sequence_number=2, is_completed=False),
        GoalCheckpoint(goal_id=goals[0].id, title="Pass final assessment", sequence_number=3, is_completed=False),
    ]
    session.add_all(checkpoints)
    session.commit()
    print(f"Created {len(goals)} goals with checkpoints")

def seed_skill_modules(session, users):
    """Create skill modules and enrollments"""
    print("\nCreating skill modules...")
    modules = [
        SkillModule(name="Python Advanced", description="Advanced Python concepts", category="Programming", module_link="https://example.com/python", duration_hours=40, difficulty_level="advanced"),
        SkillModule(name="React Fundamentals", description="Learn React basics", category="Frontend", module_link="https://example.com/react", duration_hours=30, difficulty_level="intermediate"),
        SkillModule(name="Docker & Kubernetes", description="Container orchestration", category="DevOps", module_link="https://example.com/docker", duration_hours=35, difficulty_level="advanced"),
    ]
    session.add_all(modules)
    session.commit()
    
    enrollments = [
        SkillModuleEnrollment(employee_id=users[3].id, module_id=modules[0].id, status=ModuleStatus.COMPLETED, progress_percentage=100.0, 
                             enrolled_date=date(2024, 9, 1), completed_date=date(2024, 10, 15)),
        SkillModuleEnrollment(employee_id=users[3].id, module_id=modules[1].id, status=ModuleStatus.PENDING, progress_percentage=60.0, 
                             enrolled_date=date(2024, 10, 1)),
        SkillModuleEnrollment(employee_id=users[4].id, module_id=modules[1].id, status=ModuleStatus.NOT_STARTED, progress_percentage=0.0, 
                             enrolled_date=date(2024, 11, 1)),
    ]
    session.add_all(enrollments)
    session.commit()
    print(f"Created {len(modules)} skill modules")

def seed_feedback(session, users):
    """Create feedback"""
    print("\nCreating feedback...")
    feedbacks = [
        Feedback(employee_id=users[3].id, given_by=users[1].id, subject="Great work on Q3 project", 
                description="Excellent performance and team collaboration", rating=4.5, given_on=datetime.now() - timedelta(days=5)),
        Feedback(employee_id=users[4].id, given_by=users[1].id, subject="Code review improvements needed",
                description="Good progress but needs attention to code quality", rating=3.8, given_on=datetime.now() - timedelta(days=3)),
    ]
    session.add_all(feedbacks)
    session.commit()
    print(f"Created {len(feedbacks)} feedback entries")

def seed_announcements(session, users):
    """Create announcements"""
    print("\nCreating announcements...")
    announcements = [
        Announcement(
            title="Company Holiday - Diwali",
            message="Office will be closed on November 1st for Diwali celebration",
            is_urgent=True,
            created_by=users[0].id,
            published_date=datetime.now() - timedelta(days=7)
        ),
        Announcement(
            title="New Health Insurance Policy",
            message="Updated health insurance benefits are now available. Check the policy section for details.",
            created_by=users[0].id,
            published_date=datetime.now() - timedelta(days=3)
        ),
    ]
    session.add_all(announcements)
    session.commit()
    print(f"Created {len(announcements)} announcements")

def seed_policies(session, users):
    """Create policies"""
    print("\nCreating policies...")
    policies = [
        Policy(
            title="Work From Home Policy",
            description="Guidelines for remote work",
            content="Employees can work from home up to 2 days per week with manager approval...",
            category="HR",
            version="2.0",
            effective_date=date(2024, 1, 1),
            created_by=users[0].id
        ),
        Policy(
            title="Leave Policy",
            description="Annual leave and sick leave policy",
            content="All employees are entitled to 15 days of annual leave...",
            category="HR",
            version="1.5",
            effective_date=date(2024, 1, 1),
            created_by=users[0].id
        ),
    ]
    session.add_all(policies)
    session.commit()
    print(f"Created {len(policies)} policies")

def seed_payslips(session, users):
    """Create payslips"""
    print("\nCreating payslips...")
    payslips = []
    
    for user in users[3:8]:  # Create for 5 employees
        payslip = Payslip(
            employee_id=user.id,
            pay_period_start=date(2024, 10, 1),
            pay_period_end=date(2024, 10, 31),
            pay_date=date(2024, 11, 1),
            basic_salary=user.salary * 0.6,
            allowances=user.salary * 0.3,
            overtime_pay=0,
            bonus=user.salary * 0.1,
            gross_salary=user.salary,
            tax_deduction=user.salary * 0.2,
            pf_deduction=user.salary * 0.08,
            insurance_deduction=500,
            other_deductions=0,
            total_deductions=user.salary * 0.28 + 500,
            net_salary=user.salary * 0.72 - 500,
            generated_date=datetime(2024, 11, 1)
        )
        payslips.append(payslip)
    
    session.add_all(payslips)
    session.commit()
    print(f"Created {len(payslips)} payslips")

def seed_requests(session, users):
    """Create requests"""
    print("\nCreating requests...")
    requests = [
        Request(
            employee_id=users[3].id,
            request_type=RequestType.WFH,
            subject="WFH Request for Monday",
            description="Need to work from home due to home maintenance",
            request_date=date.today() + timedelta(days=3),
            status=LeaveStatus.PENDING,
            submitted_date=datetime.now()
        ),
        Request(
            employee_id=users[4].id,
            request_type=RequestType.EQUIPMENT,
            subject="New Monitor Request",
            description="Requesting a second monitor for better productivity",
            status=LeaveStatus.APPROVED,
            approved_by=users[1].id,
            approved_date=datetime.now() - timedelta(days=1),
            submitted_date=datetime.now() - timedelta(days=2)
        ),
    ]
    session.add_all(requests)
    session.commit()
    print(f"Created {len(requests)} requests")

def seed_notifications(session, users):
    """Create notifications"""
    print("\nCreating notifications...")
    notifications = [
        Notification(user_id=users[3].id, title="Leave Approved", message="Your leave request has been approved", 
                    notification_type="success", is_read=False, created_at=datetime.now() - timedelta(hours=2)),
        Notification(user_id=users[3].id, title="New Announcement", message="Check out the new company policy", 
                    notification_type="info", is_read=False, created_at=datetime.now() - timedelta(hours=5)),
        Notification(user_id=users[4].id, title="Goal Updated", message="Your manager updated your goal progress", 
                    notification_type="info", is_read=True, read_at=datetime.now() - timedelta(hours=1), created_at=datetime.now() - timedelta(hours=3)),
    ]
    session.add_all(notifications)
    session.commit()
    print(f"Created {len(notifications)} notifications")

def main():
    """Main seeding function"""
    print("="*60)
    print("Starting database seeding...")
    print("="*60)
    
    session = SessionLocal()
    
    try:
        # Clear existing data
        clear_database(session)
        
        # Seed data in order (respecting foreign keys)
        departments = seed_departments(session)
        teams = seed_teams(session, departments)
        users = seed_users(session, departments, teams)
        jobs = seed_job_listings(session, departments, users)
        applications = seed_applications(session, jobs, users)
        seed_attendance(session, users)
        seed_leave_requests(session, users)
        seed_holidays(session, users)
        seed_goals(session, users)
        seed_skill_modules(session, users)
        seed_feedback(session, users)
        seed_announcements(session, users)
        seed_policies(session, users)
        seed_payslips(session, users)
        seed_requests(session, users)
        seed_notifications(session, users)
        
        print("\n" + "="*60)
        print("Database seeded successfully!")
        print("="*60)
        print("\nTest Credentials:")
        print("  HR: sarah.johnson@company.com / pass123")
        print("  Manager: michael.chen@company.com / pass123")
        print("  Employee: john.doe@company.com / pass123")
        print("="*60)
        
    except Exception as e:
        print(f"\n[ERROR] Error seeding database: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()

