from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "VisionGPT API"
    DEBUG: bool = True

    HF_TOKEN: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache
def get_settings():
    return Settings()