"""
config.py
---------
Centralised configuration for the AI Resume Builder backend.
All environment variables and app-level settings are loaded here,
keeping the rest of the codebase free of raw os.getenv() calls.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file into the process environment
load_dotenv()


class Config:
    """Base configuration shared by all environments."""

    # ── Groq / LLM ────────────────────────────────────────────────────────────
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_MAX_TOKENS: int = 2048
    GROQ_TEMPERATURE: float = 0.7

    # ── Flask ──────────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # ── CORS ───────────────────────────────────────────────────────────────────
    # In production replace "*" with your actual frontend origin
    CORS_ORIGINS: list = ["*"]


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Map the FLASK_ENV string to the correct class
config_map: dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

# The config object that will be imported everywhere else
active_config: Config = config_map.get(
    os.getenv("FLASK_ENV", "development"), DevelopmentConfig
)
