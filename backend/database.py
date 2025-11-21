"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Use this in FastAPI route dependencies.
    
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def create_tables():
    """Create all database tables"""
    from models import Base as ModelsBase
    ModelsBase.metadata.create_all(bind=engine)
    print("[OK] Database tables created successfully!")

# Function to drop all tables (use with caution!)
def drop_tables():
    """Drop all database tables - USE WITH CAUTION!"""
    from models import Base as ModelsBase
    ModelsBase.metadata.drop_all(bind=engine)
    print("[OK] Database tables dropped!")

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()

