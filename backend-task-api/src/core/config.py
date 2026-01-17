from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Server settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    APP_ENV: str = "development"

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "info"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Return the database URL with asyncpg driver for async operations"""
        if "asyncpg" not in self.DATABASE_URL:
            # Replace postgresql:// with postgresql+asyncpg:// if not present
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        return self.DATABASE_URL


def get_settings():
    # Load environment variables from .env file when function is called
    from dotenv import load_dotenv
    
    # Determine the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to reach the backend directory
    backend_dir = os.path.dirname(os.path.dirname(current_dir))
    # Load the .env file from the backend directory
    dotenv_path = os.path.join(backend_dir, '.env')
    
    # Override system environment variables with .env file
    load_dotenv(dotenv_path=dotenv_path, override=True)
    
    return Settings()


# Create a function to get settings instead of instantiating at import time
settings = get_settings()