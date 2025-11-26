"""
Comprehensive seed database with 15 rows per table of realistic data
Run: python seed_comprehensive.py
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
    """Create 15 departments"""
    print("\nCreating departments...")
    departments = [
        Department(name="Engineering", code="ENG", description="Software Development and Engineering"),
        Department(name="Human Resources", code="HR", description="HR and People Operations"),
        Department(name="Finance", code="FIN", description="Finance and Accounting"),
        Department(name="Sales", code="SAL", description="Sales and Business Development"),
        Department(name="Marketing", code="MKT", description="Marketing and Brand Management"),
        Department(name="Operations", code="OPS", description="Operations and Support"),
        Department(name="Product Management", code="PRD", description="Product Strategy and Management"),
        Department(name="Quality Assurance", code="QA", description="Quality Testing and Assurance"),
        Department(name="Customer Success", code="CS", description="Customer Support and Success"),
        Department(name="Data Science", code="DS", description="Data Analytics and Machine Learning"),
        Department(name="DevOps", code="DVO", description="DevOps and Infrastructure"),
        Department(name="Legal", code="LGL", description="Legal and Compliance"),
        Department(name="Research & Development", code="RND", description="Innovation and Research"),
        Department(name="IT Support", code="IT", description="Information Technology Support"),
        Department(name="Business Intelligence", code="BI", description="Business Analytics and Insights"),
    ]
    session.add_all(departments)
    session.commit()
    print(f"Created {len(departments)} departments")
    return departments

def seed_teams(session, departments):
    """Create 15 teams"""
    print("\nCreating teams...")
    teams = [
        Team(name="Backend Team", department_id=departments[0].id, description="Backend development team"),
        Team(name="Frontend Team", department_id=departments[0].id, description="Frontend development team"),
        Team(name="Mobile App Team", department_id=departments[0].id, description="iOS and Android development"),
        Team(name="Recruitment", department_id=departments[1].id, description="Talent acquisition team"),
        Team(name="Employee Relations", department_id=departments[1].id, description="Employee engagement and relations"),
        Team(name="Payroll Team", department_id=departments[2].id, description="Payroll processing team"),
        Team(name="Financial Planning", department_id=departments[2].id, description="Budget and financial planning"),
        Team(name="Sales North", department_id=departments[3].id, description="North region sales"),
        Team(name="Sales South", department_id=departments[3].id, description="South region sales"),
        Team(name="Digital Marketing", department_id=departments[4].id, description="Online marketing and campaigns"),
        Team(name="Content Team", department_id=departments[4].id, description="Content creation and strategy"),
        Team(name="Product Design", department_id=departments[6].id, description="Product design and UX"),
        Team(name="Automation QA", department_id=departments[7].id, description="Automated testing team"),
        Team(name="ML Engineering", department_id=departments[9].id, description="Machine learning and AI"),
        Team(name="Cloud Infrastructure", department_id=departments[10].id, description="Cloud and infrastructure management"),
    ]
    session.add_all(teams)
    session.commit()
    print(f"Created {len(teams)} teams")
    return teams

def seed_users(session, departments, teams):
    """Create 15+ users with different roles"""
    print("\nCreating users...")
    
    users_data = [
        # HR
        {"name": "Sarah Johnson", "email": "sarah.johnson@company.com", "phone": "+1-555-0101", "role": UserRole.HR, 
         "employee_id": "EMP001", "dept": 1, "job_role": "HR Manager", "job_level": "Manager", "hierarchy": 3, 
         "team": 3, "hire_date": date(2018, 3, 15), "salary": 95000.0},
        
        {"name": "Linda Martinez", "email": "linda.martinez@company.com", "phone": "+1-555-0102", "role": UserRole.HR,
         "employee_id": "EMP002", "dept": 1, "job_role": "HR Business Partner", "job_level": "Senior", "hierarchy": 5,
         "team": 4, "hire_date": date(2019, 7, 20), "salary": 82000.0},
        
        # Managers
        {"name": "Michael Chen", "email": "michael.chen@company.com", "phone": "+1-555-0103", "role": UserRole.MANAGER,
         "employee_id": "EMP003", "dept": 0, "job_role": "Engineering Manager", "job_level": "Manager", "hierarchy": 3,
         "team": 0, "hire_date": date(2017, 5, 10), "salary": 115000.0},
        
        {"name": "Emily Rodriguez", "email": "emily.rodriguez@company.com", "phone": "+1-555-0104", "role": UserRole.MANAGER,
         "employee_id": "EMP004", "dept": 0, "job_role": "Frontend Lead", "job_level": "Lead", "hierarchy": 4,
         "team": 1, "hire_date": date(2018, 9, 12), "salary": 105000.0},
        
        {"name": "David Kim", "email": "david.kim@company.com", "phone": "+1-555-0105", "role": UserRole.MANAGER,
         "employee_id": "EMP005", "dept": 9, "job_role": "Data Science Manager", "job_level": "Manager", "hierarchy": 3,
         "team": 13, "hire_date": date(2019, 1, 8), "salary": 125000.0},
        
        # Employees - Engineering
        {"name": "John Anderson", "email": "john.anderson@company.com", "phone": "+1-555-0106", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP006", "dept": 0, "job_role": "Senior Backend Engineer", "job_level": "Senior", "hierarchy": 5,
         "team": 0, "hire_date": date(2019, 11, 5), "salary": 92000.0, "manager": 2},
        
        {"name": "Alice Williams", "email": "alice.williams@company.com", "phone": "+1-555-0107", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP007", "dept": 0, "job_role": "Backend Engineer", "job_level": "Mid-level", "hierarchy": 6,
         "team": 0, "hire_date": date(2020, 3, 18), "salary": 78000.0, "manager": 2},
        
        {"name": "Robert Kumar", "email": "robert.kumar@company.com", "phone": "+1-555-0108", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP008", "dept": 0, "job_role": "Frontend Developer", "job_level": "Mid-level", "hierarchy": 6,
         "team": 1, "hire_date": date(2020, 6, 22), "salary": 75000.0, "manager": 3},
        
        {"name": "Maria Garcia", "email": "maria.garcia@company.com", "phone": "+1-555-0109", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP009", "dept": 0, "job_role": "Senior Frontend Developer", "job_level": "Senior", "hierarchy": 5,
         "team": 1, "hire_date": date(2019, 8, 14), "salary": 88000.0, "manager": 3},
        
        {"name": "James Wilson", "email": "james.wilson@company.com", "phone": "+1-555-0110", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP010", "dept": 0, "job_role": "Mobile Developer", "job_level": "Mid-level", "hierarchy": 6,
         "team": 2, "hire_date": date(2021, 2, 10), "salary": 76000.0, "manager": 2},
        
        # Data Science & ML
        {"name": "Priya Sharma", "email": "priya.sharma@company.com", "phone": "+1-555-0111", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP011", "dept": 9, "job_role": "Senior Data Scientist", "job_level": "Senior", "hierarchy": 5,
         "team": 13, "hire_date": date(2020, 1, 20), "salary": 95000.0, "manager": 4},
        
        {"name": "Daniel Brown", "email": "daniel.brown@company.com", "phone": "+1-555-0112", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP012", "dept": 9, "job_role": "ML Engineer", "job_level": "Mid-level", "hierarchy": 6,
         "team": 13, "hire_date": date(2021, 5, 15), "salary": 82000.0, "manager": 4},
        
        # QA
        {"name": "Jessica Lee", "email": "jessica.lee@company.com", "phone": "+1-555-0113", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP013", "dept": 7, "job_role": "Senior QA Engineer", "job_level": "Senior", "hierarchy": 5,
         "team": 12, "hire_date": date(2019, 4, 8), "salary": 79000.0, "manager": 2},
        
        # Product & Design
        {"name": "Thomas Miller", "email": "thomas.miller@company.com", "phone": "+1-555-0114", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP014", "dept": 6, "job_role": "Product Manager", "job_level": "Senior", "hierarchy": 5,
         "team": 11, "hire_date": date(2018, 11, 3), "salary": 98000.0, "manager": 3},
        
        {"name": "Emma Davis", "email": "emma.davis@company.com", "phone": "+1-555-0115", "role": UserRole.EMPLOYEE,
         "employee_id": "EMP015", "dept": 6, "job_role": "UX Designer", "job_level": "Mid-level", "hierarchy": 6,
         "team": 11, "hire_date": date(2020, 9, 25), "salary": 72000.0, "manager": 3},
    ]
    
    users = []
    for user_data in users_data:
        dept_idx = user_data.pop("dept")
        team_idx = user_data.pop("team")
        manager_idx = user_data.pop("manager", None)
        
        user = User(
            name=user_data["name"],
            email=user_data["email"],
            phone=user_data["phone"],
            password_hash=hash_password("pass123"),
            role=user_data["role"],
            employee_id=user_data["employee_id"],
            department_id=departments[dept_idx].id,
            job_role=user_data["job_role"],
            job_level=user_data["job_level"],
            hierarchy_level=user_data["hierarchy"],
            team_id=teams[team_idx].id,
            hire_date=user_data["hire_date"],
            salary=user_data["salary"],
            casual_leave_balance=random.randint(8, 12),
            sick_leave_balance=random.randint(8, 12),
            annual_leave_balance=random.randint(10, 15),
            wfh_balance=random.randint(15, 24),
            is_active=True
        )
        users.append(user)
    
    session.add_all(users)
    session.commit()
    
    # Update manager relationships
    users[5].manager_id = users[2].id  # John -> Michael
    users[6].manager_id = users[2].id  # Alice -> Michael
    users[7].manager_id = users[3].id  # Robert -> Emily
    users[8].manager_id = users[3].id  # Maria -> Emily
    users[9].manager_id = users[2].id  # James -> Michael
    users[10].manager_id = users[4].id  # Priya -> David
    users[11].manager_id = users[4].id  # Daniel -> David
    users[12].manager_id = users[2].id  # Jessica -> Michael
    users[13].manager_id = users[3].id  # Thomas -> Emily
    users[14].manager_id = users[3].id  # Emma -> Emily
    
    # Set team managers
    teams[0].manager_id = users[2].id  # Michael
    teams[1].manager_id = users[3].id  # Emily
    teams[13].manager_id = users[4].id  # David
    
    # Set department heads
    departments[0].head_id = users[2].id
    departments[1].head_id = users[0].id
    departments[9].head_id = users[4].id
    
    session.commit()
    print(f"Created {len(users)} users")
    return users

def seed_job_listings(session, departments, users):
    """Create 15 job listings"""
    print("\nCreating job listings...")
    
    jobs_data = [
        {"position": "Senior Backend Engineer", "dept": 0, "exp": "5-7 years", "skills": "Python, Django, PostgreSQL, Redis, AWS",
         "desc": "Looking for experienced backend engineer to build scalable APIs", "location": "Bangalore", "type": "full-time", "salary": "₹18-25 LPA"},
        
        {"position": "Frontend Developer", "dept": 0, "exp": "3-5 years", "skills": "React, TypeScript, Redux, Tailwind CSS",
         "desc": "Join our frontend team to build beautiful user interfaces", "location": "Remote", "type": "full-time", "salary": "₹12-18 LPA"},
        
        {"position": "Full Stack Developer", "dept": 0, "exp": "4-6 years", "skills": "Node.js, React, MongoDB, Docker",
         "desc": "Versatile developer for both frontend and backend", "location": "Hyderabad", "type": "full-time", "salary": "₹15-22 LPA"},
        
        {"position": "Data Scientist", "dept": 9, "exp": "3-5 years", "skills": "Python, Machine Learning, TensorFlow, SQL",
         "desc": "Build ML models and derive insights from data", "location": "Pune", "type": "full-time", "salary": "₹16-24 LPA"},
        
        {"position": "DevOps Engineer", "dept": 10, "exp": "4-6 years", "skills": "Kubernetes, Docker, AWS, CI/CD, Terraform",
         "desc": "Manage cloud infrastructure and deployment pipelines", "location": "Bangalore", "type": "full-time", "salary": "₹18-26 LPA"},
        
        {"position": "Product Manager", "dept": 6, "exp": "5-8 years", "skills": "Product Strategy, Agile, User Research",
         "desc": "Lead product development from concept to launch", "location": "Mumbai", "type": "full-time", "salary": "₹20-30 LPA"},
        
        {"position": "QA Automation Engineer", "dept": 7, "exp": "3-5 years", "skills": "Selenium, Pytest, CI/CD, API Testing",
         "desc": "Build and maintain automated test suites", "location": "Chennai", "type": "full-time", "salary": "₹12-18 LPA"},
        
        {"position": "UX Designer", "dept": 6, "exp": "2-4 years", "skills": "Figma, User Research, Prototyping, Design Systems",
         "desc": "Create delightful user experiences", "location": "Bangalore", "type": "full-time", "salary": "₹10-16 LPA"},
        
        {"position": "Mobile Developer (React Native)", "dept": 0, "exp": "3-5 years", "skills": "React Native, iOS, Android, JavaScript",
         "desc": "Build cross-platform mobile applications", "location": "Remote", "type": "full-time", "salary": "₹14-20 LPA"},
        
        {"position": "HR Business Partner", "dept": 1, "exp": "4-6 years", "skills": "Employee Relations, Recruitment, HR Analytics",
         "desc": "Strategic HR partner for business units", "location": "Delhi", "type": "full-time", "salary": "₹12-18 LPA"},
        
        {"position": "Sales Manager", "dept": 3, "exp": "5-7 years", "skills": "B2B Sales, Team Management, CRM",
         "desc": "Lead sales team and drive revenue growth", "location": "Mumbai", "type": "full-time", "salary": "₹15-25 LPA"},
        
        {"position": "Content Marketing Manager", "dept": 4, "exp": "4-6 years", "skills": "Content Strategy, SEO, Social Media",
         "desc": "Create engaging content and marketing campaigns", "location": "Bangalore", "type": "full-time", "salary": "₹12-18 LPA"},
        
        {"position": "Financial Analyst", "dept": 2, "exp": "2-4 years", "skills": "Financial Modeling, Excel, SQL, Tableau",
         "desc": "Analyze financial data and prepare reports", "location": "Pune", "type": "full-time", "salary": "₹10-15 LPA"},
        
        {"position": "Customer Success Manager", "dept": 8, "exp": "3-5 years", "skills": "Customer Relations, Problem Solving, CRM",
         "desc": "Ensure customer satisfaction and retention", "location": "Remote", "type": "full-time", "salary": "₹10-16 LPA"},
        
        {"position": "Business Analyst", "dept": 14, "exp": "3-5 years", "skills": "Business Analysis, SQL, Data Visualization, Requirements Gathering",
         "desc": "Bridge business needs with technical solutions", "location": "Bangalore", "type": "full-time", "salary": "₹12-18 LPA"},
    ]
    
    jobs = []
    for i, job_data in enumerate(jobs_data):
        job = JobListing(
            position=job_data["position"],
            department_id=departments[job_data["dept"]].id,
            experience_required=job_data["exp"],
            skills_required=job_data["skills"],
            description=job_data["desc"],
            location=job_data["location"],
            employment_type=job_data["type"],
            salary_range=job_data["salary"],
            is_active=i < 12,  # Last 3 are inactive
            posted_by=users[0].id if i % 2 == 0 else users[1].id,
            posted_date=datetime.now() - timedelta(days=random.randint(1, 30)),
            application_deadline=date.today() + timedelta(days=random.randint(15, 60))
        )
        jobs.append(job)
    
    session.add_all(jobs)
    session.commit()
    print(f"Created {len(jobs)} job listings")
    return jobs

def seed_applications(session, jobs, users):
    """Create 15 applications"""
    print("\nCreating applications...")
    
    applicants = [
        {"name": "Rajesh Patel", "email": "rajesh.patel@email.com", "phone": "+91-9876543210"},
        {"name": "Anjali Reddy", "email": "anjali.reddy@email.com", "phone": "+91-9876543211"},
        {"name": "Vikram Singh", "email": "vikram.singh@email.com", "phone": "+91-9876543212"},
        {"name": "Sneha Gupta", "email": "sneha.gupta@email.com", "phone": "+91-9876543213"},
        {"name": "Arjun Nair", "email": "arjun.nair@email.com", "phone": "+91-9876543214"},
        {"name": "Kavya Iyer", "email": "kavya.iyer@email.com", "phone": "+91-9876543215"},
        {"name": "Rahul Verma", "email": "rahul.verma@email.com", "phone": "+91-9876543216"},
        {"name": "Neha Kapoor", "email": "neha.kapoor@email.com", "phone": "+91-9876543217"},
        {"name": "Aditya Joshi", "email": "aditya.joshi@email.com", "phone": "+91-9876543218"},
        {"name": "Pooja Mehta", "email": "pooja.mehta@email.com", "phone": "+91-9876543219"},
        {"name": "Karthik Krishnan", "email": "karthik.krishnan@email.com", "phone": "+91-9876543220"},
        {"name": "Divya Saxena", "email": "divya.saxena@email.com", "phone": "+91-9876543221"},
        {"name": "Sanjay Kumar", "email": "sanjay.kumar@email.com", "phone": "+91-9876543222"},
        {"name": "Riya Shah", "email": "riya.shah@email.com", "phone": "+91-9876543223"},
        {"name": "Amit Malhotra", "email": "amit.malhotra@email.com", "phone": "+91-9876543224"},
    ]
    
    statuses = [ApplicationStatus.PENDING, ApplicationStatus.REVIEWED, ApplicationStatus.SHORTLISTED, 
                ApplicationStatus.REJECTED, ApplicationStatus.HIRED]
    sources = ["self-applied", "referral", "recruitment", "self-applied", "referral"]
    
    applications = []
    for i, applicant in enumerate(applicants):
        status = random.choice(statuses)
        source = sources[i % 5]
        
        app = Application(
            job_id=jobs[i % len(jobs)].id,
            applicant_name=applicant["name"],
            applicant_email=applicant["email"],
            applicant_phone=applicant["phone"],
            source=source,
            referred_by=users[5 + (i % 5)].id if source == "referral" else None,
            status=status,
            screening_score=random.uniform(60.0, 95.0) if status != ApplicationStatus.PENDING else None,
            screening_notes=f"Good match for the role" if status != ApplicationStatus.PENDING else None,
            applied_date=datetime.now() - timedelta(days=random.randint(1, 20)),
            reviewed_date=datetime.now() - timedelta(days=random.randint(0, 10)) if status != ApplicationStatus.PENDING else None
        )
        applications.append(app)
    
    session.add_all(applications)
    session.commit()
    print(f"Created {len(applications)} applications")
    return applications

def seed_announcements(session, users):
    """Create 15 announcements"""
    print("\nCreating announcements...")
    
    announcements_data = [
        {"title": "Diwali Holiday", "msg": "Office will be closed on November 1st for Diwali celebrations", "urgent": True, "days_ago": 15},
        {"title": "New Health Insurance Policy", "msg": "Updated health insurance benefits now available. Check policy section.", "urgent": False, "days_ago": 10},
        {"title": "Q4 Town Hall Meeting", "msg": "Join us for Q4 all-hands meeting on Friday at 3 PM", "urgent": True, "days_ago": 5},
        {"title": "Office Renovation Notice", "msg": "4th floor will undergo renovation from next week", "urgent": False, "days_ago": 8},
        {"title": "New Parking Policy", "msg": "Updated parking allocation system effective from next month", "urgent": False, "days_ago": 12},
        {"title": "Annual Performance Reviews", "msg": "Performance review cycle starts next week. Please complete self-assessment.", "urgent": True, "days_ago": 3},
        {"title": "Team Building Event", "msg": "Join us for team outing on Saturday. RSVP by Wednesday.", "urgent": False, "days_ago": 7},
        {"title": "Security System Upgrade", "msg": "New access card system will be implemented. Collect new cards from reception.", "urgent": True, "days_ago": 4},
        {"title": "Holiday Calendar 2025", "msg": "2025 holiday calendar is now published. Plan your leaves accordingly.", "urgent": False, "days_ago": 20},
        {"title": "Wellness Program Launch", "msg": "New employee wellness program with gym memberships and yoga classes", "urgent": False, "days_ago": 6},
        {"title": "COVID-19 Safety Guidelines", "msg": "Updated safety protocols. Masks optional but recommended.", "urgent": True, "days_ago": 25},
        {"title": "New Learning Platform", "msg": "Access to LinkedIn Learning now available for all employees", "urgent": False, "days_ago": 14},
        {"title": "Cafeteria Menu Update", "msg": "New healthy menu options available from Monday", "urgent": False, "days_ago": 9},
        {"title": "Employee Referral Bonus", "msg": "Earn up to ₹50,000 for successful referrals. Check internal job board.", "urgent": False, "days_ago": 11},
        {"title": "Work From Home Policy Update", "msg": "Hybrid work model - 3 days office, 2 days WFH now standard", "urgent": True, "days_ago": 2},
    ]
    
    announcements = []
    for i, ann_data in enumerate(announcements_data):
        ann = Announcement(
            title=ann_data["title"],
            message=ann_data["msg"],
            is_urgent=ann_data["urgent"],
            created_by=users[0].id if i % 2 == 0 else users[1].id,
            published_date=datetime.now() - timedelta(days=ann_data["days_ago"]),
            expiry_date=datetime.now() + timedelta(days=random.randint(30, 90)),
            is_active=i < 12  # Last 3 inactive
        )
        announcements.append(ann)
    
    session.add_all(announcements)
    session.commit()
    print(f"Created {len(announcements)} announcements")

def seed_attendance(session, users):
    """Create attendance records for last 15 days"""
    print("\nCreating attendance records...")
    attendance_records = []
    
    # Create for employees only (skip HR/Managers in first 5)
    for user in users[5:]:
        for days_ago in range(15):
            attendance_date = date.today() - timedelta(days=days_ago)
            
            # 85% present, 10% WFH, 5% leave
            rand = random.random()
            if rand < 0.85:
                status = AttendanceStatus.PRESENT
            elif rand < 0.95:
                status = AttendanceStatus.WFH
            else:
                status = AttendanceStatus.LEAVE
            
            if status in [AttendanceStatus.PRESENT, AttendanceStatus.WFH]:
                check_in = datetime.combine(attendance_date, datetime.min.time()) + timedelta(hours=9, minutes=random.randint(0, 45))
                check_out = datetime.combine(attendance_date, datetime.min.time()) + timedelta(hours=18, minutes=random.randint(0, 90))
                hours = round((check_out - check_in).seconds / 3600, 2)
                location = "office" if status == AttendanceStatus.PRESENT else "home"
            else:
                check_in = None
                check_out = None
                hours = 0.0
                location = None
            
            attendance_records.append(Attendance(
                employee_id=user.id,
                date=attendance_date,
                status=status,
                check_in_time=check_in,
                check_out_time=check_out,
                hours_worked=hours,
                location=location
            ))
    
    session.add_all(attendance_records)
    session.commit()
    print(f"Created {len(attendance_records)} attendance records")

def seed_leave_requests(session, users):
    """Create 15 leave requests"""
    print("\nCreating leave requests...")
    
    leave_types = [LeaveType.CASUAL, LeaveType.SICK, LeaveType.ANNUAL, LeaveType.CASUAL, LeaveType.ANNUAL]
    leave_statuses = [LeaveStatus.PENDING, LeaveStatus.APPROVED, LeaveStatus.APPROVED, LeaveStatus.REJECTED, LeaveStatus.PENDING]
    
    leave_reasons = [
        ("Family Wedding", "Attending cousin's wedding ceremony"),
        ("Medical Checkup", "Annual health checkup scheduled"),
        ("Personal Work", "Need to handle urgent personal matter"),
        ("Vacation", "Planned family vacation to Goa"),
        ("Home Renovation", "Supervising home repairs"),
        ("Parent Visit", "Parents visiting from hometown"),
        ("Fever", "Running high temperature, need rest"),
        ("Travel Plans", "Pre-booked trip to Kerala"),
        ("Festival Celebration", "Celebrating Pongal with family"),
        ("Child Care", "Kids' school annual day event"),
        ("Moving House", "Relocating to new apartment"),
        ("Medical Emergency", "Elderly parent needs care"),
        ("Mental Health Day", "Need personal time off"),
        ("Religious Event", "Attending temple festival"),
        ("Legal Work", "Property registration work"),
    ]
    
    leaves = []
    for i in range(15):
        employee = users[5 + (i % 10)]  # Rotate through employees
        days = random.randint(1, 5)
        start = date.today() + timedelta(days=random.randint(-10, 20))
        status = leave_statuses[i % 5]
        
        leave = LeaveRequest(
            employee_id=employee.id,
            leave_type=leave_types[i % 5],
            start_date=start,
            end_date=start + timedelta(days=days - 1),
            days_requested=days,
            subject=leave_reasons[i][0],
            reason=leave_reasons[i][1],
            status=status,
            approved_by=employee.manager_id if status != LeaveStatus.PENDING else None,
            approved_date=datetime.now() - timedelta(days=random.randint(1, 3)) if status != LeaveStatus.PENDING else None,
            rejection_reason="Team has critical deadlines" if status == LeaveStatus.REJECTED else None,
            requested_date=datetime.now() - timedelta(days=random.randint(1, 7))
        )
        leaves.append(leave)
    
    session.add_all(leaves)
    session.commit()
    print(f"Created {len(leaves)} leave requests")

def seed_holidays(session, users):
    """Create 15 holidays"""
    print("\nCreating holidays...")
    
    holidays_data = [
        {"name": "Republic Day", "date": date(2025, 1, 26), "type": "national"},
        {"name": "Holi", "date": date(2025, 3, 14), "type": "festival"},
        {"name": "Good Friday", "date": date(2025, 4, 18), "type": "religious"},
        {"name": "Eid ul-Fitr", "date": date(2025, 4, 10), "type": "festival"},
        {"name": "May Day", "date": date(2025, 5, 1), "type": "national"},
        {"name": "Independence Day", "date": date(2025, 8, 15), "type": "national"},
        {"name": "Janmashtami", "date": date(2025, 8, 16), "type": "festival"},
        {"name": "Gandhi Jayanti", "date": date(2025, 10, 2), "type": "national"},
        {"name": "Dussehra", "date": date(2025, 10, 2), "type": "festival"},
        {"name": "Diwali", "date": date(2025, 10, 20), "type": "festival"},
        {"name": "Guru Nanak Jayanti", "date": date(2025, 11, 5), "type": "religious"},
        {"name": "Christmas", "date": date(2025, 12, 25), "type": "religious"},
        {"name": "New Year", "date": date(2026, 1, 1), "type": "national"},
        {"name": "Pongal", "date": date(2026, 1, 14), "type": "festival"},
        {"name": "Maha Shivaratri", "date": date(2026, 2, 17), "type": "religious"},
    ]
    
    holidays = []
    for hol_data in holidays_data:
        holiday = Holiday(
            name=hol_data["name"],
            description=f"National holiday - {hol_data['name']}",
            start_date=hol_data["date"],
            end_date=hol_data["date"],
            is_mandatory=True,
            holiday_type=hol_data["type"],
            created_by=users[0].id
        )
        holidays.append(holiday)
    
    session.add_all(holidays)
    session.commit()
    print(f"Created {len(holidays)} holidays")

def seed_goals(session, users):
    """Create 15 goals"""
    print("\nCreating goals...")
    
    goals_data = [
        {"title": "Complete React Advanced Course", "desc": "Master advanced React patterns and hooks", "cat": "learning", "status": GoalStatus.IN_PROGRESS, "progress": 60},
        {"title": "Reduce API Response Time", "desc": "Optimize backend APIs to reduce response time by 30%", "cat": "performance", "status": GoalStatus.IN_PROGRESS, "progress": 45},
        {"title": "Lead Code Review Sessions", "desc": "Conduct weekly code review sessions for team", "cat": "leadership", "status": GoalStatus.COMPLETED, "progress": 100},
        {"title": "Learn Kubernetes", "desc": "Complete Kubernetes certification course", "cat": "learning", "status": GoalStatus.NOT_STARTED, "progress": 0},
        {"title": "Improve Test Coverage", "desc": "Increase unit test coverage to 85%", "cat": "performance", "status": GoalStatus.IN_PROGRESS, "progress": 70},
        {"title": "Mentor Junior Developers", "desc": "Mentor 2 junior developers on best practices", "cat": "leadership", "status": GoalStatus.IN_PROGRESS, "progress": 50},
        {"title": "Complete AWS Certification", "desc": "Get AWS Solutions Architect certification", "cat": "learning", "status": GoalStatus.IN_PROGRESS, "progress": 30},
        {"title": "Refactor Legacy Code", "desc": "Refactor payment module using modern patterns", "cat": "performance", "status": GoalStatus.NOT_STARTED, "progress": 0},
        {"title": "Present at Tech Talk", "desc": "Give presentation on microservices architecture", "cat": "leadership", "status": GoalStatus.COMPLETED, "progress": 100},
        {"title": "Learn TypeScript", "desc": "Master TypeScript and apply to existing projects", "cat": "learning", "status": GoalStatus.IN_PROGRESS, "progress": 80},
        {"title": "Improve Database Performance", "desc": "Optimize slow queries and indexing", "cat": "performance", "status": GoalStatus.IN_PROGRESS, "progress": 40},
        {"title": "Build Design System", "desc": "Create comprehensive component library", "cat": "project", "status": GoalStatus.IN_PROGRESS, "progress": 55},
        {"title": "Security Audit", "desc": "Complete security audit of all services", "cat": "performance", "status": GoalStatus.NOT_STARTED, "progress": 0},
        {"title": "Mobile App Launch", "desc": "Launch mobile app version 2.0", "cat": "project", "status": GoalStatus.IN_PROGRESS, "progress": 65},
        {"title": "Documentation Improvement", "desc": "Update and improve technical documentation", "cat": "performance", "status": GoalStatus.IN_PROGRESS, "progress": 35},
    ]
    
    goals = []
    for i, goal_data in enumerate(goals_data):
        employee = users[5 + (i % 10)]
        start = date.today() - timedelta(days=random.randint(30, 90))
        target = date.today() + timedelta(days=random.randint(30, 180))
        
        goal = Goal(
            employee_id=employee.id,
            title=goal_data["title"],
            description=goal_data["desc"],
            category=goal_data["cat"],
            start_date=start,
            target_date=target,
            completion_date=datetime.now().date() if goal_data["status"] == GoalStatus.COMPLETED else None,
            status=goal_data["status"],
            progress_percentage=goal_data["progress"],
            assigned_by=employee.manager_id
        )
        goals.append(goal)
    
    session.add_all(goals)
    session.commit()
    
    # Add 30 checkpoints (2 per goal for first 15 goals)
    checkpoints = []
    for i, goal in enumerate(goals):
        for j in range(2):
            checkpoint = GoalCheckpoint(
                goal_id=goal.id,
                title=f"Milestone {j+1}",
                description=f"Complete phase {j+1} of {goal.title}",
                sequence_number=j+1,
                is_completed=j == 0 and goal.progress_percentage > 50,
                completed_date=datetime.now() - timedelta(days=random.randint(5, 20)) if j == 0 and goal.progress_percentage > 50 else None
            )
            checkpoints.append(checkpoint)
    
    session.add_all(checkpoints)
    session.commit()
    print(f"Created {len(goals)} goals with {len(checkpoints)} checkpoints")

def seed_skill_modules(session):
    """Create 15 skill modules"""
    print("\nCreating skill modules...")
    
    modules_data = [
        {"name": "Python Advanced Programming", "desc": "Deep dive into Python advanced concepts", "cat": "Programming", "hours": 40, "level": "advanced"},
        {"name": "React Fundamentals", "desc": "Learn React from scratch", "cat": "Frontend", "hours": 30, "level": "beginner"},
        {"name": "Docker & Kubernetes", "desc": "Container orchestration mastery", "cat": "DevOps", "hours": 35, "level": "intermediate"},
        {"name": "Machine Learning Basics", "desc": "Introduction to ML algorithms", "cat": "Data Science", "hours": 50, "level": "beginner"},
        {"name": "AWS Cloud Practitioner", "desc": "AWS fundamentals and services", "cat": "Cloud", "hours": 25, "level": "beginner"},
        {"name": "System Design", "desc": "Design scalable distributed systems", "cat": "Architecture", "hours": 45, "level": "advanced"},
        {"name": "TypeScript Mastery", "desc": "Complete TypeScript guide", "cat": "Programming", "hours": 20, "level": "intermediate"},
        {"name": "UI/UX Design Principles", "desc": "Modern design thinking", "cat": "Design", "hours": 30, "level": "beginner"},
        {"name": "Database Optimization", "desc": "SQL and NoSQL performance tuning", "cat": "Database", "hours": 35, "level": "advanced"},
        {"name": "API Design Best Practices", "desc": "RESTful API design patterns", "cat": "Backend", "hours": 25, "level": "intermediate"},
        {"name": "Git & Version Control", "desc": "Master Git workflows", "cat": "Tools", "hours": 15, "level": "beginner"},
        {"name": "Microservices Architecture", "desc": "Build microservices-based systems", "cat": "Architecture", "hours": 40, "level": "advanced"},
        {"name": "Agile & Scrum", "desc": "Agile methodologies and Scrum framework", "cat": "Management", "hours": 20, "level": "beginner"},
        {"name": "Cybersecurity Fundamentals", "desc": "Security best practices for developers", "cat": "Security", "hours": 30, "level": "intermediate"},
        {"name": "Data Structures & Algorithms", "desc": "Essential DSA for interviews", "cat": "Programming", "hours": 60, "level": "intermediate"},
    ]
    
    modules = []
    for mod_data in modules_data:
        module = SkillModule(
            name=mod_data["name"],
            description=mod_data["desc"],
            category=mod_data["cat"],
            module_link=f"https://learning.company.com/{mod_data['name'].lower().replace(' ', '-')}",
            duration_hours=mod_data["hours"],
            difficulty_level=mod_data["level"],
            skill_areas=mod_data["cat"]
        )
        modules.append(module)
    
    session.add_all(modules)
    session.commit()
    print(f"Created {len(modules)} skill modules")
    return modules

def seed_skill_enrollments(session, modules, users):
    """Create 15 skill enrollments"""
    print("\nCreating skill enrollments...")
    
    statuses = [ModuleStatus.COMPLETED, ModuleStatus.PENDING, ModuleStatus.NOT_STARTED]
    
    enrollments = []
    for i in range(15):
        employee = users[5 + (i % 10)]
        module = modules[i]
        status = random.choice(statuses)
        
        enrolled = date.today() - timedelta(days=random.randint(10, 90))
        progress = 0 if status == ModuleStatus.NOT_STARTED else (100 if status == ModuleStatus.COMPLETED else random.randint(20, 80))
        
        enrollment = SkillModuleEnrollment(
            employee_id=employee.id,
            module_id=module.id,
            status=status,
            progress_percentage=progress,
            enrolled_date=enrolled,
            started_date=enrolled + timedelta(days=2) if status != ModuleStatus.NOT_STARTED else None,
            completed_date=enrolled + timedelta(days=random.randint(20, 60)) if status == ModuleStatus.COMPLETED else None,
            target_completion_date=enrolled + timedelta(days=90),
            score=random.uniform(75, 95) if status == ModuleStatus.COMPLETED else None
        )
        enrollments.append(enrollment)
    
    session.add_all(enrollments)
    session.commit()
    print(f"Created {len(enrollments)} skill enrollments")

def seed_skill_developments(session, users):
    """Create 15 skill development records"""
    print("\nCreating skill development records...")
    
    developments = []
    categories = ["Technical", "Leadership", "Communication", "Management", "Design"]
    
    for i in range(15):
        employee = users[5 + (i % 10)]
        progress = random.randint(0, 100)
        enrolled = date.today() - timedelta(days=random.randint(30, 120))
        
        dev = SkillDevelopment(
            employee_id=employee.id,
            module_name=f"Professional Development Track {i+1}",
            description=f"Comprehensive skill development program for {categories[i % 5]}",
            category=categories[i % 5],
            skill_areas=f"{categories[i % 5]}, Problem Solving, Collaboration",
            total_modules=random.randint(3, 8),
            completed_modules=int((progress / 100) * random.randint(3, 8)),
            progress_percentage=progress,
            enrolled_date=enrolled,
            target_completion_date=enrolled + timedelta(days=180),
            completion_date=enrolled + timedelta(days=random.randint(90, 150)) if progress == 100 else None,
            is_certified=progress == 100
        )
        developments.append(dev)
    
    session.add_all(developments)
    session.commit()
    print(f"Created {len(developments)} skill development records")

def seed_policies(session, users):
    """Create 15 policies"""
    print("\nCreating policies...")
    
    policies_data = [
        {"title": "Work From Home Policy", "desc": "Remote work guidelines", "content": "Employees can work from home up to 2 days per week...", "cat": "HR"},
        {"title": "Leave Policy", "desc": "Annual and sick leave policy", "content": "All employees entitled to 15 days annual leave...", "cat": "HR"},
        {"title": "Code of Conduct", "desc": "Professional behavior standards", "content": "Expected behavior and ethics guidelines...", "cat": "HR"},
        {"title": "Information Security Policy", "desc": "Data protection guidelines", "content": "Secure handling of company and customer data...", "cat": "IT"},
        {"title": "Expense Reimbursement", "desc": "Business expense claims", "content": "Policy for claiming business-related expenses...", "cat": "Finance"},
        {"title": "Dress Code Policy", "desc": "Workplace attire guidelines", "content": "Business casual dress code for office days...", "cat": "HR"},
        {"title": "Email and Communication", "desc": "Professional communication standards", "content": "Guidelines for email and Slack usage...", "cat": "IT"},
        {"title": "Performance Management", "desc": "Performance review process", "content": "Quarterly performance review and feedback cycle...", "cat": "HR"},
        {"title": "Anti-Harassment Policy", "desc": "Workplace harassment prevention", "content": "Zero tolerance policy for harassment...", "cat": "HR"},
        {"title": "Device Usage Policy", "desc": "Company device guidelines", "content": "Proper usage of company-provided laptops and phones...", "cat": "IT"},
        {"title": "Social Media Policy", "desc": "Social media usage guidelines", "content": "Guidelines for representing company on social media...", "cat": "Marketing"},
        {"title": "Confidentiality Agreement", "desc": "Trade secrets and NDA", "content": "Protection of confidential company information...", "cat": "Legal"},
        {"title": "Health and Safety", "desc": "Workplace safety guidelines", "content": "Safety protocols and emergency procedures...", "cat": "Operations"},
        {"title": "Learning and Development", "desc": "Professional growth support", "content": "Company support for learning and certifications...", "cat": "HR"},
        {"title": "Travel Policy", "desc": "Business travel guidelines", "content": "Booking and expense guidelines for business travel...", "cat": "Finance"},
    ]
    
    policies = []
    for i, pol_data in enumerate(policies_data):
        policy = Policy(
            title=pol_data["title"],
            description=pol_data["desc"],
            content=pol_data["content"],
            category=pol_data["cat"],
            version=f"{random.randint(1,3)}.{random.randint(0,5)}",
            effective_date=date.today() - timedelta(days=random.randint(30, 365)),
            review_date=date.today() + timedelta(days=random.randint(180, 365)),
            created_by=users[0].id if i % 2 == 0 else users[1].id
        )
        policies.append(policy)
    
    session.add_all(policies)
    session.commit()
    print(f"Created {len(policies)} policies")

def seed_payslips(session, users):
    """Create 15 payslips"""
    print("\nCreating payslips...")
    
    payslips = []
    # Create payslips for employees
    for i, user in enumerate(users[5:15]):  # 10 employees
        for month_offset in range(0, 2):  # Last 2 months, but we'll create 15 total
            pay_period_start = date(2024, 10 - month_offset, 1)
            pay_period_end = date(2024, 10 - month_offset, 30)
            pay_date = date(2024, 11 - month_offset, 1)
            
            basic = user.salary * 0.6
            allowances = user.salary * 0.3
            bonus = user.salary * 0.1 if month_offset == 0 else 0
            gross = basic + allowances + bonus
            
            tax = gross * 0.2
            pf = gross * 0.08
            insurance = 500
            total_ded = tax + pf + insurance
            net = gross - total_ded
            
            payslip = Payslip(
                employee_id=user.id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end,
                pay_date=pay_date,
                basic_salary=basic,
                allowances=allowances,
                overtime_pay=0,
                bonus=bonus,
                gross_salary=gross,
                tax_deduction=tax,
                pf_deduction=pf,
                insurance_deduction=insurance,
                other_deductions=0,
                total_deductions=total_ded,
                net_salary=net,
                generated_date=datetime(2024, 11 - month_offset, 1)
            )
            payslips.append(payslip)
            
            if len(payslips) >= 15:
                break
        
        if len(payslips) >= 15:
            break
    
    session.add_all(payslips[:15])
    session.commit()
    print(f"Created {len(payslips[:15])} payslips")

def seed_requests(session, users):
    """Create 15 requests"""
    print("\nCreating requests...")
    
    request_types = [RequestType.WFH, RequestType.EQUIPMENT, RequestType.TRAVEL, RequestType.LEAVE, RequestType.OTHER]
    subjects = [
        "WFH Request - Monday", "New Laptop Request", "Client Visit - Delhi", "Sick Leave Extension",
        "Conference Attendance", "Monitor Request", "WFH Request - Week", "Ergonomic Chair",
        "Training Program - Mumbai", "Certification Reimbursement", "WFH Internet Allowance",
        "Mobile Phone Upgrade", "Team Offsite - Goa", "Parking Spot Request", "Software License"
    ]
    
    requests = []
    for i in range(15):
        employee = users[5 + (i % 10)]
        req_type = request_types[i % 5]
        status = random.choice([LeaveStatus.PENDING, LeaveStatus.APPROVED, LeaveStatus.APPROVED, LeaveStatus.REJECTED])
        
        request = Request(
            employee_id=employee.id,
            request_type=req_type,
            subject=subjects[i],
            description=f"Requesting {subjects[i].lower()} for work purposes",
            request_date=date.today() + timedelta(days=random.randint(0, 10)) if req_type in [RequestType.WFH, RequestType.TRAVEL] else None,
            status=status,
            approved_by=employee.manager_id if status != LeaveStatus.PENDING else None,
            approved_date=datetime.now() - timedelta(days=random.randint(1, 5)) if status != LeaveStatus.PENDING else None,
            rejection_reason="Budget constraints" if status == LeaveStatus.REJECTED else None,
            submitted_date=datetime.now() - timedelta(days=random.randint(1, 10))
        )
        requests.append(request)
    
    session.add_all(requests)
    session.commit()
    print(f"Created {len(requests)} requests")

def seed_feedback(session, users):
    """Create 15 feedback entries"""
    print("\nCreating feedback...")
    
    feedback_subjects = [
        "Excellent Performance in Q4", "Great Teamwork", "Code Quality Improvement Needed",
        "Outstanding Project Delivery", "Communication Skills", "Leadership Qualities",
        "Technical Skills Assessment", "Meeting Deadlines", "Collaborative Spirit",
        "Problem-Solving Approach", "Initiative and Ownership", "Attention to Detail",
        "Customer Interaction", "Documentation Quality", "Mentoring New Members"
    ]
    
    feedbacks = []
    for i in range(15):
        employee = users[5 + (i % 10)]
        manager = users[2] if i % 3 == 0 else users[3] if i % 3 == 1 else users[4]
        rating = random.uniform(3.5, 5.0)
        
        positive = rating >= 4.0
        description = f"{'Great work on' if positive else 'Needs improvement in'} {feedback_subjects[i].lower()}. {'Keep up the excellent work!' if positive else 'Looking forward to seeing progress.'}"
        
        feedback = Feedback(
            employee_id=employee.id,
            given_by=manager.id,
            subject=feedback_subjects[i],
            description=description,
            feedback_type="performance" if i % 3 == 0 else "project" if i % 3 == 1 else "behavioral",
            rating=rating,
            given_on=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        feedbacks.append(feedback)
    
    session.add_all(feedbacks)
    session.commit()
    print(f"Created {len(feedbacks)} feedback entries")

def seed_notifications(session, users):
    """Create 15 notifications"""
    print("\nCreating notifications...")
    
    notifications_data = [
        {"title": "Leave Approved", "msg": "Your leave request has been approved", "type": "success"},
        {"title": "New Announcement", "msg": "Check out the new company policy update", "type": "info"},
        {"title": "Goal Updated", "msg": "Your manager updated your goal progress", "type": "info"},
        {"title": "Payslip Generated", "msg": "Your October payslip is now available", "type": "info"},
        {"title": "Performance Review", "msg": "Your Q3 performance review is ready", "type": "info"},
        {"title": "Training Reminder", "msg": "Complete your mandatory security training", "type": "warning"},
        {"title": "Leave Request", "msg": "New leave request from team member needs approval", "type": "info"},
        {"title": "Birthday Wish", "msg": "Happy Birthday! Check your rewards", "type": "celebration"},
        {"title": "System Maintenance", "msg": "Scheduled maintenance on Saturday", "type": "warning"},
        {"title": "Certificate Earned", "msg": "Congratulations on completing AWS course!", "type": "success"},
        {"title": "Meeting Reminder", "msg": "Team standup in 15 minutes", "type": "reminder"},
        {"title": "Document Pending", "msg": "Please upload your updated PAN card", "type": "warning"},
        {"title": "Referral Bonus", "msg": "You've earned ₹25,000 referral bonus!", "type": "success"},
        {"title": "Project Milestone", "msg": "Team achieved 90% completion on Project Alpha", "type": "celebration"},
        {"title": "Policy Update", "msg": "New WFH policy effective from next month", "type": "info"},
    ]
    
    notifications = []
    for i, notif_data in enumerate(notifications_data):
        user = users[5 + (i % 10)]
        is_read = i % 3 != 0  # 66% read
        
        notification = Notification(
            user_id=user.id,
            title=notif_data["title"],
            message=notif_data["msg"],
            notification_type=notif_data["type"],
            is_read=is_read,
            created_at=datetime.now() - timedelta(hours=random.randint(1, 72)),
            read_at=datetime.now() - timedelta(hours=random.randint(0, 24)) if is_read else None
        )
        notifications.append(notification)
    
    session.add_all(notifications)
    session.commit()
    print(f"Created {len(notifications)} notifications")

def seed_performance_reports(session, users):
    """Create 15 performance reports"""
    print("\nCreating performance reports...")
    
    reports = []
    for i in range(15):
        employee = users[5 + (i % 10)]
        
        # Q3 2024 reports
        report = PerformanceReport(
            employee_id=employee.id,
            report_period_start=date(2024, 7, 1),
            report_period_end=date(2024, 9, 30),
            report_type="quarterly",
            overall_rating=random.uniform(3.5, 5.0),
            goals_completion_rate=random.uniform(70, 100),
            attendance_rate=random.uniform(85, 100),
            training_completion_rate=random.uniform(60, 100),
            manager_feedback=f"Solid performance in Q3. {'Exceeded expectations in key areas.' if i % 3 == 0 else 'Met most objectives successfully.' if i % 3 == 1 else 'Good progress with room for improvement.'}",
            self_assessment="Achieved major milestones and learned new technologies",
            development_areas="Focus on mentoring and leadership skills",
            achievements="Successfully delivered 3 major features, improved code quality",
            created_by=employee.manager_id,
            created_at=datetime.now() - timedelta(days=random.randint(10, 30))
        )
        reports.append(report)
    
    session.add_all(reports)
    session.commit()
    print(f"Created {len(reports)} performance reports")

def seed_resume_screening_results(session, applications):
    """Create 15 resume screening results"""
    print("\nCreating resume screening results...")
    
    results = []
    for i, app in enumerate(applications[:15]):
        if app.status != ApplicationStatus.PENDING:
            result = ResumeScreeningResult(
                application_id=app.id,
                resume_path=f"/uploads/resumes/resume_{app.id}.pdf",
                screening_model_version="v2.1",
                overall_score=app.screening_score or random.uniform(60, 95),
                technical_skills_score=random.uniform(60, 95),
                experience_score=random.uniform(65, 90),
                education_score=random.uniform(70, 95),
                matched_keywords='["Python", "React", "SQL", "Docker", "AWS"]',
                missing_keywords='["Kubernetes", "GraphQL"]',
                strengths="Strong technical background, relevant experience",
                weaknesses="Limited leadership experience",
                recommendation="recommend" if app.screening_score and app.screening_score > 80 else "maybe",
                screened_date=app.reviewed_date or datetime.now()
            )
            results.append(result)
    
    session.add_all(results)
    session.commit()
    print(f"Created {len(results)} resume screening results")

def main():
    """Main comprehensive seeding function"""
    print("="*70)
    print("Starting COMPREHENSIVE database seeding with 15 rows per table...")
    print("="*70)
    
    session = SessionLocal()
    
    try:
        # Clear existing data
        clear_database(session)
        
        # Seed all tables with 15 rows each
        departments = seed_departments(session)
        teams = seed_teams(session, departments)
        users = seed_users(session, departments, teams)
        jobs = seed_job_listings(session, departments, users)
        applications = seed_applications(session, jobs, users)
        seed_announcements(session, users)
        seed_attendance(session, users)
        seed_leave_requests(session, users)
        seed_holidays(session, users)
        seed_goals(session, users)
        modules = seed_skill_modules(session)
        seed_skill_enrollments(session, modules, users)
        seed_skill_developments(session, users)
        seed_policies(session, users)
        seed_payslips(session, users)
        seed_requests(session, users)
        seed_feedback(session, users)
        seed_notifications(session, users)
        seed_performance_reports(session, users)
        seed_resume_screening_results(session, applications)
        
        print("\n" + "="*70)
        print("✅ Database seeded successfully with comprehensive realistic data!")
        print("="*70)
        print("\n📊 Summary:")
        print("  ✓ 15 Departments")
        print("  ✓ 15 Teams")
        print("  ✓ 15 Users (HR, Managers, Employees)")
        print("  ✓ 15 Job Listings")
        print("  ✓ 15 Applications")
        print("  ✓ 15 Announcements")
        print("  ✓ 150+ Attendance Records")
        print("  ✓ 15 Leave Requests")
        print("  ✓ 15 Holidays")
        print("  ✓ 15 Goals with 30 Checkpoints")
        print("  ✓ 15 Skill Modules")
        print("  ✓ 15 Skill Enrollments")
        print("  ✓ 15 Skill Development Records")
        print("  ✓ 15 Policies")
        print("  ✓ 15 Payslips")
        print("  ✓ 15 Requests")
        print("  ✓ 15 Feedback Entries")
        print("  ✓ 15 Notifications")
        print("  ✓ 15 Performance Reports")
        print("  ✓ 15 Resume Screening Results")
        print("\n🔑 Test Credentials:")
        print("  HR:       sarah.johnson@company.com / pass123")
        print("  Manager:  michael.chen@company.com / pass123")
        print("  Employee: john.anderson@company.com / pass123")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ [ERROR] Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()

