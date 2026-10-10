"""
Telegram Media Storage Bot v3.0.0
Least Recently Used (LRU) Cache with TTL Expiry

Provides a memory-efficient ordered cache with automatic eviction
of least recently used entries and periodic cleanup of expired
items based on a configurable Time-To-Live.

FIXES v3.0.1:
- Added key validation and length limits
- Added cache statistics for monitoring
"""

import logging
import time
from collections import OrderedDict
from typing import Any, Dict, Optional

from config import CACHE_TTL_HOURS

logger = logging.getLogger(__name__)

# Maximum key length to prevent memory abuse
MAX_KEY_LENGTH = 256


class LRUCache:
    """
    Least Recently Used cache with Time-To-Live support.

    Entries are evicted when:
    - The cache exceeds its maximum capacity (oldest first).
    - The entry's TTL has expired (checked periodically).

    Attributes:
        max_size: Maximum number of entries allowed.
        ttl_seconds: Entry lifespan in seconds.
        cleanup_interval: Interval between expiry checks (seconds).
    """

    def __init__(self, max_size: int = 50000):
        self._cache: OrderedDict = OrderedDict()
        self.max_size: int = max_size
        self._last_cleanup: float = time.time()
        self.ttl_seconds: int = CACHE_TTL_HOURS * 3600
        self.cleanup_interval: int = 300  # 5 minutes
        
        # Cache statistics for monitoring
        self.stats: Dict[str, int] = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "expirations": 0,
            "invalid_keys": 0,
        }

    def _validate_key(self, key: str) -> str:
        """
        Validate and sanitize cache key.
        
        Args:
            key: The cache key to validate.
            
        Returns:
            Sanitized key string.
            
        Raises:
            ValueError: If key is empty or not a string.
        """
        if not isinstance(key, str):
            self.stats["invalid_keys"] += 1
            raise ValueError(f"Cache key must be a string, got {type(key).__name__}")
        
        if len(key) == 0:
            self.stats["invalid_keys"] += 1
            raise ValueError("Cache key must be a non-empty string")
        
        # Truncate long keys with warning
        if len(key) > MAX_KEY_LENGTH:
            logger.warning(
                "Cache key too long (%s chars), truncating: %s...",
                len(key), key[:50]
            )
            self.stats["invalid_keys"] += 1
            key = key[:MAX_KEY_LENGTH]
        
        return key

    def __contains__(self, key: str) -> bool:
        """
        Check if a key exists (promotes to most recently used).

        Args:
            key: The cache key.

        Returns:
            True if present and not expired.
        """
        self._cleanup_if_needed()
        try:
            key = self._validate_key(key)
        except ValueError:
            return False
            
        if key in self._cache:
            self._cache.move_to_end(key)
            self.stats["hits"] += 1
            return True
        
        self.stats["misses"] += 1
        return False

    def add(self, key: str, value: Optional[Dict[str, Any]] = None) -> None:
        """
        Add or update a cache entry.

        Args:
            key: The cache key.
            value: Optional data payload.
            
        Raises:
            ValueError: If key is invalid.
        """
        self._cleanup_if_needed()
        key = self._validate_key(key)

        if key in self._cache:
            self._cache.move_to_end(key)

        self._cache[key] = {
            "data": value or {},
            "timestamp": time.time(),
        }

        # Evict oldest entries if over capacity
        while len(self._cache) > self.max_size:
            evicted_key, _ = self._cache.popitem(last=False)
            self.stats["evictions"] += 1
            logger.debug(
                "Cache evicted key (capacity %s exceeded): %s...",
                self.max_size, evicted_key[:50]
            )

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a cache entry (promotes to most recently used).

        Args:
            key: The cache key.

        Returns:
            The stored data dict, or None.
        """
        self._cleanup_if_needed()
        try:
            key = self._validate_key(key)
        except ValueError:
            return None
            
        if key in self._cache:
            self._cache.move_to_end(key)
            self.stats["hits"] += 1
            return self._cache[key]["data"]
        
        self.stats["misses"] += 1
        return None

    def remove(self, key: str) -> None:
        """
        Remove a specific key from the cache.

        Args:
            key: The cache key.
        """
        try:
            key = self._validate_key(key)
        except ValueError:
            return
            
        if self._cache.pop(key, None) is not None:
            logger.debug("Cache key removed: %s...", key[:50])

    def _cleanup_if_needed(self) -> None:
        """Periodically remove entries that have exceeded their TTL."""
        now = time.time()
        if now - self._last_cleanup > self.cleanup_interval:
            expired = [
                key for key, val in self._cache.items()
                if now - val["timestamp"] > self.ttl_seconds
            ]
            for key in expired:
                del self._cache[key]
            self._last_cleanup = now
            if expired:
                self.stats["expirations"] += len(expired)
                logger.info("Cache cleanup: %s expired items removed", len(expired))

    def clear(self) -> None:
        """Remove all entries."""
        self._cache.clear()
        logger.info("Cache fully cleared")

    @property
    def size(self) -> int:
        """Current number of entries."""
        return len(self._cache)
    
    def get_stats(self) -> Dict[str, int]:
        """Return cache statistics for monitoring."""
        return {
            **self.stats,
            "current_size": len(self._cache),
            "max_size": self.max_size,
            "ttl_hours": CACHE_TTL_HOURS,
        }