"""
Telegram Media Storage Bot v3.0.0
User Manager Middleware

Handles automatic user registration, ban checks, and per-user
limit enforcement. Called before processing any user request.
"""

import logging
from typing import Optional

from telegram import Update

from config import USER_DEFAULT_FILE_LIMIT, USER_DEFAULT_STORAGE_MB
from database.models import MediaFile, UserProfile

logger = logging.getLogger(__name__)


class UserManager:
    """
    Manages user lifecycle: registration, ban checks, and quota.

    Ensures every interacting user has a profile and validates
    their ability to perform actions before processing.
    """

    async def ensure_user_exists(self, update: Update) -> None:
        """
        Auto-create or update a user profile from Telegram data.

        Args:
            update: The incoming Telegram Update.
        """
        user = update.message.from_user
        if user is None:
            return

        await UserProfile.upsert(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_premium=getattr(user, "is_premium", False),
        )

    async def is_banned(self, user_id: int) -> bool:
        """
        Check if a user is banned.

        Args:
            user_id: Telegram user ID.

        Returns:
            True if banned.
        """
        return await UserProfile.is_banned(user_id)

    async def has_quota(self, user_id: int) -> bool:
        """
        Check if a user has remaining file quota.

        Args:
            user_id: Telegram user ID.

        Returns:
            True if user can upload more files.
        """
        profile = await UserProfile.get(user_id)
        if profile is None:
            return True

        limit = profile.get("max_files_limit", USER_DEFAULT_FILE_LIMIT)
        if limit <= 0:
            return True  # Unlimited

        current = await MediaFile.get_total_count(owner_id=user_id)
        return current < limit

    async def get_remaining_quota(self, user_id: int) -> Optional[int]:
        """
        Get the number of files a user can still upload.

        Args:
            user_id: Telegram user ID.

        Returns:
            Remaining quota, or None if unlimited.
        """
        profile = await UserProfile.get(user_id)
        if profile is None:
            return USER_DEFAULT_FILE_LIMIT

        limit = profile.get("max_files_limit", USER_DEFAULT_FILE_LIMIT)
        if limit <= 0:
            return None  # Unlimited

        current = await MediaFile.get_total_count(owner_id=user_id)
        return max(0, limit - current)


# Global singleton
user_manager = UserManager()