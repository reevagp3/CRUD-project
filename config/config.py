"""Configuration management for the Flask application."""
import os
import logging
import secrets
from dotenv import load_dotenv

# Load .env for local development.  On Render, env vars are injected natively.
load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """Base configuration shared across all environments."""

    # ------------------------------------------------------------------ #
    # Flask core
    # ------------------------------------------------------------------ #
    # Generate a random key as a safe in-memory fallback for local dev.
    # In production this MUST be overridden by the SECRET_KEY env var.
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_hex(32))

    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    DEBUG: bool = False
    TESTING: bool = False

    # ------------------------------------------------------------------ #
    # Database — Supabase PostgreSQL
    # ------------------------------------------------------------------ #
    DATABASE_URL: str | None = os.getenv("SUPABASE_DB_URL")

    # ------------------------------------------------------------------ #
    # Server
    # ------------------------------------------------------------------ #
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))

    # ------------------------------------------------------------------ #
    # Logging
    # ------------------------------------------------------------------ #
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # ------------------------------------------------------------------ #
    # JSON / response
    # ------------------------------------------------------------------ #
    JSON_SORT_KEYS: bool = False

    @classmethod
    def validate(cls) -> None:
        """Raise if required config values are missing."""
        if not cls.DATABASE_URL:
            raise ValueError(
                "SUPABASE_DB_URL is not set. "
                "Add it to your .env file (local) or Render environment variables (production)."
            )


class DevelopmentConfig(Config):
    """Development — debug on, relaxed secret key check."""
    DEBUG = True
    TESTING = False

    @classmethod
    def validate(cls) -> None:
        super().validate()
        if os.getenv("SECRET_KEY") is None:
            logger.info(
                "SECRET_KEY not set — using a random per-process key for development."
            )
        logger.info("Development configuration loaded.")


class ProductionConfig(Config):
    """Production — debug off, strict secret key enforcement."""
    DEBUG = False
    TESTING = False

    @classmethod
    def validate(cls) -> None:
        super().validate()
        if not os.getenv("SECRET_KEY"):
            raise ValueError(
                "SECRET_KEY must be set in production. "
                "Add it as an environment variable in Render."
            )
        logger.info("Production configuration loaded.")


class TestingConfig(Config):
    """Testing — in-memory overrides, no DB required."""
    DEBUG = True
    TESTING = True

    @classmethod
    def validate(cls) -> None:
        logger.info("Testing configuration loaded.")


# ------------------------------------------------------------------ #
# Factory
# ------------------------------------------------------------------ #
_ENV_MAP: dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config() -> type[Config]:
    """Return and validate the config class for the current FLASK_ENV."""
    env = os.getenv("FLASK_ENV", "development").lower()
    config_class = _ENV_MAP.get(env, DevelopmentConfig)
    config_class.validate()
    return config_class
