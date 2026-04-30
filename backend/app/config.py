"""
Configuration management for FairLens backend.
Loads environment variables and provides centralized config.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_TITLE: str = "FairLens API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Google Cloud Configuration
    PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "fairlens-datasets")
    FIRESTORE_DATABASE: str = os.getenv("FIRESTORE_DATABASE", "(default)")
    
    # Gemini AI Configuration
    GEMINI_MODEL: str = "gemini-1.5-pro"
    GEMINI_MAX_TOKENS: int = 1024
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = 100
    ALLOWED_FILE_EXTENSIONS: list = [".csv", ".xlsx", ".json"]
    
    # Fairness Thresholds
    FAIRNESS_THRESHOLD_RED: float = 0.40
    FAIRNESS_THRESHOLD_YELLOW: float = 0.70
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://fairlens.web.app",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()