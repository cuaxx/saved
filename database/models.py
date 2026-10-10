"""
Telegram Media Storage Bot v3.0.0
Database Models and Query Layer

Provides high-level asynchronous data access operations for:
- User profile management
- Media file storage with per-user isolation
- Daily statistics with integrity verification
- Admin user management

FIXES v3.0.1:
- Removed f-string SQL injection in UserProfile.upsert()
  and connection.py migration code
- All SQL values now use parameterized queries
"""

import logging
from datetime import date
from typing import Dict, List, Optional

from config import (
    STATS_RETENTION_DAYS,
    USER_DEFAULT_FILE_LIMIT,
    USER_DEFAULT_STORAGE_MB,
)
from .connection import db

logger = logging.getLogger(__name__)

# Whitelist of allowed statistics field names (prevents SQL injection)
ALLOWED_STATS_FIELDS = {
    "files_added",
    "photos_added",
    "videos_added",
    "documents_added",
    "duplicates_rejected",
    "files_served",
}


# ============================================
# USER PROFILE
# ============================================
class UserProfile:
    """User profile database operations."""

    @staticmethod
    async def upsert(user_id: int, username: str = None,
                     first_name: str = None, last_name: str = None,
                     is_premium: bool = False) -> None:
        """
        Insert or update a user profile.

        Args:
            user_id: Telegram user ID.
            username: Telegram username (optional).
            first_name: User's first name.
            last_name: User's last name.
            is_premium: Telegram premium status.
        """
        # ✅ FIX: Use parameterized query instead of f-string
        # Default max_files_limit from config, passed as parameter
        await db.execute("""
            INSERT INTO users (
                user_id, username, first_name, last_name,
                is_premium, max_files_limit, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                username    = COALESCE(excluded.username, users.username),
                first_name  = COALESCE(excluded.first_name, users.first_name),
                last_name   = COALESCE(excluded.last_name, users.last_name),
                is_premium  = excluded.is_premium,
                updated_at  = CURRENT_TIMESTAMP
        """, (user_id, username, first_name, last_name,
              is_premium, USER_DEFAULT_FILE_LIMIT))
        await db.commit()

    @staticmethod
    async def get(user_id: int) -> Optional[Dict]:
        """
        Get a user's profile.

        Args:
            user_id: Telegram user ID.

        Returns:
            User profile dict or None.
        """
        row = await db.fetchone(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        return dict(row) if row else None

    @staticmethod
    async def increment_file_stats(user_id: int, file_size: int) -> None:
        """
        Increment a user's total file count and storage used.

        Args:
            user_id: Telegram user ID.
            file_size: Size of the added file in bytes.
        """
        await db.execute("""
            UPDATE users
            SET total_files = total_files + 1,
                total_size  = total_size + ?,
                updated_at  = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (file_size, user_id))
        await db.commit()

    @staticmethod
    async def is_banned(user_id: int) -> bool:
        """
        Check if a user is banned.

        Args:
            user_id: Telegram user ID.

        Returns:
            True if banned.
        """
        row = await db.fetchone(
            "SELECT is_banned FROM users WHERE user_id = ?", (user_id,)
        )
        return row["is_banned"] if row else False

    @staticmethod
    async def set_ban(user_id: int, banned: bool) -> None:
        """
        Ban or unban a user.

        Args:
            user_id: Telegram user ID.
            banned: True to ban, False to unban.
        """
        await db.execute(
            "UPDATE users SET is_banned = ?, updated_at = CURRENT_TIMESTAMP "
            "WHERE user_id = ?",
            (banned, user_id)
        )
        await db.commit()

    @staticmethod
    async def set_file_limit(user_id: int, limit: int) -> None:
        """
        Set a custom file limit for a user.

        Args:
            user_id: Telegram user ID.
            limit: Maximum number of files allowed.
        """
        await db.execute(
            "UPDATE users SET max_files_limit = ?, updated_at = CURRENT_TIMESTAMP "
            "WHERE user_id = ?",
            (limit, user_id)
        )
        await db.commit()

    @staticmethod
    async def get_all_users() -> List[Dict]:
        """
        Get all registered users.

        Returns:
            List of user profile dictionaries.
        """
        rows = await db.fetchall(
            "SELECT * FROM users ORDER BY total_files DESC"
        )
        return [dict(row) for row in rows]

    @staticmethod
    async def get_count() -> int:
        """
        Get the total number of registered users.

        Returns:
            Total user count.
        """
        row = await db.fetchone("SELECT COUNT(*) as count FROM users")
        return row["count"] if row else 0

    @staticmethod
    async def set_language(user_id: int, lang: str) -> None:
        """
        Set user's preferred language.

        Args:
            user_id: Telegram user ID.
            lang: Language code (id, en, ru, zh, ja).
        """
        await db.execute(
            "UPDATE users SET language_code = ?, updated_at = CURRENT_TIMESTAMP "
            "WHERE user_id = ?",
            (lang, user_id)
        )
        await db.commit()


# ============================================
# ADMIN USERS
# ============================================
class AdminUsers:
    """Admin user management database operations."""

    @staticmethod
    async def add(admin_id: int, added_by: int) -> bool:
        """
        Add a user as admin.

        Args:
            admin_id: User ID to promote.
            added_by: Admin who performed the action.

        Returns:
            True if added, False if already admin.
        """
        cursor = await db.execute(
            "INSERT OR IGNORE INTO admin_users (user_id, added_by) "
            "VALUES (?, ?)",
            (admin_id, added_by)
        )
        await db.commit()
        return cursor.rowcount > 0

    @staticmethod
    async def remove(admin_id: int) -> bool:
        """
        Remove a runtime admin.

        Args:
            admin_id: User ID to demote.

        Returns:
            True if removed, False if not found.
        """
        cursor = await db.execute(
            "DELETE FROM admin_users WHERE user_id = ?",
            (admin_id,)
        )
        await db.commit()
        return cursor.rowcount > 0

    @staticmethod
    async def get_all() -> List[Dict]:
        """
        Get all runtime admins.

        Returns:
            List of admin records.
        """
        rows = await db.fetchall("""
            SELECT a.*, u.username, u.first_name
            FROM admin_users a
            LEFT JOIN users u ON a.user_id = u.user_id
            ORDER BY a.added_at DESC
        """)
        return [dict(row) for row in rows]

    @staticmethod
    async def exists(admin_id: int) -> bool:
        """
        Check if a user is a runtime admin.

        Args:
            admin_id: User ID to check.

        Returns:
            True if admin.
        """
        row = await db.fetchone(
            "SELECT 1 FROM admin_users WHERE user_id = ?",
            (admin_id,)
        )
        return row is not None


class AdminMessage:
    """Admin message database operations for user-admin communication."""

    @staticmethod
    async def create(from_user_id: int, message_text: str) -> int:
        """
        Create a new message from user to admin.

        Args:
            from_user_id: Sender's Telegram user ID.
            message_text: Message content.

        Returns:
            Inserted row ID.
        """
        cursor = await db.execute(
            "INSERT INTO admin_messages (from_user_id, message_text) VALUES (?, ?)",
            (from_user_id, message_text)
        )
        await db.commit()
        return cursor.lastrowid

    @staticmethod
    async def get_unread_count() -> int:
        """Get count of unread admin messages."""
        row = await db.fetchone(
            "SELECT COUNT(*) as count FROM admin_messages WHERE is_read = FALSE"
        )
        return row["count"] if row else 0

    @staticmethod
    async def get_unread(limit: int = 10) -> list:
        """Get unread messages."""
        rows = await db.fetchall(
            "SELECT m.*, u.username, u.first_name "
            "FROM admin_messages m "
            "LEFT JOIN users u ON m.from_user_id = u.user_id "
            "WHERE m.is_read = FALSE "
            "ORDER BY m.created_at DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in rows]

    @staticmethod
    async def mark_replied(message_id: int, replied_by: int, reply_text: str) -> None:
        """Mark a message as replied with reply text."""
        await db.execute(
            "UPDATE admin_messages SET is_read = TRUE, replied_by = ?, "
            "reply_text = ?, replied_at = CURRENT_TIMESTAMP WHERE id = ?",
            (replied_by, reply_text, message_id)
        )
        await db.commit()

    @staticmethod
    async def get_by_id(message_id: int) -> dict:
        """Get a message by ID."""
        row = await db.fetchone(
            "SELECT m.*, u.username, u.first_name "
            "FROM admin_messages m "
            "LEFT JOIN users u ON m.from_user_id = u.user_id "
            "WHERE m.id = ?",
            (message_id,)
        )
        return dict(row) if row else None


# ============================================
# MEDIA FILES
# ============================================
class MediaFile:
    """Media file database operations with per-user isolation."""

    @staticmethod
    async def insert(media_data: dict) -> int:
        """
        Insert a new media file record.

        Uses INSERT OR IGNORE with UNIQUE(file_unique_id, owner_id) to
        prevent duplicate files within a user's scope.

        Args:
            media_data: Dictionary with file metadata including owner_id.

        Returns:
            Row ID of the inserted record, or 0 if ignored.
        """
        query = """
            INSERT OR IGNORE INTO media_files
            (file_id, file_unique_id, media_group_id, file_name,
             file_size, mime_type, media_type, width, height,
             duration, file_signature, owner_id, message_id, chat_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = await db.execute(query, (
            media_data["file_id"],
            media_data["file_unique_id"],
            media_data.get("media_group_id"),
            media_data.get("file_name"),
            media_data["file_size"],
            media_data.get("mime_type"),
            media_data["media_type"],
            media_data.get("width", 0),
            media_data.get("height", 0),
            media_data.get("duration", 0),
            media_data["file_signature"],
            media_data["owner_id"],
            media_data["message_id"],
            media_data["chat_id"],
        ))
        await db.commit()
        return cursor.lastrowid

    @staticmethod
    async def is_duplicate(file_unique_id: str, file_signature: str,
                           owner_id: int) -> bool:
        """
        Check for duplicate files within a user's scope.

        Performs two-stage verification:
        1. Exact file_unique_id + owner_id match.
        2. Metadata signature + owner_id match (strict mode).

        Args:
            file_unique_id: Telegram's unique file identifier.
            file_signature: Generated metadata signature.
            owner_id: Owner's Telegram user ID.

        Returns:
            True if duplicate exists.
        """
        # Exact match (fastest, most reliable)
        row = await db.fetchone(
            "SELECT 1 FROM media_files "
            "WHERE file_unique_id = ? AND owner_id = ?",
            (file_unique_id, owner_id)
        )
        if row:
            return True

        # Signature match (metadata-based)
        if file_signature:
            row = await db.fetchone(
                "SELECT 1 FROM media_files "
                "WHERE file_signature = ? AND owner_id = ?",
                (file_signature, owner_id)
            )
            if row:
                return True

        return False

    @staticmethod
    async def get_by_position(position: int, owner_id: int):
        """
        Get a single file by position for a specific user.

        Args:
            position: 1-indexed position (1 = newest).
            owner_id: Owner's Telegram user ID.

        Returns:
            File record or None.
        """
        offset = position - 1
        row = await db.fetchone(
            "SELECT * FROM media_files "
            "WHERE owner_id = ? "
            "ORDER BY created_at DESC LIMIT 1 OFFSET ?",
            (owner_id, offset)
        )
        return row

    @staticmethod
    async def get_range(start: int, end: int, owner_id: int,
                        max_range: int = 50) -> list:
        """
        Get a range of files for a specific user.

        Args:
            start: Start position (1-indexed).
            end: End position.
            owner_id: Owner's Telegram user ID.
            max_range: Maximum allowed range size.

        Returns:
            List of file records.
        """
        if start < 1:
            start = 1
        if end - start + 1 > max_range:
            end = start + max_range - 1

        offset = start - 1
        limit = end - start + 1
        rows = await db.fetchall(
            "SELECT * FROM media_files "
            "WHERE owner_id = ? "
            "ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (owner_id, limit, offset)
        )
        return rows

    @staticmethod
    async def get_range_all_users(start: int, end: int,
                                  max_range: int = 50) -> list:
        """
        Get a range of files across all users (admin only).

        Args:
            start: Start position.
            end: End position.
            max_range: Maximum allowed range size.

        Returns:
            List of file records.
        """
        if start < 1:
            start = 1
        if end - start + 1 > max_range:
            end = start + max_range - 1

        offset = start - 1
        limit = end - start + 1
        rows = await db.fetchall(
            "SELECT m.*, u.username, u.first_name "
            "FROM media_files m "
            "LEFT JOIN users u ON m.owner_id = u.user_id "
            "ORDER BY m.created_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        return rows

    @staticmethod
    async def get_total_count(owner_id: int = None) -> int:
        """
        Get the total number of files for a user or globally.

        Args:
            owner_id: If provided, count only this user's files.

        Returns:
            Total file count.
        """
        if owner_id is not None:
            row = await db.fetchone(
                "SELECT COUNT(*) as count FROM media_files WHERE owner_id = ?",
                (owner_id,)
            )
        else:
            row = await db.fetchone(
                "SELECT COUNT(*) as count FROM media_files"
            )
        return row["count"] if row else 0

    @staticmethod
    async def get_count_by_type(owner_id: int = None) -> dict:
        """
        Get file count and size grouped by media type.

        Args:
            owner_id: If provided, filter by owner.

        Returns:
            Dict mapping media_type to {count, size}.
        """
        if owner_id is not None:
            rows = await db.fetchall(
                "SELECT media_type, COUNT(*) as count, "
                "SUM(file_size) as total_size "
                "FROM media_files WHERE owner_id = ? "
                "GROUP BY media_type",
                (owner_id,)
            )
        else:
            rows = await db.fetchall(
                "SELECT media_type, COUNT(*) as count, "
                "SUM(file_size) as total_size "
                "FROM media_files GROUP BY media_type"
            )
        return {
            row["media_type"]: {"count": row["count"], "size": row["total_size"]}
            for row in rows
        }

    @staticmethod
    async def get_total_size(owner_id: int = None) -> int:
        """
        Get the total storage size in bytes.

        Args:
            owner_id: If provided, filter by owner.

        Returns:
            Total size in bytes.
        """
        if owner_id is not None:
            row = await db.fetchone(
                "SELECT SUM(file_size) as total FROM media_files "
                "WHERE owner_id = ?",
                (owner_id,)
            )
        else:
            row = await db.fetchone(
                "SELECT SUM(file_size) as total FROM media_files"
            )
        return row["total"] or 0 if row else 0

    @staticmethod
    async def get_actual_count_today(owner_id: int) -> int:
        """
        Get the actual count of files added today for a user.

        Args:
            owner_id: Owner's user ID.

        Returns:
            Number of files added today.
        """
        row = await db.fetchone(
            "SELECT COUNT(*) as count FROM media_files "
            "WHERE owner_id = ? AND DATE(created_at) = DATE('now')",
            (owner_id,)
        )
        return row["count"] if row else 0

    @staticmethod
    async def cleanup_old_stats() -> int:
        """
        Delete statistics records older than STATS_RETENTION_DAYS.

        Returns:
            Number of deleted records.
        """
        cursor = await db.execute(
            "DELETE FROM daily_stats "
            "WHERE stat_date < date('now', ?)",
            (f"-{STATS_RETENTION_DAYS} days",)
        )
        await db.commit()
        return cursor.rowcount


# ============================================
# DAILY STATISTICS
# ============================================
STATS_FIELD_MAP = {
    "files_added": "files_added",
    "photos_added": "photos_added",
    "videos_added": "videos_added",
    "documents_added": "documents_added",
    "duplicates_rejected": "duplicates_rejected",
    "files_served": "files_served",
}
class DailyStats:
    """Daily statistics database operations with per-user support."""

    @staticmethod
    async def increment(stat_date: date, owner_id: int,
                        field: str, value: int = 1) -> None:
        # Gunakan mapping untuk mendapatkan nama field yang aman
        safe_field = STATS_FIELD_MAP.get(field)
        if safe_field is None:
            raise ValueError(
                f"Invalid stats field: '{field}'. "
                f"Allowed: {list(STATS_FIELD_MAP.keys())}"
            )
        
        # Gunakan string literal yang aman dari mapping
        query = (
            f"INSERT INTO daily_stats (stat_date, owner_id, {safe_field}) "
            f"VALUES (?, ?, ?) "
            f"ON CONFLICT(stat_date, owner_id) DO UPDATE "
            f"SET {safe_field} = {safe_field} + ?"
        )
        await db.execute(query, (stat_date, owner_id, value, value))
        await db.commit()

    @staticmethod
    async def get_stats(owner_id: int, days: int = 7) -> list:
        """
        Get statistics for a user over a number of days.

        Args:
            owner_id: Owner's user ID.
            days: Number of past days to retrieve.

        Returns:
            List of daily stats dicts.
        """
        rows = await db.fetchall(
            "SELECT * FROM daily_stats "
            "WHERE owner_id = ? AND stat_date >= date('now', ?) "
            "ORDER BY stat_date DESC",
            (owner_id, f"-{days} days")
        )
        return [dict(row) for row in rows]

    @staticmethod
    async def get_global_stats(days: int = 7) -> list:
        """
        Get aggregated statistics for all users.

        Args:
            days: Number of past days.

        Returns:
            List of aggregated daily stats dicts.
        """
        rows = await db.fetchall(
            "SELECT stat_date, "
            "SUM(files_added) as files_added, "
            "SUM(photos_added) as photos_added, "
            "SUM(videos_added) as videos_added, "
            "SUM(documents_added) as documents_added, "
            "SUM(duplicates_rejected) as duplicates_rejected, "
            "SUM(files_served) as files_served, "
            "SUM(total_size_bytes) as total_size_bytes "
            "FROM daily_stats "
            "WHERE stat_date >= date('now', ?) "
            "GROUP BY stat_date "
            "ORDER BY stat_date DESC",
            (f"-{days} days",)
        )
        return [dict(row) for row in rows]

    @staticmethod
    async def get_total_served() -> int:
        """
        Get the total number of files served via /get globally.

        Returns:
            Total files served count.
        """
        row = await db.fetchone(
            "SELECT SUM(files_served) as total FROM daily_stats"
        )
        return row["total"] or 0 if row else 0

    @staticmethod
    async def recalculate_today(owner_id: int) -> None:
        # Gunakan transaksi eksklusif agar tidak bertabrakan dengan increment
        await db.execute("BEGIN EXCLUSIVE")
        try:
            await db.execute("""
                INSERT OR REPLACE INTO daily_stats
                (stat_date, owner_id, files_added, photos_added,
                 videos_added, documents_added, total_size_bytes)
                SELECT
                    DATE('now'),
                    ?,
                    COUNT(*),
                    SUM(CASE WHEN media_type = 'photo' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN media_type = 'video' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN media_type = 'document' THEN 1 ELSE 0 END),
                    SUM(file_size)
                FROM media_files
                WHERE owner_id = ? AND DATE(created_at) = DATE('now')
            """, (owner_id, owner_id))
            await db.execute("COMMIT")
            logger.info("Daily stats recalculated for user %s", owner_id)
        except Exception:
            await db.execute("ROLLBACK")
            raise

    @staticmethod
    async def verify_stats_integrity(owner_id: int) -> bool:
        """
        Verify and auto-fix statistics drift for a user.

        Args:
            owner_id: Owner's user ID.

        Returns:
            True if stats were consistent, False if fixed.
        """
        actual_count = await MediaFile.get_actual_count_today(owner_id)
        row = await db.fetchone(
            "SELECT files_added FROM daily_stats "
            "WHERE owner_id = ? AND stat_date = DATE('now')",
            (owner_id,)
        )
        stats_count = row["files_added"] if row else 0

        if actual_count != stats_count:
            logger.warning(
                "Stats drift for user %s: actual=%s, recorded=%s",
                owner_id, actual_count, stats_count
            )
            await DailyStats.recalculate_today(owner_id)
            return False
        return True