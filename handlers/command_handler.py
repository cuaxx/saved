"""
Telegram Media Storage Bot v3.0.5
User Command Handlers

Handles user-facing commands with multi-language support.
Includes compact file browser, navigation below media with numbered buttons + ✅ marker,
View Page, Prev/Next pages, and page jump via ForceReply.
"""

import hashlib
import logging
import random
import string
import time
from datetime import date
from html import escape
from typing import Dict, List, Optional, Tuple

from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    Update,
)
from telegram.ext import ContextTypes

from config import (
    DELETE_DELAY_SECONDS,
    DELETE_GET_DELAY_SECONDS,
    DELETE_GET_RESULTS,
    DELETE_MEDIA_ONLY,
    GET_DEFAULT_LIMIT,
    GET_MAX_RANGE,
    GET_SEND_AS_GROUP,
    USER_DEFAULT_FILE_LIMIT,
)
from database.models import DailyStats, MediaFile, UserProfile
from locales.loader import get_text, get_user_language
from middleware import is_admin, user_manager
from utils.cleaner import cleaner
from utils.delete_helper import safe_delete_message, safe_delete_update
from utils.helpers import format_bytes, parse_get_command

logger = logging.getLogger(__name__)

start_time = time.time()
ITEMS_PER_PAGE = 10

# ============================================
# CALLBACK DATA STORE (Fix for 64-byte limit)
# ============================================
_callback_store = {}

MAX_CALLBACK_STORE_SIZE = 10000
CALLBACK_STORE_TTL = 86400  # 24 hours in seconds
PROACTIVE_CLEANUP_INTERVAL = 100  # Cleanup every 100 stores

# Supported languages list (consistent with loader.py)
SUPPORTED_LANGS = {"id", "en", "ru", "zh", "ja", "es", "hi", "pt"}


def get_callback_store() -> dict:
    """Return reference to callback store for external cleaner."""
    return _callback_store


def _store_callback_data(data: dict) -> str:
    """Store callback data and return a short random key."""
    # Proactive cleanup
    if len(_callback_store) % PROACTIVE_CLEANUP_INTERVAL == 0:
        now = time.time()
        expired_keys = [
            k for k, v in _callback_store.items()
            if now - v.get("_created", 0) > CALLBACK_STORE_TTL
        ]
        for k in expired_keys:
            _callback_store.pop(k, None)
        if expired_keys:
            logger.debug("Proactive cleanup: removed %s expired entries", len(expired_keys))

    # Emergency cleanup
    if len(_callback_store) > MAX_CALLBACK_STORE_SIZE:
        now = time.time()
        expired_keys = [
            k for k, v in _callback_store.items()
            if now - v.get("_created", 0) > CALLBACK_STORE_TTL
        ]
        for k in expired_keys:
            _callback_store.pop(k, None)
        logger.debug("Emergency cleanup: removed %s expired entries", len(expired_keys))

    # Generate unique key
    for _ in range(100):
        short_key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if short_key not in _callback_store:
            break
    else:
        short_key = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:8]

    data["_created"] = time.time()
    _callback_store[short_key] = data
    return short_key


def _get_callback_data(key: str) -> Optional[dict]:
    """Retrieve and remove callback data by key."""
    data = _callback_store.pop(key, None)
    if data:
        if time.time() - data.get("_created", 0) > CALLBACK_STORE_TTL:
            return None
        data.pop("_created", None)
    return data


async def _get_user_language_fast(user_id: int) -> str:
    """Get user language quickly from database."""
    try:
        profile = await UserProfile.get(user_id)
        if profile and profile.get("language_code"):
            lang = profile["language_code"]
            if lang in SUPPORTED_LANGS:
                return lang
    except Exception:
        pass
    return "id"


# ============================================
# HELPER: Fetch files page (centralized)
# ============================================
async def _fetch_files_page(
    user_id: int,
    target_id: int,
    page: int,
    is_admin_user: bool,
    lang: str
) -> Tuple[List[Dict], int, str, bool, int]:
    """
    Fetch files for a specific page.

    Returns:
        Tuple of (files, total_pages, title, is_other_user, total_files)
    """
    # Case 1: Admin viewing specific user's files
    if is_admin_user and target_id != user_id and target_id != 0:
        total_files = await MediaFile.get_total_count(owner_id=target_id)
        total_pages = max(1, (total_files + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
        page = max(1, min(page, total_pages))
        start = (page - 1) * ITEMS_PER_PAGE + 1
        end = start + ITEMS_PER_PAGE - 1
        files = await MediaFile.get_range(start, end, target_id, max_range=ITEMS_PER_PAGE)
        profile = await UserProfile.get(target_id)
        owner_name = profile.get("first_name", "Unknown") if profile else "Unknown"
        title = get_text("nav.user_files", lang, name=owner_name, uid=target_id)
        if profile and profile.get("is_banned"):
            title += " 🚫 BANNED"
        is_other_user = True

    # Case 2: Admin viewing all files
    elif is_admin_user and (target_id == 0 or target_id == user_id):
        total_files = await MediaFile.get_total_count()
        total_pages = max(1, (total_files + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
        page = max(1, min(page, total_pages))
        start = (page - 1) * ITEMS_PER_PAGE + 1
        end = start + ITEMS_PER_PAGE - 1
        files = await MediaFile.get_range_all_users(start, end, max_range=ITEMS_PER_PAGE)
        title = get_text("nav.all_files", lang)
        is_other_user = False

    # Case 3: Regular user viewing own files
    else:
        total_files = await MediaFile.get_total_count(owner_id=user_id)
        total_pages = max(1, (total_files + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
        page = max(1, min(page, total_pages))
        start = (page - 1) * ITEMS_PER_PAGE + 1
        end = start + ITEMS_PER_PAGE - 1
        files = await MediaFile.get_range(start, end, user_id, max_range=ITEMS_PER_PAGE)
        title = get_text("nav.my_files", lang)
        is_other_user = False

    return files, total_pages, title, is_other_user, total_files


# ============================================
# BUILD LIST MESSAGE (Compact)
# ============================================
def _build_file_list_message(
    files: List[Dict],
    page: int,
    total_pages: int,
    total_files: int,
    title: str,
    lang: str = "id"
) -> str:
    """
    Build compact file list message — only header with range indicator.
    No file names or sizes are shown.
    """
    if total_files == 0:
        return f"{title}"#\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    start_pos = (page - 1) * ITEMS_PER_PAGE + 1
    end_pos = min(start_pos + len(files) - 1, total_files)

    range_text = get_text("nav.range_indicator", lang,
                          start=start_pos, end=end_pos, total=total_files)

    msg = f"{title} {range_text}\n"
  #  msg += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    return msg


# ============================================
# BUILD LIST KEYBOARD (for /get listing)
# ============================================
def _build_file_keyboard(
    page: int,
    total_pages: int,
    target_user_id: int,
    is_other_user: bool,
    files_count: int,
    lang: str = "id"
) -> InlineKeyboardMarkup:
    """Build file browser keyboard with short callback keys."""
    keyboard = []
    if files_count is None:
        files_count = ITEMS_PER_PAGE

    # Number buttons for each file
    start_num = (page - 1) * ITEMS_PER_PAGE + 1
    for row_start in range(0, files_count, 5):
        row = []
        for i in range(row_start, min(row_start + 5, files_count)):
            num = start_num + i
            key = _store_callback_data({
                "action": "file",
                "num": num,
                "target_id": target_user_id,
                "lang": lang
            })
            row.append(InlineKeyboardButton(str(num), callback_data=key))
        if row:
            keyboard.append(row)

    # View page button
    view_key = _store_callback_data({
        "action": "view",
        "page": page,
        "target_id": target_user_id,
        "lang": lang
    })
    keyboard.append([InlineKeyboardButton(
        get_text("nav.view_page", lang, page=page),
        callback_data=view_key
    )])

    # Navigation row: Prev | Page indicator | Next
    nav_row = []
    if page > 1:
        prev_key = _store_callback_data({
            "action": "nav",
            "page": page - 1,
            "target_id": target_user_id,
            "lang": lang
        })
        nav_row.append(InlineKeyboardButton(
            get_text("nav.prev", lang),
            callback_data=prev_key
        ))

    jump_key = _store_callback_data({
        "action": "jump",
        "page": page,
        "total_pages": total_pages,
        "target_id": target_user_id,
        "lang": lang
    })
    nav_row.append(InlineKeyboardButton(
        get_text("nav.page_of", lang, page=page, total=total_pages),
        callback_data=jump_key
    ))

    if page < total_pages:
        next_key = _store_callback_data({
            "action": "nav",
            "page": page + 1,
            "target_id": target_user_id,
            "lang": lang
        })
        nav_row.append(InlineKeyboardButton(
            get_text("nav.next", lang),
            callback_data=next_key
        ))
    keyboard.append(nav_row)

    # Back button for admin viewing other user's files
    if is_other_user:
        back_key = _store_callback_data({
            "action": "nav",
            "page": 1,
            "target_id": 0,
            "lang": lang
        })
        keyboard.append([InlineKeyboardButton(
            get_text("nav.back_all", lang),
            callback_data=back_key
        )])

    return InlineKeyboardMarkup(keyboard)


# ============================================
# NAVIGATION BELOW MEDIA
# ============================================
def _build_media_navigation_keyboard(
    current_num: int,
    total_files: int,
    target_id: int,
    lang: str,
    view_mode: bool = False,  # TAMBAHAN
    view_start: int = None,   # TAMBAHAN
    view_end: int = None      # TAMBAHAN
) -> InlineKeyboardMarkup:
    """
    Build navigation keyboard for media view.
    If view_mode=True, all numbers in the viewed range get ✅.
    """
    page = (current_num - 1) // ITEMS_PER_PAGE + 1
    total_pages = (total_files + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE if total_files > 0 else 1
    start = (page - 1) * ITEMS_PER_PAGE + 1
    end = min(start + ITEMS_PER_PAGE - 1, total_files)

    # Jika view_mode aktif, gunakan range view
    if view_mode and view_start and view_end:
        view_start = max(start, view_start)
        view_end = min(end, view_end)
    else:
        view_start = start
        view_end = end

    keyboard = []

    # Number buttons (5 per row)
    row = []
    for num in range(start, end + 1):
        # ✅ jika num dalam range yang di-view ATAU num == current_num
        if (view_mode and view_start <= num <= view_end) or num == current_num:
            label = f"{num}✅"
        else:
            label = str(num)

        key = _store_callback_data({
            "action": "nav_file",
            "num": num,
            "target_id": target_id,
            "lang": lang
        })
        row.append(InlineKeyboardButton(label, callback_data=key))
        if len(row) == 5:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # View Page button
    view_key = _store_callback_data({
        "action": "view_page_from_nav",
        "page": page,
        "target_id": target_id,
        "lang": lang
    })
    keyboard.append([InlineKeyboardButton(
        get_text("nav.view_page", lang, page=page),
        callback_data=view_key
    )])

    # Navigation row: Prev / 📄 page / Next
    nav_row = []
    if page > 1:
        prev_key = _store_callback_data({
            "action": "nav_page_from_media",
            "page": page - 1,
            "target_id": target_id,
            "lang": lang
        })
        nav_row.append(InlineKeyboardButton(
            get_text("nav.prev", lang),
            callback_data=prev_key
        ))

    jump_key = _store_callback_data({
        "action": "jump_page_from_media",
        "page": page,
        "total_pages": total_pages,
        "target_id": target_id,
        "lang": lang
    })
    nav_row.append(InlineKeyboardButton(
        f"📄 {page}/{total_pages}",
        callback_data=jump_key
    ))

    if page < total_pages:
        next_key = _store_callback_data({
            "action": "nav_page_from_media",
            "page": page + 1,
            "target_id": target_id,
            "lang": lang
        })
        nav_row.append(InlineKeyboardButton(
            get_text("nav.next", lang),
            callback_data=next_key
        ))

    keyboard.append(nav_row)

    return InlineKeyboardMarkup(keyboard)


async def _delete_previous_navigation(context: ContextTypes.DEFAULT_TYPE, bot, chat_id: int) -> None:
    """Delete previous navigation message if exists."""
    if context and context.user_data.get("nav_msg_id"):
        prev_id = context.user_data["nav_msg_id"]
        try:
            await bot.delete_message(chat_id=chat_id, message_id=prev_id)
        except Exception:
            pass  # Already deleted
        context.user_data.pop("nav_msg_id", None)


async def _send_navigation(
    bot,
    chat_id: int,
    current_num: int,
    total_files: int,
    target_id: int,
    lang: str,
    context: ContextTypes.DEFAULT_TYPE,
    view_mode: bool = False,
    view_start: int = None,
    view_end: int = None
) -> int:
    """
    Send navigation message below media with numbered keyboard and ✅ marker.
    Deletes any previous navigation message first.
    Returns message_id of the new navigation message.
    """
    if total_files <= 0:
        return 0

    await _delete_previous_navigation(context, bot, chat_id)

    reply_markup = _build_media_navigation_keyboard(
        current_num, total_files, target_id, lang,
        view_mode=view_mode,
        view_start=view_start,
        view_end=view_end
    )

    # ✅ PERBAIKAN: Tampilkan range jika view_mode aktif
    if view_mode and view_start is not None and view_end is not None:
        text = get_text("nav.navigation_hint_range", lang,
                        start=view_start, end=view_end, total=total_files)
    else:
        text = get_text("nav.navigation_hint", lang, num=current_num, total=total_files)

    nav_msg = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )

    context.user_data["nav_msg_id"] = nav_msg.message_id
    context.user_data["nav_chat_id"] = chat_id

    return nav_msg.message_id


# ============================================
# /start
# ============================================
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with welcome message."""
    user = update.message.from_user
    user_id = user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    if DELETE_MEDIA_ONLY:
        delete_desc = get_text("start.autodel_desc_media", lang, delay=DELETE_DELAY_SECONDS)
    else:
        delete_desc = get_text("start.autodel_desc_all", lang, delay=DELETE_DELAY_SECONDS)

    welcome_msg = (
        get_text("start.welcome", lang, name=user.first_name) + "\n\n" +
        get_text("start.bot_desc", lang) + "\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n" +
        get_text("start.features_title", lang) + "\n" +
        get_text("start.feature_save", lang) + "\n" +
        get_text("start.feature_dedup", lang) + "\n" +
        get_text("start.feature_privacy", lang) + "\n" +
        get_text("start.feature_autodel", lang, desc=delete_desc) + "\n" +
        get_text("start.feature_spoiler", lang) + "\n" +
        get_text("start.feature_album", lang) + "\n" +
        get_text("start.feature_forward", lang) + "\n" +
        get_text("start.feature_stats", lang) + "\n" +
        get_text("start.feature_delete", lang) + "\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n" +
        get_text("start.howto_title", lang) + "\n" +
        get_text("start.howto_desc", lang) + "\n\n" +
        get_text("start.commands_title", lang) + "\n" +
        get_text("start.cmd_get", lang) + "\n" +
        get_text("start.cmd_stats", lang) + "\n" +
        get_text("start.cmd_limit", lang) + "\n" +
        get_text("start.cmd_delete", lang) + "\n" +
        get_text("start.cmd_help", lang) + "\n" +
        get_text("start.cmd_lang", lang) + "\n" +
        get_text("start.cmd_admin_msg", lang) + "\n"
    )

    if await is_admin(user_id):
        welcome_msg += "\n" + get_text("start.admin_title", lang) + "\n" + get_text("start.admin_cmd", lang) + "\n"

    welcome_msg += "\n━━━━━━━━━━━━━━━━━━━━━━\n" + get_text("start.privacy_title", lang)

    try:
        await update.message.reply_text(welcome_msg, parse_mode="HTML", disable_notification=True)
    except Exception as exc:
        logger.error("Failed to send /start: %s", exc)

    await safe_delete_update(update, context, delay=5)


# ============================================
# /help
# ============================================
async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command with comprehensive guide."""
    user = update.message.from_user
    user_id = user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    help_msg = (
        get_text("help.title", lang) + "\n" +
        get_text("help.subtitle", lang) + "\n━━━━━━━━━━━━━━━━━━━━━━\n\n" +
        get_text("help.section1_title", lang) + "\n" +
        get_text("help.section1_desc", lang) + "\n" +
        get_text("help.section1_support", lang) + "\n" +
        get_text("help.section1_album", lang) + "\n" +
        get_text("help.section1_forward", lang) + "\n" +
        get_text("help.section1_duplicate", lang) + "\n" +
        get_text("help.section1_spoiler", lang) + "\n" +
        get_text("help.section1_delete", lang, delay=DELETE_DELAY_SECONDS) + "\n\n" +

        get_text("help.section2_title", lang) + "\n" +
        get_text("help.section2_intro", lang) + "\n\n" +
        get_text("help.section2_nav_title", lang) + "\n" +
        get_text("help.section2_nav1", lang) + "\n" +
        get_text("help.section2_nav2", lang) + "\n" +
        get_text("help.section2_nav3", lang) + "\n" +
        get_text("help.section2_nav4", lang) + "\n" +
        get_text("help.section2_nav5", lang) + "\n" +
        get_text("help.section2_nav6", lang) + "\n"
    )

    if await is_admin(user_id):
        help_msg += get_text("help.section2_admin", lang) + "\n"

    if DELETE_GET_RESULTS:
        help_msg += get_text("help.section2_delete", lang, delay=DELETE_GET_DELAY_SECONDS) + "\n"

    help_msg += (
        "\n" +
        get_text("help.section3_title", lang) + "\n" +
        get_text("help.section3_files", lang) + "\n" +
        get_text("help.section3_breakdown", lang) + "\n" +
        get_text("help.section3_today", lang) + "\n" +
        get_text("help.section3_uptime", lang) + "\n\n" +
        get_text("help.section4_title", lang) + "\n" +
        get_text("help.section4_default", lang, limit=USER_DEFAULT_FILE_LIMIT) + "\n" +
        get_text("help.section4_admin", lang) + "\n" +
        get_text("help.section4_unlimited", lang) + "\n\n" +
        get_text("help.section5_title", lang) + "\n" +
        get_text("help.section5_cmd", lang) + "\n" +
        get_text("help.section5_all", lang) + "\n" +
        get_text("help.section5_note", lang) + "\n\n" +
        get_text("help.section6_title", lang) + "\n" +
        get_text("help.section6_cmd", lang) + "\n" +
        get_text("help.section6_example", lang) + "\n" +
        get_text("help.section6_reply", lang) + "\n\n" +
        get_text("help.section7_title", lang) + "\n" +
        get_text("help.section7_private", lang) + "\n" +
        get_text("help.section7_noshare", lang) + "\n" +
        get_text("help.section7_clean", lang) + "\n" +
        get_text("help.section7_dedup", lang) + "\n\n" +
        get_text("help.section7_encryption", lang) + "\n\n" +
        get_text("help.section8_title", lang) + "\n" +
        get_text("help.section8_desc", lang) + "\n" +
        get_text("help.section8_list", lang) + "\n" +
        get_text("help.section8_set", lang) + "\n" +
        get_text("help.section8_langs", lang) + "\n\n" +
        get_text("help.section9_title", lang) + "\n" +
        get_text("help.section9_tip1", lang) + "\n" +
        get_text("help.section9_tip2", lang) + "\n" +
        get_text("help.section9_tip3", lang) + "\n" +
        get_text("help.section9_tip4", lang) + "\n"
    )

    if await is_admin(user_id):
        help_msg += (
            "\n" + get_text("help.admin_title", lang) + "\n━━━━━━━━━━━━━━━━━━━━━━\n" +
            get_text("help.admin_list", lang) + "\n" +
            get_text("help.admin_users", lang) + "\n" +
            get_text("help.admin_user", lang) + "\n" +
            get_text("help.admin_add", lang) + "\n" +
            get_text("help.admin_remove", lang) + "\n" +
            get_text("help.admin_setlimit", lang) + "\n" +
            get_text("help.admin_stats", lang) + "\n" +
            get_text("help.admin_messages", lang) + "\n" +
            get_text("help.admin_ban", lang) + "\n" +
            get_text("help.admin_unban", lang) + "\n" +
            get_text("help.admin_broadcast", lang) + "\n" +
            get_text("help.admin_reply", lang) + "\n" +
            get_text("help.admin_delete", lang) + "\n" +
            get_text("help.admin_get_user", lang) + "\n"
        )

    help_msg += "\n" + get_text("help.privacy_bottom", lang) + "\n"
    help_msg += "\n━━━━━━━━━━━━━━━━━━━━━━\n" + get_text("help.footer", lang) + "\n" + get_text("help.made_with", lang)

    try:
        await update.message.reply_text(help_msg, parse_mode="HTML")
    except Exception as exc:
        logger.error("Failed to send /help: %s", exc)

    await safe_delete_update(update, context, delay=15)


# ============================================
# /get — COMPACT FILE BROWSER
# ============================================
async def handle_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /get command with compact paginated file browser.
    Shows only range indicator and keyboard, no file names.
    """
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    if await user_manager.is_banned(user_id):
        await update.message.reply_text(get_text("get.banned", lang))
        return

    try:
        text = update.message.text.strip()
        is_admin_user = await is_admin(user_id)
        target_user_id = user_id
        page = 1

        # Parse command arguments
        parts = text.split()
        if is_admin_user and len(parts) >= 3 and parts[1] == "user":
            try:
                target_user_id = int(parts[2])
                if len(parts) >= 4:
                    page = int(parts[3])
            except ValueError:
                await update.message.reply_text(get_text("get.invalid_input", lang))
                await safe_delete_update(update, context, delay=5)
                return
        elif len(parts) >= 2:
            try:
                page = int(parts[1])
            except ValueError:
                page = 1

        files, total_pages, title, is_other_user, total_files = await _fetch_files_page(
            user_id=user_id,
            target_id=target_user_id,
            page=page,
            is_admin_user=is_admin_user,
            lang=lang
        )

        if not files:
            await update.message.reply_text(get_text("get.no_files", lang))
            await safe_delete_update(update, context, delay=5)
            return

        # Delete any leftover navigation from previous session
        await _delete_previous_navigation(context, context.bot, update.message.chat_id)

        file_list_msg = _build_file_list_message(files, page, total_pages, total_files, title, lang)
        keyboard = _build_file_keyboard(page, total_pages, target_user_id, is_other_user, len(files), lang)

        await update.message.reply_text(file_list_msg, reply_markup=keyboard)
        await DailyStats.increment(date.today(), user_id, "files_served", len(files))
        await safe_delete_update(update, context, delay=5)

    except Exception as exc:
        logger.error("Error in /get for user %s: %s", user_id, exc, exc_info=True)
        await update.message.reply_text(get_text("get.error", lang))


# ============================================
# NAVIGATE PAGE (list view)
# ============================================
async def _navigate_page(query, context, page, target_id, user_id, lang):
    """Navigate to a specific page in the file list."""
    is_admin_user = await is_admin(user_id)
    files, total_pages, title, is_other_user, total_files = await _fetch_files_page(
        user_id=user_id,
        target_id=target_id,
        page=page,
        is_admin_user=is_admin_user,
        lang=lang
    )

    if not files:
        await query.edit_message_text(get_text("get.no_files", lang))
        return

    file_list_msg = _build_file_list_message(files, page, total_pages, total_files, title, lang)
    keyboard = _build_file_keyboard(
        page, total_pages,
        target_id if target_id != 0 else user_id,
        is_other_user,
        len(files),
        lang
    )
    await query.edit_message_text(file_list_msg, reply_markup=keyboard)


# ============================================
# SEND SINGLE FILE (with navigation below)
# ============================================
async def _send_single_file(query, context, file_num, target_id, lang):
    """Send a single file and append navigation below it."""
    file_data = await MediaFile.get_by_position(file_num, target_id)
    if not file_data:
        await query.answer(get_text("nav.no_file", lang), show_alert=True)
        return

    file_data = dict(file_data)
    media_type = file_data["media_type"]

    try:
        sent_msg = None
        if media_type == "photo":
            sent_msg = await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=file_data["file_id"],
                has_spoiler=False
            )
        elif media_type == "video":
            sent_msg = await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=file_data["file_id"],
                supports_streaming=True,
                has_spoiler=False
            )
        elif media_type == "document":
            sent_msg = await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=file_data["file_id"]
            )

        if sent_msg:
            total_files = await MediaFile.get_total_count(owner_id=target_id)
            await _send_navigation(
                bot=context.bot,
                chat_id=query.message.chat_id,
                current_num=file_num,
                total_files=total_files,
                target_id=target_id,
                lang=lang,
                context=context
            )

            if DELETE_GET_RESULTS:
                await cleaner.schedule_delete_get_result(
                    context.bot, query.message.chat_id, sent_msg.message_id
                )

        await query.answer(get_text("nav.file_sent", lang, name=file_data.get("file_name") or media_type), show_alert=False)

    except Exception as exc:
        logger.error("Failed to send single file: %s", exc)
        await query.answer(get_text("nav.send_failed", lang), show_alert=True)


# ============================================
# DOWNLOAD PAGE (View Page from list)
# ============================================
async def _download_page(query, context, page, target_id, user_id, lang):
    """Download all files on the current page (from list view)."""
    start = (page - 1) * ITEMS_PER_PAGE + 1
    end = start + ITEMS_PER_PAGE - 1
    is_admin_user = await is_admin(user_id)

    if is_admin_user and target_id != user_id:
        files = await MediaFile.get_range(start, end, target_id, max_range=ITEMS_PER_PAGE)
    elif is_admin_user:
        files = await MediaFile.get_range_all_users(start, end, max_range=ITEMS_PER_PAGE)
    else:
        files = await MediaFile.get_range(start, end, user_id, max_range=ITEMS_PER_PAGE)

    if not files:
        await query.answer(get_text("nav.no_files_page", lang), show_alert=True)
        return

    sent_ids = []
    media_group = []

    for file_data in files:
        file_data = dict(file_data)
        media_type = file_data["media_type"]

        if media_type == "photo":
            media_group.append(InputMediaPhoto(media=file_data["file_id"], has_spoiler=False))
        elif media_type == "video":
            media_group.append(InputMediaVideo(media=file_data["file_id"], supports_streaming=True, has_spoiler=False))
        elif media_type == "document":
            try:
                sent_msg = await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=file_data["file_id"]
                )
                if sent_msg:
                    sent_ids.append(sent_msg.message_id)
            except Exception as exc:
                logger.error("Failed to send document: %s", exc)
            continue

        if len(media_group) == 10:
            try:
                msgs = await context.bot.send_media_group(
                    chat_id=query.message.chat_id,
                    media=media_group
                )
                sent_ids.extend(m.message_id for m in msgs)
            except Exception as exc:
                logger.error("Failed to send media group: %s", exc)
            media_group = []

    if media_group:
        try:
            msgs = await context.bot.send_media_group(
                chat_id=query.message.chat_id,
                media=media_group
            )
            sent_ids.extend(m.message_id for m in msgs)
        except Exception as exc:
            logger.error("Failed to send media group: %s", exc)

    # ✅ PERBAIKAN: Define last_num
    if files:
        total_files = await MediaFile.get_total_count(owner_id=target_id)
        first_num = start
        last_num = min(start + len(files) - 1, total_files)  # <-- TAMBAHKAN INI

        await _send_navigation(
            bot=context.bot,
            chat_id=query.message.chat_id,
            current_num=first_num,
            total_files=total_files,
            target_id=target_id,
            lang=lang,
            context=context,
            view_mode=True,
            view_start=first_num,
            view_end=last_num
        )

    if DELETE_GET_RESULTS and sent_ids:
        await cleaner.delete_multiple_get_results(context.bot, query.message.chat_id, sent_ids)

    await query.answer(get_text("nav.files_sent", lang, count=len(files)), show_alert=False)


# ============================================
# DOWNLOAD PAGE FROM MEDIA NAVIGATION
# ============================================
async def _download_page_from_media(query, context, page, target_id, lang):
    """Download all files on a page (called from media navigation)."""
    user_id = query.from_user.id
    is_admin_user = await is_admin(user_id)

    start = (page - 1) * ITEMS_PER_PAGE + 1
    end = start + ITEMS_PER_PAGE - 1

    if is_admin_user and target_id != user_id:
        files = await MediaFile.get_range(start, end, target_id, max_range=ITEMS_PER_PAGE)
    elif is_admin_user:
        files = await MediaFile.get_range_all_users(start, end, max_range=ITEMS_PER_PAGE)
    else:
        files = await MediaFile.get_range(start, end, user_id, max_range=ITEMS_PER_PAGE)

    if not files:
        await query.answer(get_text("nav.no_files_page", lang), show_alert=True)
        return

    sent_ids = []
    media_group = []

    for file_data in files:
        file_data = dict(file_data)
        media_type = file_data["media_type"]

        if media_type == "photo":
            media_group.append(InputMediaPhoto(media=file_data["file_id"], has_spoiler=False))
        elif media_type == "video":
            media_group.append(InputMediaVideo(media=file_data["file_id"], supports_streaming=True, has_spoiler=False))
        elif media_type == "document":
            try:
                sent_msg = await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=file_data["file_id"]
                )
                if sent_msg:
                    sent_ids.append(sent_msg.message_id)
            except Exception as exc:
                logger.error("Failed to send document: %s", exc)
            continue

        if len(media_group) == 10:
            try:
                msgs = await context.bot.send_media_group(
                    chat_id=query.message.chat_id,
                    media=media_group
                )
                sent_ids.extend(m.message_id for m in msgs)
            except Exception as exc:
                logger.error("Failed to send media group: %s", exc)
            media_group = []

    if media_group:
        try:
            msgs = await context.bot.send_media_group(
                chat_id=query.message.chat_id,
                media=media_group
            )
            sent_ids.extend(m.message_id for m in msgs)
        except Exception as exc:
            logger.error("Failed to send media group: %s", exc)

    # ✅ PERBAIKAN: Define last_num
    if files:
        total_files = await MediaFile.get_total_count(owner_id=target_id)
        first_num = start
        last_num = min(start + len(files) - 1, total_files)  # <-- TAMBAHKAN INI

        await _send_navigation(
            bot=context.bot,
            chat_id=query.message.chat_id,
            current_num=first_num,
            total_files=total_files,
            target_id=target_id,
            lang=lang,
            context=context,
            view_mode=True,
            view_start=first_num,
            view_end=last_num
        )

    if DELETE_GET_RESULTS and sent_ids:
        await cleaner.delete_multiple_get_results(context.bot, query.message.chat_id, sent_ids)

    await query.answer(get_text("nav.files_sent", lang, count=len(files)), show_alert=False)


# ============================================
# SHOW JUMP INPUT (ForceReply for page jump)
# ============================================
async def _show_jump_input(query, context, page, total_pages, target_id, user_id):
    """Show prompt for page jump (ForceReply)."""
    lang = await get_user_language_from_query(query)

    context.user_data["awaiting_jump_reply"] = True
    context.user_data["jump_target_id"] = target_id
    context.user_data["jump_total_pages"] = total_pages

    prompt = await query.message.reply_text(
        get_text("nav.jump_prompt", lang, total=total_pages),
        reply_markup=ForceReply(selective=True)
    )
    context.user_data["jump_prompt_msg_id"] = prompt.message_id
    await query.answer(get_text("nav.jump_alert", lang, total=total_pages), show_alert=True)


async def get_user_language_from_query(query) -> str:
    """Extract user language from callback query."""
    from locales.loader import DEFAULT_LANGUAGE

    user = query.from_user
    if user is None:
        return DEFAULT_LANGUAGE

    profile = await UserProfile.get(user.id)
    if profile and profile.get("language_code"):
        lang = profile["language_code"]
        if lang in SUPPORTED_LANGS:
            return lang

    lang = user.language_code
    if lang and lang in SUPPORTED_LANGS:
        return lang

    return DEFAULT_LANGUAGE


# ============================================
# PAGE JUMP REPLY HANDLER (handles both list and media jump)
# ============================================
async def handle_page_jump_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle page jump reply from ForceReply (both list and media)."""
    user_id = update.message.from_user.id
    lang = await get_user_language(update)

    # First check: jump to a specific page (from list view)
    if context.user_data.get("awaiting_jump_reply"):
        context.user_data.pop("awaiting_jump_reply", None)
        try:
            page = int(update.message.text.strip())
        except ValueError:
            await update.message.reply_text(get_text("nav.invalid_number", lang))
            return

        target_id = context.user_data.get("jump_target_id", user_id)
        total_pages = context.user_data.get("jump_total_pages", 1)

        if page < 1 or page > total_pages:
            await update.message.reply_text(get_text("nav.invalid_page", lang, total=total_pages))
            return

        is_admin_user = await is_admin(user_id)
        files, total_pages, title, is_other_user, total_files = await _fetch_files_page(
            user_id, target_id, page, is_admin_user, lang
        )
        if not files:
            await update.message.reply_text(get_text("get.no_files", lang))
            return

        file_list_msg = _build_file_list_message(files, page, total_pages, total_files, title, lang)
        keyboard = _build_file_keyboard(page, total_pages, target_id, is_other_user, len(files), lang)
        await update.message.reply_text(file_list_msg, reply_markup=keyboard)

        await safe_delete_update(update, context, delay=3)
        context.user_data.pop("jump_target_id", None)
        context.user_data.pop("jump_total_pages", None)
        context.user_data.pop("jump_prompt_msg_id", None)
        return

    # Second check: jump to a specific file (from media navigation)
    if context.user_data.get("awaiting_jump_file"):
        context.user_data.pop("awaiting_jump_file", None)
        try:
            file_num = int(update.message.text.strip())
        except ValueError:
            await update.message.reply_text(get_text("nav.invalid_number", lang))
            return

        target_id = context.user_data.get("jump_file_target_id", user_id)
        total_files = context.user_data.get("jump_file_total", 0)

        if file_num < 1 or file_num > total_files:
            await update.message.reply_text(get_text("nav.invalid_file", lang, total=total_files))
            return

        # Send the requested file with navigation
        await _send_file_direct(
            bot=context.bot,
            chat_id=update.message.chat_id,
            file_num=file_num,
            target_id=target_id,
            lang=lang,
            context=context
        )

        await safe_delete_update(update, context, delay=3)
        context.user_data.pop("jump_file_target_id", None)
        context.user_data.pop("jump_file_total", None)
        context.user_data.pop("jump_file_prompt_msg_id", None)
        return


# ============================================
# SEND FILE DIRECT (for jump file without callback)
# ============================================
async def _send_file_direct(bot, chat_id: int, file_num: int, target_id: int, lang: str, context: ContextTypes.DEFAULT_TYPE):
    """Send a file directly (without callback query) for jump file."""
    file_data = await MediaFile.get_by_position(file_num, target_id)
    if not file_data:
        await bot.send_message(chat_id=chat_id, text=get_text("nav.no_file", lang))
        return

    file_data = dict(file_data)
    media_type = file_data["media_type"]

    try:
        sent_msg = None
        if media_type == "photo":
            sent_msg = await bot.send_photo(
                chat_id=chat_id,
                photo=file_data["file_id"],
                has_spoiler=False
            )
        elif media_type == "video":
            sent_msg = await bot.send_video(
                chat_id=chat_id,
                video=file_data["file_id"],
                supports_streaming=True,
                has_spoiler=False
            )
        elif media_type == "document":
            sent_msg = await bot.send_document(
                chat_id=chat_id,
                document=file_data["file_id"]
            )

        if sent_msg:
            total_files = await MediaFile.get_total_count(owner_id=target_id)
            await _send_navigation(
                bot=bot,
                chat_id=chat_id,
                current_num=file_num,
                total_files=total_files,
                target_id=target_id,
                lang=lang,
                context=context
            )
            if DELETE_GET_RESULTS:
                await cleaner.schedule_delete_get_result(bot, chat_id, sent_msg.message_id)

    except Exception as exc:
        logger.error("Failed to send file directly: %s", exc)
        await bot.send_message(chat_id=chat_id, text=get_text("nav.send_failed", lang))


# ============================================
# CALLBACK HANDLER (main dispatcher)
# ============================================
async def handle_get_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle all file browser callback queries.
    Supports: navigation, file send, view page, jump, and media navigation.
    """
    query = update.callback_query
    user_id = query.from_user.id
    short_key = query.data
    user_lang = await _get_user_language_fast(user_id)

    # Rate limit check
    from utils.user_rate_limiter import callback_rate_limiter
    if not callback_rate_limiter.is_allowed(user_id, operation="callback"):
        await query.answer("⚠️ " + get_text("nav.too_fast", user_lang), show_alert=True)
        return

    data = _get_callback_data(short_key)
    if not data:
        await query.answer("⚠️ " + get_text("nav.session_expired", user_lang), show_alert=True)
        return

    action = data.get("action")
    lang = data.get("lang", user_lang)

    try:
        if action == "nav":
            # Navigate to a different page in the list
            await _navigate_page(
                query, context, data["page"], data["target_id"], user_id, lang
            )
            await query.answer()

        elif action == "file":
            # Send a single file (from list view)
            await _send_single_file(
                query, context, data["num"], data["target_id"], lang
            )
            # query.answer is called inside _send_single_file

        elif action == "view":
            # Download all files on the current page (from list view)
            await _download_page(
                query, context, data["page"], data["target_id"], user_id, lang
            )
            # query.answer is called inside

        elif action == "jump":
            # Show ForceReply for page jump (from list view)
            await _show_jump_input(
                query, context, data["page"], data["total_pages"],
                data["target_id"], user_id
            )
            # query.answer is called inside

        elif action == "nav_file":
            # Navigate to a specific file (from media navigation keyboard)
            new_num = data.get("num")
            target_id = data.get("target_id")
            await _send_single_file(query, context, new_num, target_id, lang)

        elif action == "view_page_from_nav":
            # View Page from media navigation
            page = data.get("page")
            target_id = data.get("target_id")
            await _download_page_from_media(query, context, page, target_id, lang)

        elif action == "nav_page_from_media":
            # Prev/Next page from media navigation -> show list view of that page
            page = data.get("page")
            target_id = data.get("target_id")
            await _navigate_page(query, context, page, target_id, user_id, lang)
            await query.answer()

        elif action == "jump_page_from_media":
            # Jump to a different page from media navigation
            page = data.get("page")
            total_pages = data.get("total_pages")
            target_id = data.get("target_id")
            # Store context for jump reply
            context.user_data["awaiting_jump_reply"] = True
            context.user_data["jump_target_id"] = target_id
            context.user_data["jump_total_pages"] = total_pages
            # Also store that we came from media navigation so we return to media after jump
            context.user_data["jump_from_media"] = True

            prompt = await query.message.reply_text(
                get_text("nav.jump_prompt", lang, total=total_pages),
                reply_markup=ForceReply(selective=True)
            )
            context.user_data["jump_prompt_msg_id"] = prompt.message_id
            await query.answer(get_text("nav.jump_alert", lang, total=total_pages), show_alert=True)

        elif action == "back_to_list":
            # Back to list (kept for compatibility, but not used in new design)
            target_id = data.get("target_id")
            await _navigate_page(query, context, 1, target_id, user_id, lang)
            await query.answer()

        else:
            await query.answer(get_text("nav.generic_error", lang))

    except Exception as exc:
        logger.error("Error in get callback: %s", exc, exc_info=True)
        await query.answer(get_text("nav.generic_error", lang))


# ============================================
# /stats
# ============================================
async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command with personal statistics."""
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    try:
        total_files = await MediaFile.get_total_count(owner_id=user_id)
        total_size = await MediaFile.get_total_size(owner_id=user_id)
        type_stats = await MediaFile.get_count_by_type(owner_id=user_id)
        recent_stats = await DailyStats.get_stats(user_id, 7)
        today_added = sum(s["files_added"] for s in recent_stats[:1])
        today_dup = sum(s["duplicates_rejected"] for s in recent_stats[:1])

        uptime_seconds = int(time.time() - start_time)
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60

        profile = await UserProfile.get(user_id)
        limit = profile.get("max_files_limit", USER_DEFAULT_FILE_LIMIT) if profile else USER_DEFAULT_FILE_LIMIT

        stats_msg = get_text("stats.title", lang) + "\n━━━━━━━━━━━━━━━━━━\n\n"
        stats_msg += get_text("stats.total_files", lang, count=total_files)
        if limit > 0:
            stats_msg += get_text("stats.quota", lang, limit=limit)
        stats_msg += "\n" + get_text("stats.total_size", lang, size=format_bytes(total_size)) + "\n\n"
        stats_msg += get_text("stats.by_type", lang) + "\n"

        for mtype, data in type_stats.items():
            emoji_key = f"stats.type_{mtype}" if mtype in ["photo", "video", "document"] else "stats.type_other"
            stats_msg += "  " + get_text(emoji_key, lang, type=mtype, count=data["count"], size=format_bytes(data["size"])) + "\n"

        stats_msg += "\n" + get_text("stats.today_added", lang, count=today_added) + "\n"
        stats_msg += get_text("stats.today_dup", lang, count=today_dup) + "\n"

        await update.message.reply_text(stats_msg)
        await safe_delete_update(update, context, delay=5)

    except Exception as exc:
        logger.error("Error in /stats: %s", exc, exc_info=True)


# ============================================
# /mylimit
# ============================================
async def handle_mylimit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mylimit command to check file quota."""
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    try:
        remaining = await user_manager.get_remaining_quota(user_id)
        profile = await UserProfile.get(user_id)
        limit = profile.get("max_files_limit", USER_DEFAULT_FILE_LIMIT) if profile else USER_DEFAULT_FILE_LIMIT
        current = await MediaFile.get_total_count(owner_id=user_id)
        size = format_bytes(await MediaFile.get_total_size(owner_id=user_id))

        if limit <= 0:
            await update.message.reply_text(
                get_text("limit.unlimited", lang, current=current, size=size)
            )
        else:
            await update.message.reply_text(
                get_text("limit.limited", lang, current=current, limit=limit, remaining=remaining, size=size)
            )

        await safe_delete_update(update, context, delay=5)

    except Exception as exc:
        logger.error("Error in /mylimit: %s", exc, exc_info=True)


# ============================================
# /language
# ============================================
async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /language command with inline keyboard."""
    from locales.loader import SUPPORTED_LANGUAGES

    user = update.message.from_user
    user_id = user.id
    await user_manager.ensure_user_exists(update)

    current_lang = await get_user_language(update)
    current_name = SUPPORTED_LANGUAGES.get(current_lang, "Unknown")

    keyboard = []
    lang_entries = list(SUPPORTED_LANGUAGES.items())

    for i in range(0, len(lang_entries), 2):
        row = []
        for code, name in lang_entries[i:i+2]:
            emoji = name.split()[0]
            label = f"{emoji} {name.split(' ', 1)[1] if ' ' in name else name}"
            if code == current_lang:
                label = f"✅ {label}"
            row.append(InlineKeyboardButton(label, callback_data=f"lang:{code}"))
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(
        f"📌 {current_name}",
        callback_data="ignore"
    )])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text("language.select_title", current_lang),
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    await safe_delete_update(update, context, delay=5)


async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection callback."""
    query = update.callback_query
    data = query.data

    if data == "ignore":
        await query.answer()
        return

    if data.startswith("lang:"):
        from locales.loader import set_user_language, SUPPORTED_LANGUAGES

        lang_code = data.split(":")[1]
        user_id = query.from_user.id

        current_lang = await _get_user_language_fast(user_id)
        if lang_code == current_lang:
            await query.answer(get_text("language.already_set", current_lang), show_alert=True)
            return

        if lang_code in SUPPORTED_LANGUAGES:
            success = await set_user_language(user_id, lang_code)
            if success:
                new_name = SUPPORTED_LANGUAGES[lang_code]

                keyboard = []
                lang_entries = list(SUPPORTED_LANGUAGES.items())
                for i in range(0, len(lang_entries), 2):
                    row = []
                    for code, name in lang_entries[i:i+2]:
                        emoji = name.split()[0]
                        label = f"{emoji} {name.split(' ', 1)[1] if ' ' in name else name}"
                        if code == lang_code:
                            label = f"✅ {label}"
                        row.append(InlineKeyboardButton(label, callback_data=f"lang:{code}"))
                    keyboard.append(row)

                keyboard.append([InlineKeyboardButton(
                    f"📌 {new_name}",
                    callback_data="ignore"
                )])

                await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
                await query.answer(
                    get_text("language.changed", lang_code, name=new_name),
                    show_alert=True
                )
        else:
            await query.answer(
                get_text("language.unsupported", lang_code),
                show_alert=True
            )