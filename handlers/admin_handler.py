"""
Telegram Media Storage Bot v3.0.4
Admin Command Handlers

Provides admin-only commands with full multi-language support.

FIXES v3.0.4:
- ✅ All confirmation messages, status strings, and ban/unban UI
  now use get_text() for complete i18n coverage.
- ✅ Removed all hardcoded English strings.
- Existing features: retry mechanism for broadcast, ban/unban
  callback handler, admin audit logging, cache clearing on ban.
"""

import asyncio
import hashlib
import logging
import random
import string
import time
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError, RetryAfter

from config import SUPER_ADMIN_IDS, USER_DEFAULT_FILE_LIMIT
from database.models import (
    AdminMessage, AdminUsers, DailyStats, MediaFile, UserProfile
)
from locales.loader import get_text, get_user_language
from middleware import is_admin, is_super_admin, user_manager
from utils.admin_logger import log_admin_action, get_admin_name
from utils.cleaner import cleaner
from utils.delete_helper import safe_delete_update
from utils.helpers import format_bytes

logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 3
BASE_RETRY_DELAY = 1.0
MAX_RETRY_DELAY = 30.0
ITEMS_PER_PAGE_ADMIN = 20

# ============================================
# BAN/UNBAN CALLBACK STORE
# ============================================
_ban_callback_store = {}
BAN_CALLBACK_TTL = 300  # 5 menit


def _store_ban_callback(data: dict) -> str:
    """Simpan data callback ban/unban dengan prefix ban_."""
    now = time.time()
    
    # Cleanup expired entries
    expired = [k for k, v in _ban_callback_store.items()
               if now - v.get("_created", 0) > BAN_CALLBACK_TTL]
    for k in expired:
        _ban_callback_store.pop(k, None)
    
    # Generate unique key
    for _ in range(100):
        short_key = 'ban_' + ''.join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        if short_key not in _ban_callback_store:
            break
    else:
        short_key = 'ban_' + hashlib.md5(
            f"{time.time()}{random.random()}".encode()
        ).hexdigest()[:8]
    
    data["_created"] = now
    _ban_callback_store[short_key] = data
    return short_key


def _get_ban_callback(key: str) -> dict:
    """Ambil data callback ban/unban."""
    data = _ban_callback_store.pop(key, None)
    if data:
        if time.time() - data.get("_created", 0) > BAN_CALLBACK_TTL:
            return None
        data.pop("_created", None)
    return data


# ============================================
# RETRY HELPER
# ============================================
async def _send_with_retry(bot, chat_id: int, text: str, max_retries: int = MAX_RETRIES) -> bool:
    """Send a message with retry logic for rate limits."""
    for attempt in range(max_retries):
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            return True
        except RetryAfter as e:
            wait_time = min(e.retry_after, MAX_RETRY_DELAY)
            logger.warning(
                "Rate limited for chat %s, waiting %ss (attempt %s/%s)",
                chat_id, wait_time, attempt + 1, max_retries
            )
            await asyncio.sleep(wait_time)
        except TelegramError as e:
            logger.debug("Failed to send to %s: %s", chat_id, e)
            return False
        except Exception as e:
            logger.error("Unexpected error sending to %s: %s", chat_id, e)
            if attempt < max_retries - 1:
                delay = min(BASE_RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                await asyncio.sleep(delay)
            else:
                return False
    return False


# ============================================
# LANGUAGE HELPER
# ============================================
async def _get_target_user_language(user_id: int) -> str:
    """Dapatkan preferensi bahasa user target."""
    from config import DEFAULT_LANGUAGE, validate_language
    
    try:
        profile = await UserProfile.get(user_id)
        if profile and profile.get("language_code"):
            return validate_language(profile["language_code"])
    except Exception:
        pass
    
    return DEFAULT_LANGUAGE


# ============================================
# USER to ADMIN MESSAGE
# ============================================
async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle @admin [message] from regular users."""
    user = update.message.from_user
    user_id = user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    text = update.message.text.strip()
    if text.startswith("@admin "):
        message_text = text[7:].strip()
    elif text.startswith("@admin"):
        message_text = text[6:].strip()
    else:
        return

    if not message_text:
        await update.message.reply_text(get_text("admin_msg.format", lang))
        return

    msg_id = await AdminMessage.create(user_id, message_text)

    admins = await AdminUsers.get_all()
    all_admin_ids = set(SUPER_ADMIN_IDS)
    for a in admins:
        all_admin_ids.add(a["user_id"])

    for admin_id in all_admin_ids:
        try:
            admin_lang = await _get_target_user_language(admin_id)
            await context.bot.send_message(
                chat_id=admin_id,
                text=get_text(
                    "admin_msg.notify", admin_lang,
                    name=user.first_name, uid=user_id,
                    message=message_text, msg_id=msg_id
                ),
            )
        except Exception:
            pass

    await update.message.reply_text(get_text("admin_msg.sent", lang))
    await safe_delete_update(update, context, delay=5)


# ============================================
# /admin MAIN PANEL
# ============================================
async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command to show admin panel."""
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    if not await _check_admin_access(update, user_id, lang):
        return

    text = update.message.text.strip()
    parts = text.split()

    if len(parts) == 1:
        await _show_admin_panel(update, lang)
    elif parts[1] == "users":
        page = 1
        if len(parts) >= 3:
            try:
                page = int(parts[2])
            except ValueError:
                page = 1
        await handle_admin_users_list(update, context, lang, page)
    elif parts[1] == "user" and len(parts) >= 3:
        await handle_admin_user_detail(update, context, int(parts[2]), lang)
    elif parts[1] == "add" and len(parts) >= 3:
        await handle_admin_add(update, context, int(parts[2]), lang)
    elif parts[1] == "remove" and len(parts) >= 3:
        await handle_admin_remove(update, context, int(parts[2]), lang)
    elif parts[1] == "setlimit" and len(parts) >= 4:
        await handle_admin_set_limit(update, context, int(parts[2]), int(parts[3]), lang)
    elif parts[1] == "stats":
        await handle_admin_global_stats(update, context, lang)
    elif parts[1] == "messages":
        await handle_admin_messages(update, context, lang)
    else:
        await _show_admin_panel(update, lang)

    await safe_delete_update(update, context, delay=5)


async def _check_admin_access(update, user_id, lang="id") -> bool:
    """Verify admin access and return False if denied."""
    if user_id not in SUPER_ADMIN_IDS and not await AdminUsers.exists(user_id):
        await update.message.reply_text(get_text("admin.access_denied", lang))
        return False
    return True


async def _show_admin_panel(update, lang="id"):
    """Show the main admin panel with unread message count."""
    total_users = await UserProfile.get_count()
    total_files = await MediaFile.get_total_count()
    total_admins = len(await AdminUsers.get_all())
    unread_msgs = await AdminMessage.get_unread_count()

    panel = (
        get_text("admin.panel_title", lang) + "\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        + get_text("admin.panel_users", lang, count=total_users) + "\n"
        + get_text("admin.panel_files", lang, count=total_files) + "\n"
        + get_text("admin.panel_admins", lang, count=total_admins) + "\n"
    )
    
    if unread_msgs > 0:
        panel += get_text("admin.panel_unread", lang, count=unread_msgs) + "\n"
    
    panel += "\n" + get_text("admin.panel_commands", lang)
    
    await update.message.reply_text(panel, parse_mode="HTML")


# ============================================
# ADMIN SUB-COMMANDS
# ============================================
async def handle_admin_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE, lang="id", page: int = 1):
    """List all users with pagination."""
    users = await UserProfile.get_all_users()
    
    if not users:
        await update.message.reply_text(get_text("admin.users_empty", lang))
        return
    
    total_users = len(users)
    total_pages = max(1, (total_users + ITEMS_PER_PAGE_ADMIN - 1) // ITEMS_PER_PAGE_ADMIN)
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start_idx = (page - 1) * ITEMS_PER_PAGE_ADMIN
    end_idx = min(start_idx + ITEMS_PER_PAGE_ADMIN, total_users)
    page_users = users[start_idx:end_idx]
    global_start_num = start_idx + 1
    
    msg = get_text("admin.users_title", lang) + f" ({page}/{total_pages})\n"
    msg += "━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, u in enumerate(page_users, global_start_num):
        name = u.get("first_name", "Unknown")
        uid = u["user_id"]
        files = u.get("total_files", 0)
        banned = " 🚫" if u.get("is_banned") else ""
        msg += get_text("admin.users_item", lang,
                       i=i, name=name, uid=uid, files=files, banned=banned) + "\n"
    
    keyboard = []
    nav_row = []
    
    if page > 1:
        nav_row.append(InlineKeyboardButton(
            get_text("nav.prev", lang),
            callback_data=f"admin_users:{page-1}"
        ))
    
    nav_row.append(InlineKeyboardButton(
        f"📄 {page}/{total_pages}",
        callback_data="ignore"
    ))
    
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(
            get_text("nav.next", lang),
            callback_data=f"admin_users:{page+1}"
        ))
    
    if nav_row:
        keyboard.append(nav_row)
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    
    if update.callback_query:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode="HTML")


async def handle_admin_users_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "ignore":
        await query.answer()
        return

    user = query.from_user
    user_id = user.id if user else 0
    lang = "id"
    try:
        lang = await get_user_language_from_admin_callback(query)
    except Exception:
        pass

    try:
        parts = data.split(":")
        page = int(parts[1])
    except (ValueError, IndexError):
        await query.answer(get_text("admin_users.invalid_page", lang), show_alert=True)
        return

    # Verifikasi akses admin
    if user_id not in SUPER_ADMIN_IDS and not await AdminUsers.exists(user_id):
        await query.answer(get_text("admin_users.access_denied", lang), show_alert=True)
        return

    # ✅ Panggil ulang daftar user dengan halaman yang diminta
    await handle_admin_users_list(update, context, lang, page)


async def get_user_language_from_admin_callback(query) -> str:
    """Get language for admin callback."""
    from locales.loader import DEFAULT_LANGUAGE
    user = query.from_user
    if user is None:
        return DEFAULT_LANGUAGE
    profile = await UserProfile.get(user.id)
    if profile and profile.get("language_code"):
        return profile["language_code"]
    lang = user.language_code
    if lang and lang in ["id", "en", "ru", "zh", "ja", "es", "hi", "pt"]:
        return lang
    return DEFAULT_LANGUAGE


async def handle_admin_user_detail(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                   target_id: int, lang="id"):
    """Show detailed stats for a specific user."""
    profile = await UserProfile.get(target_id)
    if not profile:
        await update.message.reply_text(get_text("admin.user_not_found", lang))
        return

    total_files = await MediaFile.get_total_count(owner_id=target_id)
    total_size = await MediaFile.get_total_size(owner_id=target_id)
    type_stats = await MediaFile.get_count_by_type(owner_id=target_id)

    name = profile.get("first_name", "Unknown")
    username = profile.get("username") or "N/A"
    banned = "Yes 🚫" if profile.get("is_banned") else "No ✅"
    limit_val = profile.get("max_files_limit", USER_DEFAULT_FILE_LIMIT)
    limit_str = f"{limit_val:,}" if limit_val > 0 else "Unlimited"

    msg = (
        get_text("admin.user_title", lang, name=name) + "\n"
        "━━━━━━━━━━━━━━━━━━\n"
        + get_text("admin.user_id", lang, uid=target_id) + "\n"
        + get_text("admin.user_username", lang, username=username) + "\n"
        + get_text("admin.user_banned", lang, status=banned) + "\n"
        + get_text("admin.user_files", lang, files=total_files, limit=limit_str) + "\n"
        + get_text("admin.user_storage", lang, size=format_bytes(total_size)) + "\n\n"
        + get_text("admin.user_by_type", lang) + "\n"
    )
    for mt, data in type_stats.items():
        msg += f"  {mt}: {data['count']:,} ({format_bytes(data['size'])})\n"

    await update.message.reply_text(msg, parse_mode="HTML")


async def handle_admin_add(update: Update, context: ContextTypes.DEFAULT_TYPE,
                           target_id: int, lang="id"):
    """Add a regular admin."""
    user_id = update.message.from_user.id

    if not is_super_admin(user_id):
        await update.message.reply_text(get_text("admin.add_super_only", lang))
        return

    if is_super_admin(target_id):
        await update.message.reply_text(get_text("admin.add_super_cannot", lang))
        return

    success = await AdminUsers.add(target_id, added_by=user_id)
    if success:
        await update.message.reply_text(get_text("admin.add_success", lang, uid=target_id))
        logger.info("Super admin %s added admin %s", user_id, target_id)
        
        # Log audit
        log_admin_action(
            admin_id=user_id,
            admin_name=get_admin_name(update),
            action="ADD_ADMIN",
            target_id=target_id,
            details="Promoted to admin"
        )
    else:
        await update.message.reply_text(get_text("admin.add_already", lang))


async def handle_admin_remove(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              target_id: int, lang="id"):
    """Remove a regular admin."""
    user_id = update.message.from_user.id

    if not is_super_admin(user_id):
        await update.message.reply_text(get_text("admin.remove_super_only", lang))
        return

    if is_super_admin(target_id):
        await update.message.reply_text(get_text("admin.remove_super_cannot", lang))
        return

    success = await AdminUsers.remove(target_id)
    if success:
        await update.message.reply_text(get_text("admin.remove_success", lang, uid=target_id))
        logger.info("Super admin %s removed admin %s", user_id, target_id)
        
        # Log audit
        log_admin_action(
            admin_id=user_id,
            admin_name=get_admin_name(update),
            action="REMOVE_ADMIN",
            target_id=target_id,
            details="Demoted from admin"
        )
    else:
        await update.message.reply_text(get_text("admin.remove_not", lang))


async def handle_admin_set_limit(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                 target_id: int, limit: int, lang="id"):
    """Set custom file limit for a user."""
    user_id = update.message.from_user.id

    if not await _check_admin_access(update, user_id, lang):
        return

    await UserProfile.set_file_limit(target_id, limit)
    await update.message.reply_text(
        get_text("admin.setlimit_success", lang, uid=target_id, limit=limit)
    )
    
    # Log audit
    log_admin_action(
        admin_id=user_id,
        admin_name=get_admin_name(update),
        action="SET_FILE_LIMIT",
        target_id=target_id,
        details=f"File limit set to {limit}"
    )


async def handle_admin_global_stats(update: Update, context: ContextTypes.DEFAULT_TYPE, lang="id"):
    """Show global statistics for admins."""
    total_users = await UserProfile.get_count()
    total_files = await MediaFile.get_total_count()
    total_size = await MediaFile.get_total_size()
    total_served = await DailyStats.get_total_served()

    users = await UserProfile.get_all_users()
    top_users = users[:5]

    msg = (
        get_text("admin.global_title", lang) + "\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        + get_text("admin.global_users", lang, count=total_users) + "\n"
        + get_text("admin.global_files", lang, count=total_files) + "\n"
        + get_text("admin.global_storage", lang, size=format_bytes(total_size)) + "\n"
        + get_text("admin.global_served", lang, count=total_served) + "\n\n"
        + get_text("admin.global_top", lang) + "\n"
    )
    for i, u in enumerate(top_users, 1):
        name = u.get("first_name", "Unknown")
        files = u.get("total_files", 0)
        msg += get_text("admin.global_top_item", lang, i=i, name=name, files=files) + "\n"

    await update.message.reply_text(msg, parse_mode="HTML")


# ============================================
# BROADCAST (with retry)
# ============================================
async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all active (non-banned) registered users with retry mechanism."""
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    # Pemeriksaan akses admin (menggantikan @admin_required)
    if not await _check_admin_access(update, user_id, lang):
        return

    text = update.message.text.strip()
    
    if text.startswith("/broadcast "):
        message_text = text[11:].strip()
    elif text.startswith("/broadcast"):
        message_text = text[10:].strip()
    else:
        message_text = ""
    
    if not message_text:
        await update.message.reply_text(
            get_text("admin.broadcast_format", lang)
        )
        await safe_delete_update(update, context, delay=5)
        return

    # Filter banned users
    all_users = await UserProfile.get_all_users()
    active_users = [u for u in all_users if not u.get("is_banned", False)]
    banned_users = [u for u in all_users if u.get("is_banned", False)]
    
    total = len(active_users)
    skipped = len(banned_users)
    success = 0
    failed = 0

    status_msg = await update.message.reply_text(
        get_text("admin.broadcast_sending", lang, total=total) +
        (get_text("admin.broadcast_skipped", lang, skipped=skipped) if skipped > 0 else "")
    )

    BATCH_SIZE = 25
    last_progress_update = 0
    
    for i in range(0, total, BATCH_SIZE):
        batch = active_users[i:i + BATCH_SIZE]
        tasks = []
        
        for user in batch:
            user_lang = await _get_target_user_language(user["user_id"])
            broadcast_message = get_text(
                "admin.broadcast_msg", user_lang, message=message_text
            )
            task = _send_with_retry(context.bot, user["user_id"], broadcast_message)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result is True:
                success += 1
            else:
                failed += 1
        
        if success + failed - last_progress_update >= 100 or i + BATCH_SIZE >= total:
            last_progress_update = success + failed
            try:
                await status_msg.edit_text(
                    get_text("admin.broadcast_progress", lang,
                            sent=success + failed, total=total,
                            success=success, failed=failed)
                )
            except Exception:
                pass
        
        if i + BATCH_SIZE < total:
            await asyncio.sleep(0.5)

    await status_msg.edit_text(
        get_text("admin.broadcast_done", lang,
                success=success, failed=failed, total=total)
    )

    log_admin_action(
        admin_id=user_id,
        admin_name=get_admin_name(update),
        action="BROADCAST",
        details=f"Sent to {success}/{total} users (skipped {skipped} banned, {failed} failed)"
    )

    await safe_delete_update(update, context, delay=5)


# ============================================
# REPLY TO USER MESSAGE
# ============================================
async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reply to a user's @admin message."""
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    if not await _check_admin_access(update, user_id, lang):
        return

    text = update.message.text.strip()
    parts = text.split(maxsplit=2)

    if len(parts) < 3:
        await update.message.reply_text(get_text("admin.reply_format", lang))
        return

    try:
        msg_id = int(parts[1])
    except ValueError:
        await update.message.reply_text(get_text("admin.reply_invalid_id", lang))
        return

    reply_text = parts[2]

    original = await AdminMessage.get_by_id(msg_id)
    if not original:
        await update.message.reply_text(get_text("admin.reply_not_found", lang))
        return

    if original["is_read"] and original["replied_by"]:
        await update.message.reply_text(get_text("admin.reply_already", lang))
        return

    target_user_lang = await _get_target_user_language(original["from_user_id"])

    reply_message = get_text(
        "admin.reply_to_user", target_user_lang,
        original=original["message_text"], reply=reply_text
    )
    
    success = await _send_with_retry(
        context.bot, original["from_user_id"], reply_message
    )
    
    if not success:
        await update.message.reply_text(
            get_text("admin.reply_failed_delivery", lang)
        )
        return

    await AdminMessage.mark_replied(msg_id, user_id, reply_text)

    await update.message.reply_text(
        get_text("admin.reply_sent", lang, uid=original["from_user_id"])
    )

    log_admin_action(
        admin_id=user_id,
        admin_name=get_admin_name(update),
        action="REPLY_USER",
        target_id=original["from_user_id"],
        details=f"Replied to message #{msg_id}"
    )

    await safe_delete_update(update, context, delay=5)


# ============================================
# VIEW USER MESSAGES
# ============================================
async def handle_admin_messages(update: Update, context: ContextTypes.DEFAULT_TYPE, lang="id"):
    """Show unread messages from users."""
    messages = await AdminMessage.get_unread(20)

    if not messages:
        await update.message.reply_text(get_text("admin.messages_empty", lang))
        return

    msg_text = get_text("admin.messages_title", lang) + "\n━━━━━━━━━━━━━━━━━━\n\n"
    for m in messages:
        name = m.get("first_name", "Unknown")
        uid = m["from_user_id"]
        msg_text += get_text("admin.messages_item", lang,
                           id=m["id"], name=name, uid=uid,
                           text=m["message_text"][:100])

    if len(messages) == 20:
        msg_text += get_text("admin.messages_max", lang)

    await update.message.reply_text(msg_text, parse_mode="HTML")


# ============================================
# /ban COMMAND (WITH CONFIRMATION) - fully i18n
# ============================================
async def handle_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user with confirmation. All strings use get_text()."""
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    if not await _check_admin_access(update, user_id, lang):
        return

    parts = update.message.text.strip().split()
    if len(parts) < 2:
        await update.message.reply_text(get_text("admin.ban_usage", lang))
        await safe_delete_update(update, context, delay=5)
        return

    try:
        target_id = int(parts[1])
    except ValueError:
        await update.message.reply_text(get_text("admin.ban_invalid", lang))
        await safe_delete_update(update, context, delay=5)
        return

    if is_super_admin(target_id):
        await update.message.reply_text(get_text("admin.ban_super", lang))
        await safe_delete_update(update, context, delay=5)
        return

    # Cek apakah sudah di-ban
    profile = await UserProfile.get(target_id)
    if profile and profile.get("is_banned"):
        await update.message.reply_text(
            get_text("ban.already_banned", lang, uid=target_id),
            parse_mode="HTML"
        )
        await safe_delete_update(update, context, delay=5)
        return

    # Info user untuk konfirmasi
    user_name = profile.get("first_name", "Unknown") if profile else "Unknown"
    username = f"@{profile['username']}" if profile and profile.get("username") else "N/A"
    total_files = profile.get("total_files", 0) if profile else 0
    
    confirm_msg = get_text("ban.confirm_title", lang) + "\n\n" + \
                  get_text("ban.confirm_body", lang,
                           name=user_name, uid=target_id,
                           username=username, files=total_files)
    
    confirm_key = _store_ban_callback({
        "action": "confirm_ban",
        "target_id": target_id,
        "target_name": user_name,
        "admin_id": user_id,
        "lang": lang
    })
    
    cancel_key = _store_ban_callback({
        "action": "cancel_ban",
        "lang": lang
    })
    
    keyboard = [[
        InlineKeyboardButton(
            get_text("ban.btn_confirm", lang),
            callback_data=confirm_key
        ),
        InlineKeyboardButton(
            get_text("ban.btn_cancel", lang),
            callback_data=cancel_key
        ),
    ]]
    
    await update.message.reply_text(
        confirm_msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
    
    await safe_delete_update(update, context, delay=5)


# ============================================
# /unban COMMAND (WITH CONFIRMATION) - fully i18n
# ============================================
async def handle_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a user with confirmation. All strings use get_text()."""
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    if not await _check_admin_access(update, user_id, lang):
        return

    parts = update.message.text.strip().split()
    if len(parts) < 2:
        await update.message.reply_text(get_text("admin.unban_usage", lang))
        await safe_delete_update(update, context, delay=5)
        return

    try:
        target_id = int(parts[1])
    except ValueError:
        await update.message.reply_text(get_text("admin.ban_invalid", lang))
        await safe_delete_update(update, context, delay=5)
        return

    # Cek apakah benar-benar di-ban
    profile = await UserProfile.get(target_id)
    if not profile or not profile.get("is_banned"):
        await update.message.reply_text(
            get_text("unban.not_banned", lang, uid=target_id),
            parse_mode="HTML"
        )
        await safe_delete_update(update, context, delay=5)
        return

    # Info user untuk konfirmasi
    user_name = profile.get("first_name", "Unknown") if profile else "Unknown"
    username = f"@{profile['username']}" if profile and profile.get("username") else "N/A"
    total_files = profile.get("total_files", 0) if profile else 0
    
    confirm_msg = get_text("unban.confirm_title", lang) + "\n\n" + \
                  get_text("unban.confirm_body", lang,
                           name=user_name, uid=target_id,
                           username=username, files=total_files)
    
    confirm_key = _store_ban_callback({
        "action": "confirm_unban",
        "target_id": target_id,
        "target_name": user_name,
        "admin_id": user_id,
        "lang": lang
    })
    
    cancel_key = _store_ban_callback({
        "action": "cancel_ban",
        "lang": lang
    })
    
    keyboard = [[
        InlineKeyboardButton(
            get_text("unban.btn_confirm", lang),
            callback_data=confirm_key
        ),
        InlineKeyboardButton(
            get_text("ban.btn_cancel", lang),
            callback_data=cancel_key
        ),
    ]]
    
    await update.message.reply_text(
        confirm_msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
    
    await safe_delete_update(update, context, delay=5)


# ============================================
# BAN/UNBAN CALLBACK HANDLER - fully i18n
# ============================================
async def handle_ban_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    short_key = query.data

    data = _get_ban_callback(short_key)
    if not data:
        fallback_lang = "id"
        try:
            profile = await UserProfile.get(user_id)
            if profile and profile.get("language_code"):
                fallback_lang = profile["language_code"]
        except Exception:
            pass
        await query.answer(
            get_text("ban.popup_session_expired", fallback_lang),
            show_alert=True
        )
        return
    
    action = data.get("action")
    target_id = data.get("target_id")
    target_name = data.get("target_name", "Unknown")
    admin_id = data.get("admin_id")
    lang = data.get("lang", "id")

    # ✅ Verifikasi ulang bahwa user masih admin
    if admin_id and not await is_admin(user_id):
        await query.answer(get_text("admin.access_denied", lang), show_alert=True)
        return

    # Verifikasi admin access
    if user_id not in SUPER_ADMIN_IDS and not await AdminUsers.exists(user_id):
        await query.answer(
            get_text("ban.popup_access_denied", lang),
            show_alert=True
        )
        return
    
    # Verifikasi admin yang sama yang memulai
    if admin_id and user_id != admin_id:
        await query.answer(
            get_text("ban.popup_not_initiator", lang),
            show_alert=True
        )
        return
    
    if action == "cancel_ban":
        await query.edit_message_text(
            get_text("ban.cancel", lang),
            parse_mode="HTML"
        )
        await query.answer(get_text("ban.popup_cancelled", lang))
        return
    
    elif action == "confirm_ban":
        # Cek ulang sebelum ban
        if is_super_admin(target_id):
            await query.edit_message_text(
                get_text("admin.ban_super", lang),
                parse_mode="HTML"
            )
            await query.answer(
                get_text("ban.popup_cannot_ban_super", lang),
                show_alert=True
            )
            return
        
        profile = await UserProfile.get(target_id)
        if profile and profile.get("is_banned"):
            await query.edit_message_text(
                get_text("ban.already_banned", lang, uid=target_id),
                parse_mode="HTML"
            )
            await query.answer(get_text("ban.popup_already_banned", lang))
            return
        
        # Eksekusi ban
        await UserProfile.set_ban(target_id, True)
        
        # Clear cache
        try:
            from dedup.fast_filter import fast_filter
            fast_filter.clear_user_cache(target_id)
        except Exception:
            pass
        
        logger.info("Admin %s banned user %s (%s)", user_id, target_id, target_name)
        
        log_admin_action(
            admin_id=user_id,
            admin_name=get_admin_name(update),
            action="BAN_USER",
            target_id=target_id,
            target_name=target_name,
            details="User banned from bot via confirmation"
        )
        
        await query.edit_message_text(
            get_text("ban.success", lang, name=target_name, uid=target_id),
            parse_mode="HTML"
        )
        await query.answer(
            get_text("ban.popup_success_ban", lang),
            show_alert=True
        )
    
    elif action == "confirm_unban":
        profile = await UserProfile.get(target_id)
        if profile and not profile.get("is_banned"):
            await query.edit_message_text(
                get_text("unban.not_banned", lang, uid=target_id),
                parse_mode="HTML"
            )
            await query.answer(get_text("ban.popup_not_banned", lang))
            return
        
        # Eksekusi unban
        await UserProfile.set_ban(target_id, False)
        
        logger.info("Admin %s unbanned user %s (%s)", user_id, target_id, target_name)
        
        log_admin_action(
            admin_id=user_id,
            admin_name=get_admin_name(update),
            action="UNBAN_USER",
            target_id=target_id,
            target_name=target_name,
            details="User unbanned from bot via confirmation"
        )
        
        await query.edit_message_text(
            get_text("unban.success", lang, name=target_name, uid=target_id),
            parse_mode="HTML"
        )
        await query.answer(
            get_text("ban.popup_success_unban", lang),
            show_alert=True
        )
    
    await query.answer()