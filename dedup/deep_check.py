"""
Telegram Media Storage Bot v3.0.0
Deep Duplicate Check (Database Layer)

Performs authoritative duplicate verification by querying the
database. This is the source of truth for deduplication.
"""

import logging
from typing import Dict

from config import DEDUP_STRICT_MODE
from database.models import MediaFile

logger = logging.getLogger(__name__)


class DeepChecker:
    """
    Permanent duplicate verification using SQLite.

    Queries the media_files table to determine if a file already
    exists for a given user. Supports both exact file_unique_id
    matching and metadata signature matching (strict mode).
    """

    def __init__(self):
        self.stats: Dict[str, int] = {
            "checked": 0,
            "duplicates_found": 0,
            "unique_accepted": 0,
        }

    async def is_duplicate(self, media_data: dict) -> bool:
        """
        Check the database for an existing duplicate within the user's scope.

        Args:
            media_data: Must contain 'file_unique_id', optionally
                        'file_signature', and 'owner_id'.

        Returns:
            True if a duplicate exists.
        """
        self.stats["checked"] += 1

        signature = (
            media_data.get("file_signature")
            if DEDUP_STRICT_MODE
            else None
        )

        owner_id = media_data["owner_id"]

        is_dup = await MediaFile.is_duplicate(
            file_unique_id=media_data["file_unique_id"],
            file_signature=signature,
            owner_id=owner_id,
        )

        if is_dup:
            self.stats["duplicates_found"] += 1
            logger.info(
                "Deep check DUPLICATE for user %s: %s",
                owner_id,
                media_data.get("file_name", "unknown")
            )
        else:
            self.stats["unique_accepted"] += 1
            logger.debug(
                "Deep check UNIQUE for user %s: %s",
                owner_id,
                media_data.get("file_name", "unknown")
            )

        return is_dup

    def get_stats(self) -> Dict[str, int]:
        """Return deep check statistics."""
        return self.stats.copy()


# Global singleton
deep_checker = DeepChecker()