
"""
Configuration and logging setup for HR Employee Search API.
Reads environment variables (supports .env) and sets up logging.
"""
import logging
import os
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional, .env support if available

# Logging setup
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("hr_search_api")

class Settings:
    """
    Application settings loaded from environment variables.
    """
    DB_SHARDS: int = int(os.getenv("DB_SHARDS", 4))
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", 100))  # requests per minute per org
    COLUMN_CONFIG_PATH: str = os.getenv("COLUMN_CONFIG_PATH", "app/core/column_config.json")
    # PostgreSQL config
    DB_HOST: str = os.getenv("POSTGRES_HOST", "db")
    DB_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    DB_NAME: str = os.getenv("POSTGRES_DB", "hrdb")
    DB_USER: str = os.getenv("POSTGRES_USER", "hruser")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "hrpass")

settings = Settings()
