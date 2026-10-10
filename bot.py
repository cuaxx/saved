"""
Telegram Media Storage Bot v3.0.4
Main Entry Point

A high-performance, multi-user Telegram bot for storing,
deduplicating, and retrieving media files with automatic
cleanup, per-user isolation, admin panel, broadcast,
user-admin messaging, multi-language support, and file deletion.

FIXES v3.0.4:
- ✅ Fixed: SQL injection risk in DailyStats.increment()
- ✅ Fixed: Race condition in media group buffer handling
- ✅ Fixed: Startup performance bottleneck (verification moved to background)
- ✅ Fixed: File logging permission handling with graceful fallback
- ✅ NEW: Per-user queue system for responsive handling of large media bursts
"""

import asyncio
import logging
import os
import signal
import sys
import traceback

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    ALLOWED_TYPES,
    BOT_TOKEN,
    LOG_FILE,
    LOG_LEVEL,
    SUPER_ADMIN_IDS,
)
from database.connection import db
from handlers.admin_handler import (
    handle_admin,
    handle_admin_message,
    handle_admin_users_callback,
    handle_ban,
    handle_ban_callback,
    handle_broadcast,
    handle_reply,
    handle_unban,
)
from handlers.command_handler import (
    get_callback_store,
    handle_get,
    handle_get_callback,
    handle_help,
    handle_language,
    handle_language_callback,
    handle_mylimit,
    handle_page_jump_reply,
    handle_start,
    handle_stats,
)
from handlers.delete_handler import (
    handle_delete,
    handle_delete_callback,
)
from handlers.media_handler import (
    handle_media,
    init_worker_system,
    start_cleanup_task,
    stop_all_workers,
    _process_single_media,
)
from utils.callback_cleaner import callback_cleaner
from utils.callback_monitor import init_callback_monitor
from utils.cleaner import cleaner
from utils.health_server import health_server
from utils.limiter import create_rate_limiter

# ============================================
# LOGGING SETUP WITH GRACEFUL FALLBACK
# ============================================
LOG_DIR = "logs"

# Try to create logs directory and test write permission
try:
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Test write permission
    test_file = os.path.join(LOG_DIR, ".write_test")
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        log_dir_writable = True
    except (OSError, PermissionError, IOError) as exc:
        log_dir_writable = False
        print(f"⚠️  Warning: Cannot write to '{LOG_DIR}' directory: {exc}")
        print("    File logging disabled. Logging to console only.")
except (OSError, PermissionError) as exc:
    log_dir_writable = False
    print(f"⚠️  Warning: Cannot create '{LOG_DIR}' directory: {exc}")
    print("    File logging disabled. Logging to console only.")

# Setup handlers (console always available)
handlers = [logging.StreamHandler(sys.stdout)]

# Try to add file handler if directory is writable
file_handler = None
if log_dir_writable:
    try:
        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding='utf-8'
        )
        handlers.append(file_handler)
        print(f"✅ File logging enabled: {LOG_FILE}")
    except (OSError, PermissionError, IOError) as exc:
        print(f"⚠️  Warning: Cannot create log file '{LOG_FILE}': {exc}")
        print("    File logging disabled. Logging to console only.")
else:
    print(f"⚠️  Log file '{LOG_FILE}' will not be created.")
    print(f"    Check permissions for '{LOG_DIR}' directory.")
    print("    To fix: chmod 755 logs/ or run with appropriate user")

# Apply logging configuration
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=handlers,
)

# Reduce noise from third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logging.getLogger("aiosqlite").setLevel(logging.WARNING)
logging.getLogger("aiohttp.access").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Log startup status
if log_dir_writable and file_handler:
    logger.info("File logging enabled: %s", LOG_FILE)
else:
    logger.warning("File logging disabled: using console only")


# ============================================
# BACKGROUND STATS VERIFICATION
# ============================================
async def _verify_stats_background(users, batch_size=30, delay_start=10):
    """
    Verify stats integrity as background task.
    
    Moved from blocking startup to background task
    to prevent slow bot initialization with many users.
    
    Args:
        users: List of user dicts from database
        batch_size: Number of users to process per batch
        delay_start: Seconds to wait before starting verification
    """
    # Wait for bot to be ready before starting verification
    logger.debug(
        "Stats verification will start in %s seconds...",
        delay_start
    )
    await asyncio.sleep(delay_start)
    
    total_users = len(users)
    logger.info(
        "Starting background stats verification for %s users "
        "(batch size: %s)",
        total_users, batch_size
    )
    
    from database.models import DailyStats
    
    verified_count = 0
    failed_count = 0
    batch_num = 0
    
    # Process dalam batch untuk menghindari overload
    for i in range(0, total_users, batch_size):
        batch = users[i:i + batch_size]
        batch_num += 1
        
        for user in batch:
            try:
                await DailyStats.verify_stats_integrity(user["user_id"])
                verified_count += 1
            except Exception as exc:
                failed_count += 1
                logger.warning(
                    "Stats verification failed for user %s: %s",
                    user["user_id"], exc
                )
        
        # Log progress setiap 5 batch
        if batch_num % 5 == 0 or i + batch_size >= total_users:
            processed = verified_count + failed_count
            logger.info(
                "Stats verification progress: %s/%s users "
                "(%s verified, %s failed)",
                processed, total_users, verified_count, failed_count
            )
        
        # Jeda antar batch untuk memberi ruang ke bot
        if i + batch_size < total_users:
            await asyncio.sleep(1)
    
    logger.info(
        "✅ Background stats verification complete: "
        "%s success, %s failed out of %s users",
        verified_count, failed_count, total_users
    )


# ============================================
# ERROR HANDLER
# ============================================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Telegram updates."""
    error_msg = f"Update {update} caused error: {context.error}"
    
    if context.error:
        error_traceback = ''.join(
            traceback.format_exception(
                type(context.error),
                context.error,
                context.error.__traceback__
            )
        )
        logger.error(
            "Update %s caused error: %s\n%s",
            update, context.error, error_traceback
        )
    else:
        logger.error(error_msg)


# ============================================
# SHUTDOWN HANDLER
# ============================================
shutdown_event = asyncio.Event()


def handle_shutdown_signal():
    """Handle graceful shutdown on SIGINT or SIGTERM."""
    logger.info("Shutdown signal received, initiating graceful shutdown...")
    shutdown_event.set()


# ============================================
# MEDIA FILTER BUILDER
# ============================================
def build_media_filter():
    """Build a composite message filter from allowed media types."""
    media_filter = None

    if "photo" in ALLOWED_TYPES:
        media_filter = filters.PHOTO

    if "video" in ALLOWED_TYPES:
        media_filter = (
            media_filter | filters.VIDEO
            if media_filter
            else filters.VIDEO
        )

    if "document" in ALLOWED_TYPES:
        media_filter = (
            media_filter | filters.Document.ALL
            if media_filter
            else filters.Document.ALL
        )

    return media_filter


# ============================================
# HANDLER REGISTRATION
# ============================================
def register_handlers(application: Application) -> None:
    """Register all bot command and message handlers."""
    # --- Media handler ---
    media_filter = build_media_filter()
    if media_filter:
        application.add_handler(
            MessageHandler(media_filter, handle_media)
        )
        logger.info("Media handler registered for: %s", ALLOWED_TYPES)

    # --- User commands ---
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("help", handle_help))
    application.add_handler(CommandHandler("get", handle_get))
    application.add_handler(CommandHandler("stats", handle_stats))
    application.add_handler(CommandHandler("mylimit", handle_mylimit))
    application.add_handler(CommandHandler("language", handle_language))
    application.add_handler(CommandHandler("delete", handle_delete))
    logger.info(
        "User commands registered: start, help, get, stats, mylimit, "
        "language, delete"
    )

    # --- Admin commands ---
    application.add_handler(CommandHandler("admin", handle_admin))
    application.add_handler(CommandHandler("ban", handle_ban))
    application.add_handler(CommandHandler("unban", handle_unban))
    application.add_handler(CommandHandler("broadcast", handle_broadcast))
    application.add_handler(CommandHandler("reply", handle_reply))
    logger.info(
        "Admin commands registered: admin, ban, unban, broadcast, reply"
    )

    # --- User to Admin message handler ---
    application.add_handler(
        MessageHandler(
            filters.Regex(r'^@admin(\s|$)') & ~filters.COMMAND,
            handle_admin_message
        )
    )
    logger.info("Admin message handler registered: @admin")

    # --- Callback handlers ---
    # File browser navigation (short random keys - exclude del_ and ban_ prefix)
    application.add_handler(
        CallbackQueryHandler(
            handle_get_callback,
            pattern=r"^(?!del_)(?!ban_)[a-zA-Z0-9]{8}$"
        )
    )
    logger.info("File browser callback handler registered")

    # Delete confirmation callbacks (pattern: del_XXXXXXXX)
    application.add_handler(
        CallbackQueryHandler(
            handle_delete_callback,
            pattern=r"^del_[a-zA-Z0-9]{8}$"
        )
    )
    logger.info("Delete confirmation callback handler registered")

    # Ban/Unban confirmation callbacks (pattern: ban_XXXXXXXX)
    application.add_handler(
        CallbackQueryHandler(
            handle_ban_callback,
            pattern=r"^ban_[a-zA-Z0-9]{8}$"
        )
    )
    logger.info("Ban/unban confirmation callback handler registered")

    # Language selection keyboard
    application.add_handler(
        CallbackQueryHandler(
            handle_language_callback,
            pattern=r"^(lang:|ignore$)"
        )
    )
    logger.info("Language selection callback handler registered")

    # Admin users list navigation (Next/Prev)
    application.add_handler(
        CallbackQueryHandler(
            handle_admin_users_callback,
            pattern=r"^admin_users:"
        )
    )
    logger.info("Admin users navigation callback handler registered")

    # --- ForceReply handler for page jump ---
    application.add_handler(
        MessageHandler(
            filters.REPLY & filters.TEXT & ~filters.COMMAND,
            handle_page_jump_reply
        )
    )
    logger.info("Page jump reply handler registered")


# ============================================
# MAIN APPLICATION
# ============================================
async def main() -> None:
    """Main async application entry point."""

    loop = asyncio.get_running_loop()
    try:
        loop.add_signal_handler(signal.SIGINT, handle_shutdown_signal)
        loop.add_signal_handler(signal.SIGTERM, handle_shutdown_signal)
    except NotImplementedError:
        # Windows fallback
        signal.signal(signal.SIGINT, lambda s, f: handle_shutdown_signal())
        signal.signal(signal.SIGTERM, lambda s, f: handle_shutdown_signal())

    logger.info("=" * 50)
    logger.info("Telegram Media Storage Bot v3.0.4")
    logger.info("Starting initialization...")
    logger.info("=" * 50)

    # Global reference untuk callback monitor
    callback_monitor = None

    try:
        # --- Database initialization ---
        logger.info("Connecting to database...")
        await db.connect()
        logger.info("Database initialized successfully")

        # --- Schedule background stats verification ---
        try:
            from database.models import UserProfile
            
            users = await UserProfile.get_all_users()
            
            if users:
                asyncio.create_task(
                    _verify_stats_background(
                        users,
                        batch_size=30,
                        delay_start=10
                    )
                )
                logger.info(
                    "✅ Stats verification scheduled for %s users "
                    "(running in background, non-blocking)",
                    len(users)
                )
            else:
                logger.info("No users yet, stats verification skipped")
        except Exception as exc:
            logger.warning(
                "Stats verification scheduling skipped: %s", exc
            )

        # --- Start background workers ---
        await cleaner.start()
        logger.info("Message cleaner worker started")
        
        await callback_cleaner.start(get_callback_store())
        logger.info("Callback store cleaner started")

        # --- Build application ---
        logger.info("Building Telegram application...")
        application = (
            Application.builder()
            .token(BOT_TOKEN)
            .rate_limiter(create_rate_limiter())
            .concurrent_updates(10)   # Process up to 10 updates concurrently
            .build()
        )

        application.add_error_handler(error_handler)
        register_handlers(application)
        logger.info("All handlers registered")

        # --- Initialize per-user worker system ---
        # Pass the bot instance and the media processing function
        init_worker_system(application.bot, _process_single_media)
        await start_cleanup_task()
        logger.info("Per-user queue workers initialized (queue size: configurable, idle timeout: 30s)")

        # --- Initialize and start bot ---
        logger.info("Initializing bot...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling(
            allowed_updates=Update.ALL_TYPES,
            poll_interval=3.0,
            timeout=30,
            drop_pending_updates=True,
        )
        logger.info("🤖 Bot is running. Press Ctrl+C to stop.")

        # --- Start health server ---
        try:
            await health_server.start()
            logger.info(
                "Health server started at http://%s:%s",
                health_server.host, health_server.port
            )
        except Exception as exc:
            logger.error(
                "Failed to start health server (bot continues): %s",
                exc
            )

        # --- Start callback store monitor ---
        try:
            callback_store = get_callback_store()
            callback_monitor = init_callback_monitor(
                callback_store=callback_store,
                bot=application.bot,
                admin_ids=SUPER_ADMIN_IDS,
                max_size=10000,
                interval=1800,
                warning_threshold=0.8
            )
            await callback_monitor.start()
            logger.info(
                "Callback store monitor started "
                "(interval: 30min, warning: 80%%)"
            )
        except Exception as exc:
            logger.error(
                "Failed to start callback monitor (bot continues): %s",
                exc
            )

        # ✅ Bot fully initialized
        logger.info("✅ Bot initialization complete. All systems ready.")

        # --- Wait for shutdown signal ---
        await shutdown_event.wait()
        logger.info("Initiating shutdown sequence...")

        # --- Graceful shutdown ---
        shutdown_errors = []
        
        # Stop callback monitor
        if callback_monitor:
            try:
                await callback_monitor.stop()
                logger.info("Callback monitor stopped")
            except Exception as exc:
                error_msg = f"Error stopping callback monitor: {exc}"
                logger.error(error_msg)
                shutdown_errors.append(error_msg)

        # Stop health server
        try:
            await health_server.stop()
            logger.info("Health server stopped")
        except Exception as exc:
            error_msg = f"Error stopping health server: {exc}"
            logger.error(error_msg)
            shutdown_errors.append(error_msg)
        
        # Stop bot poller
        try:
            await application.updater.stop()
            logger.info("Bot poller stopped")
        except Exception as exc:
            error_msg = f"Error stopping poller: {exc}"
            logger.error(error_msg)
            shutdown_errors.append(error_msg)
        
        # Stop application
        try:
            await application.stop()
            await application.shutdown()
            logger.info("Application shutdown complete")
        except Exception as exc:
            error_msg = f"Error shutting down application: {exc}"
            logger.error(error_msg)
            shutdown_errors.append(error_msg)

        # --- Stop per-user workers ---
        try:
            await stop_all_workers()
            logger.info("All per-user workers stopped")
        except Exception as exc:
            error_msg = f"Error stopping per-user workers: {exc}"
            logger.error(error_msg)
            shutdown_errors.append(error_msg)

    except Exception as exc:
        logger.critical(
            "Fatal error during execution: %s\n%s",
            exc,
            ''.join(traceback.format_exc())
        )
        sys.exit(1)
    finally:
        # Stop callback cleaner
        try:
            await callback_cleaner.stop()
            logger.info("Callback cleaner stopped")
        except Exception as exc:
            logger.error("Error stopping callback cleaner: %s", exc)

        # Stop message cleaner
        try:
            await cleaner.stop()
            logger.info("Message cleaner stopped")
        except Exception as exc:
            logger.error("Error stopping message cleaner: %s", exc)

        # Close database
        try:
            await db.close()
            logger.info("Database connection closed")
        except Exception as exc:
            logger.error("Error closing database: %s", exc)

        # Final shutdown log
        if shutdown_errors:
            logger.warning(
                "Bot shutdown complete with %s errors: %s",
                len(shutdown_errors), shutdown_errors
            )
        else:
            logger.info("✅ Bot shutdown complete — all services stopped cleanly")


# ============================================
# ENTRY POINT
# ============================================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as exc:
        logger.critical(
            "Fatal error on startup: %s\n%s",
            exc,
            ''.join(traceback.format_exc())
        )
        sys.exit(1)