"""
Configuration settings for the Task Manager API
"""
import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "Task Manager API"
    APP_VERSION: str = "1.0.0"
    ENV: str = "development"  # development, staging, production
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/taskmanager"
    
    # CORS Configuration (comma-separated string)
    CORS_ORIGINS: str = "*"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENV.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENV.lower() == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
