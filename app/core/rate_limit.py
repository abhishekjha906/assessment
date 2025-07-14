
"""
Naive in-memory rate limiter for per-organization request limiting.
Thread-safe, resets every minute window. No persistence or distributed support.
"""
import time
from threading import Lock
from app.core.config import logger, settings
from typing import Dict

class RateLimiter:
    def __init__(self, limit: int = settings.RATE_LIMIT) -> None:
        """
        Initialize the rate limiter.
        :param limit: Max requests per org per minute.
        """
        self.limit = limit
        self.requests: Dict[str, Dict[int, int]] = {}
        self.lock = Lock()

    def is_allowed(self, org_id: str) -> bool:
        """
        Check if a request is allowed for the given org in the current minute window.
        :param org_id: Organization ID
        :return: True if allowed, False if rate limit exceeded
        """
        if not org_id:
            logger.error("RateLimiter: org_id is required.")
            return False
        now = int(time.time())
        window = now // 60  # minute window
        with self.lock:
            org_data = self.requests.setdefault(org_id, {})
            count = org_data.get(window, 0)
            if count >= self.limit:
                logger.warning(f"Rate limit exceeded for org {org_id}")
                return False
            org_data[window] = count + 1
            self.requests[org_id] = org_data
        return True

# Singleton instance for global use
rate_limiter = RateLimiter()
