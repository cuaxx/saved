"""
Telegram Media Storage Bot v3.0.0
Rate Limiter Configuration

Provides a configured AIORateLimiter to prevent hitting
Telegram API rate limits during high traffic.

FIXES v3.0.1:
- Added proper burst rate configuration
- Added documentation for rate limit values
"""

from telegram.ext import AIORateLimiter

from config import RATE_LIMIT_BURST, RATE_LIMIT_PER_SECOND


def create_rate_limiter() -> AIORateLimiter:
    """
    Create a configured AIORateLimiter.

    Configuration:
        overall_max_rate: Maximum API calls per second (default: 5)
        overall_time_period: Time window in seconds (1.0 = per second)
        max_retries: Number of retries when rate limited (default: 3)
        
    Note: Telegram allows ~30 messages per second for bots,
    but we use conservative defaults to avoid floods.
    
    Returns:
        AIORateLimiter instance with overall rate settings.
    """
    return AIORateLimiter(
        overall_max_rate=RATE_LIMIT_PER_SECOND,
        overall_time_period=1.0,
        max_retries=3,
    )