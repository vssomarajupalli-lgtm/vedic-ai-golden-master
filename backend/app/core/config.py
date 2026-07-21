from pydantic_settings import BaseSettings
from typing import List, Optional
import json


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vedic-AI Core API"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # CORS Origins - Comma separated list for production
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # External API Keys
    OPENAI_API_KEY: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text

    # Calibration Profile
    CALIBRATION_PROFILE: str = "v1.0_current"

    # Redis
    REDIS_URL: Optional[str] = None

    # Database (Postgres for auth/sessions)
    DATABASE_URL: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
