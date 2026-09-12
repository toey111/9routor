import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Faculty Personnel Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "mysql")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "3306")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "personnel_db")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "personnel_user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "personnel_pass123")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # If DATABASE_URL is provided (e.g., by Vercel/Supabase), use it directly
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            # SQLAlchemy 1.4+ requires postgresql:// instead of postgres://
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
            elif database_url.startswith("postgresql://"):
                database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
            return database_url
            
        return f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    # JWT Authentication
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretjwtkey_reru_it_2026_faculty_system")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # Uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/app/uploads")
    MAX_FILE_SIZE_MB: int = 10
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    class Config:
        case_sensitive = True

settings = Settings()
