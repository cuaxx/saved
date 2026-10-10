"""
Telegram Media Storage Bot v3.0.4
Media Upload Handler

Processes all incoming media messages through the two-layer
deduplication pipeline with per-user isolation, quota enforcement,
and ban checks.

CHANGES v3.0.4 (Queue per user):
- Added per-user queue system with bounded size (configurable)
- Media messages are now validated quickly then enqueued
- Background workers process each user's queue sequentially
- Bot remains responsive even under heavy load from a single user
"""

import asyncio
import logging
import time
from collections import defaultdict
from datetime import date
from typing import Dict, Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import (
    DELETE_DELAY_SECONDS,
    DELETE_MEDIA_ONLY,
    GROUP_BUFFER_SECONDS,
    MAX_FILES_TOTAL,
    MAX_FILE_SIZE_MB,
    USER_QUEUE_MAXSIZE,
    TOTAL_QUEUED_LIMIT,
    MAX_CONCURRENT_WORKERS,
    WORKER_IDLE_TIMEOUT,
)
from database.connection import db
from database.models import DailyStats, MediaFile, UserProfile
from dedup.deep_check import deep_checker
from dedup.fast_filter import fast_filter
from locales.loader import get_text, get_user_language
from middleware import user_manager
from utils.cleaner import cleaner
from utils.enums import MediaType
from utils.helpers import (
    extract_media_data,
    is_allowed_type,
    is_within_size_limit,
)

logger = logging.getLogger(__name__)

# ============================================
# MEDIA GROUP BUFFER (existing)
# ============================================
group_buffer = defaultdict(list)
group_tokens = {}


# ============================================
# PER-USER QUEUE SYSTEM (NEW)
# ============================================
_user_queues: Dict[int, asyncio.Queue] = {}
_user_workers: Dict[int, asyncio.Task] = {}
_user_last_active: Dict[int, float] = {}
_user_dict_lock = asyncio.Lock()
_total_queued_items = 0
_total_queue_lock = asyncio.Lock()

# Referensi ke bot dan fungsi pemrosesan sebenarnya (di-set dari bot.py)
_bot = None
_process_single_media_func = None


def init_worker_system(bot, process_single_media_func):
    """Initialize per-user queue system (call from bot.py)."""
    global _bot, _process_single_media_func
    _bot = bot
    _process_single_media_func = process_single_media_func
    logger.info("Per-user queue system initialized")


async def _get_total_queued() -> int:
    """Get total pending items across all queues."""
    async with _total_queue_lock:
        return _total_queued_items


async def _inc_total_queued(delta: int = 1) -> int:
    """Increment or decrement total queued counter."""
    async with _total_queue_lock:
        global _total_queued_items
        _total_queued_items += delta
        return _total_queued_items


async def enqueue_media(user_id: int, update, context, media_data: dict, lang: str) -> bool:
    """
    Add a media item to the user's queue.
    Returns True if enqueued successfully, False if queue is full or global limit reached.
    """
    # Check global total limit first
    total_queued = await _get_total_queued()
    if total_queued >= TOTAL_QUEUED_LIMIT:
        logger.warning(f"Global queue limit reached ({TOTAL_QUEUED_LIMIT}), rejecting media from user {user_id}")
        return False

    async with _user_dict_lock:
        # Create queue for user if not exists
        if user_id not in _user_queues:
            if len(_user_workers) >= MAX_CONCURRENT_WORKERS:
                logger.warning(f"Max workers ({MAX_CONCURRENT_WORKERS}) reached, cannot create queue for user {user_id}")
                return False
            _user_queues[user_id] = asyncio.Queue(maxsize=USER_QUEUE_MAXSIZE)

        queue = _user_queues[user_id]

        # Try to put item (non-blocking)
        try:
            queue.put_nowait((update, context, media_data, lang))
        except asyncio.QueueFull:
            logger.warning(f"Queue full for user {user_id} (size={queue.qsize()})")
            return False

        # Update global counter
        await _inc_total_queued(1)

        # Start worker if not already running
        if user_id not in _user_workers or _user_workers[user_id].done():
            _user_workers[user_id] = asyncio.create_task(_user_worker(user_id))
            _user_last_active[user_id] = asyncio.get_event_loop().time()

        return True


async def _user_worker(user_id: int):
    """
    Background worker that processes a single user's queue sequentially.
    """
    logger.info(f"Worker started for user {user_id}")
    queue = _user_queues.get(user_id)
    if not queue:
        return

    try:
        while True:
            # Wait for item with timeout to allow idle cleanup
            try:
                task = await asyncio.wait_for(queue.get(), timeout=WORKER_IDLE_TIMEOUT)
            except asyncio.TimeoutError:
                # No activity for timeout period – worker will be cleaned up by idle cleaner
                continue

            # Update last active timestamp
            _user_last_active[user_id] = asyncio.get_event_loop().time()

            update, context, media_data, lang = task
            try:
                # Process the media (this is the original _process_single_media logic)
                await _process_single_media(update, context, media_data, lang)
            except Exception as e:
                logger.error(f"Worker for user {user_id} error processing media: {e}", exc_info=True)
            finally:
                queue.task_done()
                await _inc_total_queued(-1)  # Decrement global counter

    except asyncio.CancelledError:
        logger.info(f"Worker cancelled for user {user_id}")
    finally:
        # Cleanup when worker stops
        async with _user_dict_lock:
            _user_workers.pop(user_id, None)
            _user_queues.pop(user_id, None)
            _user_last_active.pop(user_id, None)
        logger.info(f"Worker stopped for user {user_id}")


async def _cleanup_idle_workers():
    """Periodically remove workers that have been idle too long."""
    while True:
        await asyncio.sleep(30)  # Check every 30 seconds
        now = asyncio.get_event_loop().time()
        async with _user_dict_lock:
            to_remove = [
                uid for uid, last in _user_last_active.items()
                if now - last > WORKER_IDLE_TIMEOUT and uid in _user_workers
            ]
            for uid in to_remove:
                worker = _user_workers.pop(uid, None)
                if worker and not worker.done():
                    worker.cancel()
                _user_queues.pop(uid, None)
                _user_last_active.pop(uid, None)
                logger.debug(f"Cleaned idle worker for user {uid}")


async def start_cleanup_task():
    """Start the background idle worker cleaner."""
    asyncio.create_task(_cleanup_idle_workers())
    logger.info("Per-user worker cleanup task started")


async def stop_all_workers():
    """Stop all user workers (call during bot shutdown)."""
    async with _user_dict_lock:
        for uid, worker in list(_user_workers.items()):
            if worker and not worker.done():
                worker.cancel()
        await asyncio.gather(*[_user_workers[uid] for uid in list(_user_workers.keys())], return_exceptions=True)
        _user_workers.clear()
        _user_queues.clear()
        _user_last_active.clear()
        global _total_queued_items
        _total_queued_items = 0
    logger.info("All per-user workers stopped")


# ============================================
# MESSAGE CLEANUP HELPER (existing)
# ============================================
async def _cleanup_notification_if_needed(context, chat_id, message_id):
    """
    Schedule deletion of notification/bot response messages
    only if DELETE_MEDIA_ONLY is False (clean everything mode).
    Media files are always cleaned regardless of this setting.
    """
    if not DELETE_MEDIA_ONLY:
        await cleaner.schedule_delete(
            context.bot, chat_id, message_id, delay=DELETE_DELAY_SECONDS
        )


# ============================================
# MAIN HANDLER (modified to use queue)
# ============================================
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all incoming media messages."""
    user_id = update.message.from_user.id

    # Register / update user profile
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    # Check ban status
    if await user_manager.is_banned(user_id):
        logger.info(f"Banned user {user_id} attempted upload")
        await cleaner.schedule_delete(
            context.bot, update.message.chat_id,
            update.message.message_id, delay=DELETE_DELAY_SECONDS,
        )
        return

    # Extract media metadata
    media_data = extract_media_data(update.message)
    if not media_data:
        return

    # Add owner
    media_data["owner_id"] = user_id

    # Validate type
    if not is_allowed_type(media_data["media_type"]):
        logger.debug(f"Rejected type from user {user_id}: {media_data['media_type']}")
        await cleaner.schedule_delete(
            context.bot, update.message.chat_id,
            update.message.message_id, delay=DELETE_DELAY_SECONDS,
        )
        return

    # Validate size
    if not is_within_size_limit(media_data["file_size"]):
        logger.info(f"Rejected oversized file ({media_data['file_size']} bytes) from user {user_id}")
        sent_msg = await update.message.reply_text(
            get_text("media.file_too_large", lang, 
                    size=media_data["file_size"],
                    max_mb=MAX_FILE_SIZE_MB),
            disable_notification=True
        )
        await cleaner.schedule_delete(
            context.bot, update.message.chat_id,
            update.message.message_id, delay=DELETE_DELAY_SECONDS,
        )
        await _cleanup_notification_if_needed(context, sent_msg.chat_id, sent_msg.message_id)
        return

    # Global cap check
    if MAX_FILES_TOTAL > 0:
        total_global = await MediaFile.get_total_count()
        if total_global >= MAX_FILES_TOTAL:
            logger.warning(f"Global storage full: {total_global}/{MAX_FILES_TOTAL}")
            sent_msg = await update.message.reply_text(
                get_text("media.global_full", lang),
                disable_notification=True
            )
            await cleaner.schedule_delete(
                context.bot, update.message.chat_id,
                update.message.message_id, delay=DELETE_DELAY_SECONDS,
            )
            await _cleanup_notification_if_needed(context, sent_msg.chat_id, sent_msg.message_id)
            return

    # Per-user quota check
    if not await user_manager.has_quota(user_id):
        sent_msg = await update.message.reply_text(
            get_text("media.quota_full", lang),
            disable_notification=True
        )
        await cleaner.schedule_delete(
            context.bot, update.message.chat_id,
            update.message.message_id, delay=DELETE_DELAY_SECONDS,
        )
        await _cleanup_notification_if_needed(context, sent_msg.chat_id, sent_msg.message_id)
        return

    # All validations passed – enqueue the media
    if update.message.media_group_id:
        # For media groups, we need to buffer the whole group before enqueueing
        await _handle_media_group(update, context, media_data, lang)
    else:
        success = await enqueue_media(user_id, update, context, media_data, lang)
        if not success:
            # Queue full or global limit reached
            sent_msg = await update.message.reply_text(
                get_text("media.queue_full", lang, maxsize=USER_QUEUE_MAXSIZE),
                disable_notification=True
            )
            await _cleanup_notification_if_needed(context, sent_msg.chat_id, sent_msg.message_id)
        # Always delete the original media message (configurable delay)
        await cleaner.schedule_delete(
            context.bot, update.message.chat_id,
            update.message.message_id, delay=DELETE_DELAY_SECONDS,
        )


# ============================================
# MEDIA GROUP HANDLING (modified to enqueue after buffer)
# ============================================
async def _handle_media_group(update, context, media_data, lang="id"):
    group_id = update.message.media_group_id

    # Store data in buffer with user_id
    group_buffer[group_id].append({
        "media_data": media_data,
        "update": update,
        "context": context,
        "lang": lang,
        "user_id": update.message.from_user.id,
    })

    new_token = object()
    group_tokens[group_id] = new_token

    asyncio.create_task(_process_group_after_delay(group_id, context, new_token))


async def _process_group_after_delay(group_id, context, token):
    try:
        await asyncio.sleep(GROUP_BUFFER_SECONDS)

        if group_tokens.get(group_id) is not token:
            logger.debug(f"Media group {group_id} processing skipped (newer timer exists)")
            return

        items = group_buffer.pop(group_id, [])
        if group_tokens.get(group_id) is token:
            group_tokens.pop(group_id, None)

        if not items:
            return

        logger.info(f"Processing media group {group_id}: {len(items)} files")

        chat_id = None
        for item in items:
            if chat_id is None:
                chat_id = item["update"].message.chat_id
            user_id = item["user_id"]
            # Enqueue each media in the group individually
            success = await enqueue_media(
                user_id=user_id,
                update=item["update"],
                context=item["context"],
                media_data=item["media_data"],
                lang=item["lang"]
            )
            if not success:
                # Queue full – notify user (only once per group)
                lang = item["lang"]
                sent_msg = await item["update"].message.reply_text(
                    get_text("media.queue_full", lang, maxsize=USER_QUEUE_MAXSIZE),
                    disable_notification=True
                )
                await _cleanup_notification_if_needed(item["context"], sent_msg.chat_id, sent_msg.message_id)

        # Schedule deletion of all original messages in the group
        message_ids = [item["update"].message.message_id for item in items]
        if message_ids and chat_id:
            await cleaner.delete_multiple(context.bot, chat_id, message_ids)

    except asyncio.CancelledError:
        logger.debug(f"Media group {group_id} processing cancelled by system")
    except Exception as exc:
        logger.error(f"Error processing media group {group_id}: {exc}", exc_info=True)


# ============================================
# SINGLE MEDIA PROCESSING (original logic, unchanged except removed commit duplications? No changes needed)
# ============================================
async def _process_single_media(update, context, media_data, lang="id") -> bool:
    """
    Process a single media file through the full pipeline.

    Pipeline:
    1. Fast filter (in-memory, read-only) — per-user isolation
    2. Deep check (database verification) — per-user isolation
    3. Database insert (if unique)
    4. Cache update (only after confirmation) — per-user isolation
    5. Statistics update
    """
    user_id = media_data["owner_id"]

    try:
        # Stage 1: Fast filter with per-user isolation
        is_dup_fast = await fast_filter.check(
            media_data["file_unique_id"],
            media_data["owner_id"],
            media_data["file_signature"],
        )
        if is_dup_fast:
            await DailyStats.increment(
                date.today(), user_id, "duplicates_rejected"
            )
            if not update.message.media_group_id:
                await cleaner.schedule_delete(
                    context.bot, update.message.chat_id,
                    update.message.message_id, delay=DELETE_DELAY_SECONDS,
                )
            return False

        # Stage 2: Deep check
        is_dup_deep = await deep_checker.is_duplicate(media_data)
        if is_dup_deep:
            fast_filter.add_to_cache(
                media_data["file_unique_id"],
                media_data["owner_id"],
                media_data["file_signature"],
            )
            await DailyStats.increment(
                date.today(), user_id, "duplicates_rejected"
            )
            if not update.message.media_group_id:
                await cleaner.schedule_delete(
                    context.bot, update.message.chat_id,
                    update.message.message_id, delay=DELETE_DELAY_SECONDS,
                )
            return False

        # Stage 3: Insert
        file_id = await MediaFile.insert(media_data)

        if file_id:
            fast_filter.add_to_cache(
                media_data["file_unique_id"],
                media_data["owner_id"],
                media_data["file_signature"],
            )
            await UserProfile.increment_file_stats(
                user_id, media_data["file_size"]
            )
            await DailyStats.increment(
                date.today(), user_id, "files_added"
            )

            # Track by media type using enum
            mt = media_data["media_type"]
            if mt == MediaType.PHOTO:
                await DailyStats.increment(
                    date.today(), user_id, "photos_added"
                )
            elif mt == MediaType.VIDEO:
                await DailyStats.increment(
                    date.today(), user_id, "videos_added"
                )
            elif mt == MediaType.DOCUMENT:
                await DailyStats.increment(
                    date.today(), user_id, "documents_added"
                )

            logger.info(
                "Saved for user %s: %s (ID: %s)",
                user_id,
                media_data.get("file_name", "unknown"),
                file_id
            )
        else:
            logger.warning(
                "DB insert skipped (constraint) for user %s: %s",
                user_id,
                media_data.get("file_unique_id", "?")
            )
            fast_filter.add_to_cache(
                media_data["file_unique_id"],
                media_data["owner_id"],
                media_data["file_signature"],
            )
            await DailyStats.increment(
                date.today(), user_id, "duplicates_rejected"
            )

        # Stage 4: Cleanup (only if not part of a group – groups handled separately)
        if not update.message.media_group_id:
            await cleaner.schedule_delete(
                context.bot, update.message.chat_id,
                update.message.message_id, delay=DELETE_DELAY_SECONDS,
            )

        return True

    except Exception as exc:
        logger.error(
            "Error processing media for user %s: %s",
            user_id, exc, exc_info=True
        )
        if not update.message.media_group_id:
            await cleaner.schedule_delete(
                context.bot, update.message.chat_id,
                update.message.message_id, delay=DELETE_DELAY_SECONDS,
            )
        return False