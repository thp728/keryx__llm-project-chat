from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables.
    """

    # Project settings
    PROJECT_NAME: str = "Keryx Backend API"
    API_VER_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str

    # LLM and Helicone settings
    GEMINI_API_KEY: str
    HELICONE_API_KEY: str | None = (  # Use | None for union type hint in Python 3.10+
        None  # Helicone is optional, set to None if not always required
    )

    # JWT Authentication settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings():
    """
    Returns a cached instance of the Settings class.
    This ensures settings are loaded only once.
    """
    return Settings()


# Create a global settings instance for convenient access
settings = get_settings()
