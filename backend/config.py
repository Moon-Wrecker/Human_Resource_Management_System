"""
Application Configuration
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "GenAI HRMS API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "dev-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./hr_system.db"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10

    @property
    def MAX_FILE_SIZE(self) -> int:
        """Convert MB to bytes"""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    # Allowed file extensions
    ALLOWED_DOCUMENT_EXTENSIONS: set = {".pdf", ".doc", ".docx"}
    ALLOWED_IMAGE_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif"}

    # Logging
    LOG_LEVEL: str = "INFO"

    # AI Services (Google Gemini)
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    GEMINI_TEMPERATURE: float = 0.2

    # Policy RAG Configuration
    POLICY_RAG_CHUNK_SIZE: int = 1000
    POLICY_RAG_CHUNK_OVERLAP: int = 200
    POLICY_RAG_RETRIEVAL_K: int = 3
    POLICY_RAG_INDEX_DIR: str = "ai_data/policy_index"

    # Resume Screener Configuration
    RESUME_SCREENER_MAX_WORKERS: int = 4
    RESUME_SCREENER_STORAGE_DIR: str = "ai_data/resume_analysis"

    # Job Description Generator Configuration
    JD_GENERATOR_ENABLED: bool = True

    # Email (Optional)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@company.com"

    # Redis (Optional)
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()


# Create required directories
def create_upload_directories():
    """Create upload and AI data directories if they don't exist"""
    directories = [
        settings.UPLOAD_DIR,
        os.path.join(settings.UPLOAD_DIR, "resumes"),
        os.path.join(settings.UPLOAD_DIR, "documents"),
        os.path.join(settings.UPLOAD_DIR, "profiles"),
        os.path.join(settings.UPLOAD_DIR, "policies"),
        os.path.join(settings.UPLOAD_DIR, "payslips"),
        os.path.join(settings.UPLOAD_DIR, "certificates"),
        # AI data directories
        "ai_data",
        settings.POLICY_RAG_INDEX_DIR,
        settings.RESUME_SCREENER_STORAGE_DIR,
        os.path.join("ai_data", "temp"),
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print(f"[OK] Upload directories created in: {settings.UPLOAD_DIR}")
    print(f"[OK] AI data directories created")


if __name__ == "__main__":
    create_upload_directories()
    print("\nConfiguration loaded successfully!")
    print(f"App Name: {settings.APP_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Database: {settings.DATABASE_URL}")
    print(f"CORS Origins: {settings.CORS_ORIGINS}")
