
"""
Database connection provider for HR Employee Search API.
No business logic or models here. Use as dependency in services/APIs.
"""
import psycopg2
from app.core.config import settings, logger

def get_db_conn():
    """
    Create and return a new PostgreSQL database connection.
    Usage: Use as a dependency in services/APIs.
    """
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        logger.info("Database connection established.")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
