from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables.
    """

    # Database settings
    DATABASE_URL: str

    # LLM and Helicone settings
    GEMINI_API_KEY: str
    HELICONE_API_KEY: str = (
        None  # Helicone is optional, set to None if not always required
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings():
    """
    Returns a cached instance of the Settings class.
    This ensures settings are loaded only once.
    """
    return Settings()
