from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "源流AI提示词工具 API"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    DEEPSEEK_API_KEY: str = ""
    DATABASE_URL: str = ""
    JWT_SECRET: str = "dev-secret-change-in-production"
    DAILY_FREE_QUOTA: int = 5

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
