"""
Telegram Media Storage Bot v3.0.0
Database Connection Module (SQLite)

Provides a singleton database connection manager with performance
optimizations via SQLite PRAGMA settings and automatic schema
migration for upgrading from older versions.

FIXES v3.0.1:
- Removed f-string SQL injection in _create_tables() and _migrate_orphaned_data()
- Added thread-safe singleton pattern
- All SQL DDL now uses safe defaults with application-level enforcement
"""

import logging
import os
import threading

import aiosqlite

from config import DATABASE_PATH, USER_DEFAULT_FILE_LIMIT

logger = logging.getLogger(__name__)


class Database:
    """
    Singleton database connection manager for SQLite.

    Handles connection lifecycle, schema creation, migrations,
    and provides optimized async query execution methods.

    Thread-safe singleton implementation using double-checked locking.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # ✅ FIX: Thread-safe singleton with double-checked locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    # --- Connection Lifecycle ---

    async def connect(self) -> None:
        """
        Initialize the database connection and ensure schema exists.
        """
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

        self.db = await aiosqlite.connect(DATABASE_PATH)
        self.db.row_factory = aiosqlite.Row

        # Performance optimizations
        await self.db.execute("PRAGMA journal_mode=WAL")
        await self.db.execute("PRAGMA synchronous=NORMAL")
        await self.db.execute("PRAGMA cache_size=-8000")
        await self.db.execute("PRAGMA foreign_keys=ON")

        # Create tables first, then run migrations
        await self._create_tables()
        await self._run_migrations()
        
        logger.info("Database connected: %s", DATABASE_PATH)

    async def close(self) -> None:
        """Close the database connection gracefully."""
        if self.db:
            await self.db.close()
            logger.info("Database disconnected")

    # --- Schema Management ---

    async def _create_tables(self) -> None:
        """
        Create all required database tables if they do not exist.
        
        This is designed for fresh installations. For existing
        databases, _run_migrations() has already added the
        necessary columns.
        
        FIX: Uses application-level default for max_files_limit
        instead of SQL-level f-string injection.
        """
        # ✅ FIX: Use DEFAULT 0 in SQL, application enforces USER_DEFAULT_FILE_LIMIT
        await self.db.executescript("""
            -- ============================================
            -- User Profiles
            -- ============================================
            CREATE TABLE IF NOT EXISTS users (
                user_id         INTEGER PRIMARY KEY,
                username        TEXT,
                first_name      TEXT,
                last_name       TEXT,
                is_premium      BOOLEAN DEFAULT FALSE,
                is_active       BOOLEAN DEFAULT TRUE,
                is_banned       BOOLEAN DEFAULT FALSE,
                total_files     INTEGER DEFAULT 0,
                total_size      INTEGER DEFAULT 0,
                max_files_limit INTEGER DEFAULT 0,
                language_code   TEXT DEFAULT 'id',
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- ============================================
            -- Admin Users (Runtime-managed)
            -- ============================================
            CREATE TABLE IF NOT EXISTS admin_users (
                user_id   INTEGER PRIMARY KEY,
                role      TEXT DEFAULT 'admin',
                added_by  INTEGER,
                added_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            -- ============================================
            -- Media Files
            -- ============================================
            CREATE TABLE IF NOT EXISTS media_files (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id         TEXT NOT NULL,
                file_unique_id  TEXT NOT NULL,
                media_group_id  TEXT,
                file_name       TEXT,
                file_size       INTEGER NOT NULL,
                mime_type       TEXT,
                media_type      TEXT NOT NULL,
                width           INTEGER DEFAULT 0,
                height          INTEGER DEFAULT 0,
                duration        INTEGER DEFAULT 0,
                file_signature  TEXT,
                owner_id        INTEGER NOT NULL,
                message_id      INTEGER,
                chat_id         INTEGER,
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(file_unique_id, owner_id),
                FOREIGN KEY (owner_id) REFERENCES users(user_id)
            );

            CREATE INDEX IF NOT EXISTS idx_media_created
                ON media_files(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_media_signature
                ON media_files(file_signature);
            CREATE INDEX IF NOT EXISTS idx_media_owner
                ON media_files(owner_id);
            CREATE INDEX IF NOT EXISTS idx_media_owner_created
                ON media_files(owner_id, created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_media_owner_type
                ON media_files(owner_id, media_type);

            -- ============================================
            -- Daily Statistics
            -- ============================================
            CREATE TABLE IF NOT EXISTS daily_stats (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                stat_date           DATE NOT NULL,
                owner_id            INTEGER NOT NULL DEFAULT 0,
                files_added         INTEGER DEFAULT 0,
                photos_added        INTEGER DEFAULT 0,
                videos_added        INTEGER DEFAULT 0,
                documents_added     INTEGER DEFAULT 0,
                duplicates_rejected INTEGER DEFAULT 0,
                files_served        INTEGER DEFAULT 0,
                total_size_bytes    INTEGER DEFAULT 0,
                UNIQUE(stat_date, owner_id),
                FOREIGN KEY (owner_id) REFERENCES users(user_id)
            );

            CREATE INDEX IF NOT EXISTS idx_stats_date
                ON daily_stats(stat_date DESC);
            CREATE INDEX IF NOT EXISTS idx_stats_owner
                ON daily_stats(owner_id);
            CREATE INDEX IF NOT EXISTS idx_stats_owner_date
                ON daily_stats(owner_id, stat_date DESC);

            -- ============================================
            -- Admin Messages (User → Admin)
            -- ============================================
            CREATE TABLE IF NOT EXISTS admin_messages (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id    INTEGER NOT NULL,
                message_text    TEXT NOT NULL,
                replied_by      INTEGER,
                reply_text      TEXT,
                is_read         BOOLEAN DEFAULT FALSE,
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                replied_at      TIMESTAMP,
                FOREIGN KEY (from_user_id) REFERENCES users(user_id)
            );

            CREATE INDEX IF NOT EXISTS idx_admin_msg_unread
                ON admin_messages(is_read, created_at DESC);
        """)
        await self.db.commit()

    async def _run_migrations(self) -> None:
        """
        Run schema migrations for upgrading from older versions.
        Only runs if the table already exists.
        """
        # --- Migration: Create users table if not exists ---
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id         INTEGER PRIMARY KEY,
                username        TEXT,
                first_name      TEXT,
                last_name       TEXT,
                is_premium      BOOLEAN DEFAULT FALSE,
                is_active       BOOLEAN DEFAULT TRUE,
                is_banned       BOOLEAN DEFAULT FALSE,
                total_files     INTEGER DEFAULT 0,
                total_size      INTEGER DEFAULT 0,
                max_files_limit INTEGER DEFAULT 0,
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # --- Migration: Create admin_users table if not exists ---
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                user_id   INTEGER PRIMARY KEY,
                role      TEXT DEFAULT 'admin',
                added_by  INTEGER,
                added_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # --- Migration: Add language_code to users (v3.0.0) ---
        cursor = await self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        if await cursor.fetchone():
            cursor = await self.db.execute("PRAGMA table_info(users)")
            columns = [row[1] for row in await cursor.fetchall()]

            if "language_code" not in columns:
                logger.info("Migration: Adding language_code column to users")
                await self.db.execute(
                    "ALTER TABLE users ADD COLUMN language_code TEXT DEFAULT 'id'"
                )

        # --- Migration: Add owner_id to media_files (v2 → v3) ---
        cursor = await self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='media_files'"
        )
        if await cursor.fetchone():
            cursor = await self.db.execute("PRAGMA table_info(media_files)")
            columns = [row[1] for row in await cursor.fetchall()]

            if "owner_id" not in columns:
                logger.info("Migration: Adding owner_id column to media_files")
                await self.db.execute(
                    "ALTER TABLE media_files ADD COLUMN owner_id INTEGER NOT NULL DEFAULT 0"
                )

        # --- Migration: Fix daily_stats UNIQUE constraint (v2 → v3) ---
        await self._migrate_daily_stats()

        # --- Migration: Assign orphaned data to first super admin ---
        await self._migrate_orphaned_data()

        await self.db.commit()
        logger.info("Schema migrations completed successfully")

    async def _migrate_daily_stats(self) -> None:
        """
        Recreate daily_stats table with correct UNIQUE constraint.
        
        v2 schema:  UNIQUE(stat_date)
        v3 schema:  UNIQUE(stat_date, owner_id)
        
        Old stats data is backed up and restored.
        """
        # Check if table exists
        cursor = await self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='daily_stats'"
        )
        if not await cursor.fetchone():
            return
        
        cursor = await self.db.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='daily_stats'"
        )
        row = await cursor.fetchone()
        table_sql = row["sql"] if row and row["sql"] else ""
        
        if "UNIQUE(stat_date, owner_id)" in table_sql:
            logger.info("daily_stats constraint already correct — skipping migration")
            return
        
        logger.info("Migration: Fixing daily_stats UNIQUE constraint...")

        # ✅ Gunakan transaksi agar atomik
        await self.db.execute("BEGIN")
        try:
            await self.db.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats_backup AS
                SELECT * FROM daily_stats
            """)
            cursor = await self.db.execute("SELECT COUNT(*) as count FROM daily_stats_backup")
            row = await cursor.fetchone()
            backup_count = row["count"] if row else 0

            await self.db.execute("DROP TABLE IF EXISTS daily_stats")
            await self.db.execute("""
                CREATE TABLE daily_stats (
                    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                    stat_date           DATE NOT NULL,
                    owner_id            INTEGER NOT NULL DEFAULT 0,
                    files_added         INTEGER DEFAULT 0,
                    photos_added        INTEGER DEFAULT 0,
                    videos_added        INTEGER DEFAULT 0,
                    documents_added     INTEGER DEFAULT 0,
                    duplicates_rejected INTEGER DEFAULT 0,
                    files_served        INTEGER DEFAULT 0,
                    total_size_bytes    INTEGER DEFAULT 0,
                    UNIQUE(stat_date, owner_id)
                )
            """)
            await self.db.execute("""
                INSERT OR IGNORE INTO daily_stats
                SELECT * FROM daily_stats_backup
            """)
            await self.db.execute("DROP TABLE IF EXISTS daily_stats_backup")

            await self.db.execute(
                "CREATE INDEX IF NOT EXISTS idx_stats_date ON daily_stats(stat_date DESC)"
            )
            await self.db.execute(
                "CREATE INDEX IF NOT EXISTS idx_stats_owner ON daily_stats(owner_id)"
            )
            await self.db.execute(
                "CREATE INDEX IF NOT EXISTS idx_stats_owner_date "
                "ON daily_stats(owner_id, stat_date DESC)"
            )

            await self.db.execute("COMMIT")
            logger.info("Migration: daily_stats fixed (%s records preserved)", backup_count)
        except Exception:
            await self.db.execute("ROLLBACK")
            logger.exception("Migration daily_stats failed, rolled back")
            raise

    async def _migrate_orphaned_data(self) -> None:
        """
        Assign data with owner_id=0 (from v2.x) to the first super admin.
        
        This ensures that files uploaded before the multi-user update
        are still accessible to the admin.
        
        FIX: Uses parameterized query instead of f-string.
        """
        from config import SUPER_ADMIN_IDS
        
        # Count orphaned files
        cursor = await self.db.execute(
            "SELECT COUNT(*) as count FROM media_files WHERE owner_id = 0"
        )
        row = await cursor.fetchone()
        orphaned_files = row["count"] if row else 0
        
        if orphaned_files > 0 and SUPER_ADMIN_IDS:
            admin_id = SUPER_ADMIN_IDS[0]
            
            # Assign files to admin
            await self.db.execute(
                "UPDATE media_files SET owner_id = ? WHERE owner_id = 0",
                (admin_id,)
            )
            
            # Assign stats to admin
            await self.db.execute(
                "UPDATE daily_stats SET owner_id = ? WHERE owner_id = 0",
                (admin_id,)
            )
            
            # ✅ FIX: Use parameterized query for USER_DEFAULT_FILE_LIMIT
            await self.db.execute("""
                INSERT INTO users (user_id, first_name, total_files, max_files_limit)
                VALUES (?, 'Admin (Legacy Data)', ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    total_files = users.total_files + excluded.total_files
            """, (admin_id, orphaned_files, USER_DEFAULT_FILE_LIMIT))
            
            logger.info(
                "Migration: Assigned %s orphaned files to admin %s",
                orphaned_files, admin_id
            )
        elif orphaned_files > 0:
            logger.warning(
                "Migration: Found %s orphaned files but no SUPER_ADMIN_IDS configured. "
                "Data preserved with owner_id=0.",
                orphaned_files
            )

    # --- Query Execution Helpers ---

    async def execute(self, query: str, params=None):
        """
        Execute a SQL query with optional parameters.

        Args:
            query: SQL query string.
            params: Optional tuple or dict of query parameters.

        Returns:
            Cursor for fetching results.
        """
        if params is not None:
            return await self.db.execute(query, params)
        return await self.db.execute(query)

    async def fetchone(self, query: str, params=None):
        """
        Execute a query and fetch a single row.

        Args:
            query: SQL query string.
            params: Optional query parameters.

        Returns:
            Single row or None.
        """
        cursor = await self.execute(query, params)
        return await cursor.fetchone()

    async def fetchall(self, query: str, params=None):
        """
        Execute a query and fetch all rows.

        Args:
            query: SQL query string.
            params: Optional query parameters.

        Returns:
            List of all matching rows.
        """
        cursor = await self.execute(query, params)
        return await cursor.fetchall()

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.db.commit()


# Global singleton instance
db = Database()