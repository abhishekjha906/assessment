"""
Unit tests for RateLimiter (naive in-memory rate limiting).
Ensures correct behavior for allowed, blocked, and reset scenarios.
"""
import time
import pytest
from app.core.rate_limit import RateLimiter

ORG_ID = "org_test"

def test_rate_limit_allows_within_limit() -> None:
    """Should allow requests within the limit."""
    limiter = RateLimiter(limit=5)
    for _ in range(5):
        assert limiter.is_allowed(ORG_ID)

def test_rate_limit_blocks_over_limit() -> None:
    """Should block requests over the limit."""
    limiter = RateLimiter(limit=2)
    assert limiter.is_allowed(ORG_ID)
    assert limiter.is_allowed(ORG_ID)
    assert not limiter.is_allowed(ORG_ID)

def test_rate_limit_is_isolated_per_org() -> None:
    """Each org should have its own rate limit window."""
    limiter = RateLimiter(limit=1)
    assert limiter.is_allowed("org1")
    assert limiter.is_allowed("org2")
    assert not limiter.is_allowed("org1")
    assert not limiter.is_allowed("org2")

def test_rate_limit_resets_next_window() -> None:
    """Should reset after time window passes."""
    limiter = RateLimiter(limit=1)
    assert limiter.is_allowed(ORG_ID)
    time.sleep(61)  # Wait for next minute window
    assert limiter.is_allowed(ORG_ID)
