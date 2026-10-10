"""
Telegram Media Storage Bot v3.0.3
Fast Duplicate Filter (In-Memory Layer)

Provides sub-millisecond duplicate detection using dual LRU caches.
Cache entries are only added AFTER confirmation by deep check or
successful database insertion — never at check time.

CRITICAL FIX v3.0.1: Added per-user isolation to cache keys.
Previously cache keys were only file_unique_id without owner_id,
causing cross-user false positive duplicate detection.

FIXES v3.0.3:
- ✅ FIXED: clear_user_cache() now properly removes all entries
- ✅ FIXED: Cache cleanup for banned/deleted users works correctly
"""

import logging
from typing import Dict, Optional

from config import CACHE_MAX_SIZE
from .cache import LRUCache

logger = logging.getLogger(__name__)


class FastFilter:
    """
    Pre-database duplicate check using in-memory caches.

    Two caches are maintained:
    - unique_id_cache: Per-user exact file_unique_id matches.
    - signature_cache: Per-user metadata signature matches.

    The check() method is read-only. add_to_cache() must be called
    explicitly after deep check or DB confirmation.

    Cache keys include owner_id for proper per-user isolation
    (e.g., "123456:AbCdEf12345").
    """

    def __init__(self):
        self.unique_id_cache = LRUCache(max_size=CACHE_MAX_SIZE)
        self.signature_cache = LRUCache(max_size=CACHE_MAX_SIZE)
        self.stats: Dict[str, int] = {
            "checked": 0,
            "blocked": 0,
            "passed": 0,
            "cache_clears": 0,
            "total_entries_cleared": 0,
        }

    async def check(self, file_unique_id: str, owner_id: int,
                    file_signature: Optional[str] = None) -> bool:
        """
        Check caches for a known duplicate within user scope.
        Does NOT add to cache.

        Args:
            file_unique_id: Telegram unique file ID.
            owner_id: Owner's Telegram user ID (for per-user isolation).
            file_signature: Metadata signature (optional).

        Returns:
            True if found in cache (probable duplicate for this user).
        """
        self.stats["checked"] += 1

        # Build per-user cache keys
        unique_key = f"{owner_id}:{file_unique_id}"

        if unique_key in self.unique_id_cache:
            self.stats["blocked"] += 1
            logger.debug(
                "Fast filter BLOCKED (unique_id) for user %s: %s...",
                owner_id, file_unique_id[:20]
            )
            return True

        if file_signature:
            signature_key = f"{owner_id}:{file_signature}"
            if signature_key in self.signature_cache:
                self.stats["blocked"] += 1
                logger.debug(
                    "Fast filter BLOCKED (signature) for user %s: %s",
                    owner_id, file_signature
                )
                return True

        self.stats["passed"] += 1
        return False

    def add_to_cache(self, file_unique_id: str, owner_id: int,
                     file_signature: Optional[str] = None) -> None:
        """
        Add entry to caches after confirmation of uniqueness.

        Args:
            file_unique_id: Telegram unique file ID.
            owner_id: Owner's Telegram user ID (for per-user isolation).
            file_signature: Metadata signature (optional).
        """
        # Build per-user cache keys
        unique_key = f"{owner_id}:{file_unique_id}"
        self.unique_id_cache.add(unique_key)

        if file_signature:
            signature_key = f"{owner_id}:{file_signature}"
            self.signature_cache.add(signature_key)

        logger.debug(
            "Added to fast cache for user %s: %s...",
            owner_id, file_unique_id[:20]
        )

    def get_stats(self) -> Dict[str, int]:
        """Return filter statistics and cache sizes."""
        return {
            **self.stats,
            "cache_size_unique_ids": self.unique_id_cache.size,
            "cache_size_signatures": self.signature_cache.size,
        }

    def clear_user_cache(self, owner_id: int) -> None:
        """
        Clear ALL cache entries for a specific user.
        
        Iterates through both caches and removes any entry
        belonging to the specified user. This is called when
        a user's files are deleted or the user is banned.
        
        ✅ FIXED v3.0.3: Now properly removes entries instead
        of just logging. Uses safe iteration to avoid
        dictionary modification during iteration.

        Args:
            owner_id: Owner's Telegram user ID.
        """
        prefix = f"{owner_id}:"
        total_removed = 0
        
        # ✅ Clear from unique_id_cache
        try:
            uid_keys_to_remove = [
                k for k in list(self.unique_id_cache._cache.keys())
                if k.startswith(prefix)
            ]
            for k in uid_keys_to_remove:
                self.unique_id_cache._cache.pop(k, None)
            total_removed += len(uid_keys_to_remove)
        except Exception as e:
            logger.error(
                "Error clearing unique_id_cache for user %s: %s",
                owner_id, e
            )
        
        # ✅ Clear from signature_cache
        try:
            sig_keys_to_remove = [
                k for k in list(self.signature_cache._cache.keys())
                if k.startswith(prefix)
            ]
            for k in sig_keys_to_remove:
                self.signature_cache._cache.pop(k, None)
            total_removed += len(sig_keys_to_remove)
        except Exception as e:
            logger.error(
                "Error clearing signature_cache for user %s: %s",
                owner_id, e
            )
        
        # Update statistics
        if total_removed > 0:
            self.stats["cache_clears"] += 1
            self.stats["total_entries_cleared"] += total_removed
            logger.info(
                "✅ Cache cleared for user %s: %s entries removed "
                "(unique_id: %s, signature: %s)",
                owner_id, total_removed,
                len(uid_keys_to_remove) if 'uid_keys_to_remove' in locals() else 0,
                len(sig_keys_to_remove) if 'sig_keys_to_remove' in locals() else 0
            )
        else:
            logger.debug(
                "No cache entries found for user %s", owner_id
            )


# Global singleton
fast_filter = FastFilter()