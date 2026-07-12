from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vedic-AI Core API"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS Origins - Comma separated list for production (e.g., "http://localhost:3000,https://app.vedic-ai.com")
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # External API Keys (e.g. OpenAI for QuestionEngine narrative generation)
    OPENAI_API_KEY: str | None = None

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
