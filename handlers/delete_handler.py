"""
Telegram Media Storage Bot v3.0.3
Delete File Handler

Memungkinkan user menghapus file mereka sendiri
dengan konfirmasi inline keyboard untuk mencegah
penghapusan tidak sengaja.

FIXES v3.0.3:
- Delete single file dengan konfirmasi
- Delete all files dengan konfirmasi
- Admin dapat menghapus file user lain
- Membersihkan cache deduplikasi setelah hapus
- Callback pattern: del_XXXXXXXX
- Fixed: parse_mode="HTML" untuk semua pesan
- Fixed: DELETE_MEDIA_ONLY respected via safe_delete_update
- ✅ Added daily stats update after file deletion
- ✅ Added admin audit logging for all delete actions
- ✅ Proper cache clearing with FastFilter.clear_user_cache()
"""

import hashlib
import logging
import random
import string
import time
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database.connection import db
from database.models import MediaFile, UserProfile
from dedup.fast_filter import fast_filter
from locales.loader import get_text, get_user_language
from middleware import is_admin, user_manager
from utils.admin_logger import log_admin_action
from utils.cleaner import cleaner
from utils.delete_helper import safe_delete_update
from utils.helpers import format_bytes

logger = logging.getLogger(__name__)

# ============================================
# DELETE CALLBACK STORE
# ============================================
_delete_callback_store = {}
DELETE_CALLBACK_TTL = 3600  # 1 jam


def _store_delete_callback(data: dict) -> str:
    """
    Simpan data callback hapus dengan prefix del_.
    
    Membersihkan entri expired secara otomatis
    sebelum menyimpan data baru.
    
    Args:
        data: Dictionary berisi data callback
        
    Returns:
        Short key string dengan prefix 'del_'
    """
    now = time.time()
    
    # Cleanup expired entries
    expired = [k for k, v in _delete_callback_store.items()
               if now - v.get("_created", 0) > DELETE_CALLBACK_TTL]
    for k in expired:
        _delete_callback_store.pop(k, None)
    
    # Generate unique key dengan retry
    for _ in range(100):
        short_key = 'del_' + ''.join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        if short_key not in _delete_callback_store:
            break
    else:
        # Fallback: gunakan hash jika semua random key terpakai
        short_key = 'del_' + hashlib.md5(
            f"{time.time()}{random.random()}".encode()
        ).hexdigest()[:8]
    
    data["_created"] = now
    _delete_callback_store[short_key] = data
    return short_key


def _get_delete_callback(key: str) -> dict:
    """
    Ambil data callback hapus berdasarkan key.
    
    Data akan dihapus dari store setelah diambil
    (one-time use callback).
    
    Args:
        key: Short callback key
        
    Returns:
        Dictionary data callback atau None jika expired/tidak ditemukan
    """
    data = _delete_callback_store.pop(key, None)
    if data:
        # Check TTL
        if time.time() - data.get("_created", 0) > DELETE_CALLBACK_TTL:
            return None
        data.pop("_created", None)  # Clean up internal field
    return data


# ============================================
# /delete COMMAND
# ============================================
async def handle_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /delete command.
    
    Mendukung:
    - /delete [nomor]  : Hapus file tertentu (1 = terbaru)
    - /delete all       : Hapus semua file
    - /delete user [id] [nomor|all] : Admin hapus file user lain
    
    ✅ v3.0.3: DELETE_MEDIA_ONLY respected via safe_delete_update
    """
    user_id = update.message.from_user.id
    await user_manager.ensure_user_exists(update)
    lang = await get_user_language(update)

    # Cek banned
    if await user_manager.is_banned(user_id):
        await update.message.reply_text(
            get_text("delete.banned", lang),
            parse_mode="HTML"
        )
        return

    text = update.message.text.strip()
    parts = text.split()

    # Hanya /delete (tampilkan bantuan)
    if len(parts) == 1:
        await _show_delete_help(update, user_id, lang)
        await safe_delete_update(update, context, delay=5)
        return

    # Admin menghapus file user lain: /delete user [id] [nomor|all]
    if len(parts) >= 3 and parts[1] == "user" and await is_admin(user_id):
        try:
            target_id = int(parts[2])
            if len(parts) >= 4:
                if parts[3].lower() == "all":
                    await _confirm_delete_all(update, target_id, lang, admin_id=user_id)
                else:
                    await _confirm_delete_single(update, target_id, int(parts[3]), lang, admin_id=user_id)
            else:
                await _show_delete_help(update, target_id, lang, is_admin_view=True)
        except ValueError:
            await update.message.reply_text(
                get_text("delete.invalid_format", lang),
                parse_mode="HTML"
            )
        await safe_delete_update(update, context, delay=5)
        return

    # Hapus semua file: /delete all
    if parts[1].lower() == "all":
        await _confirm_delete_all(update, user_id, lang)
        await safe_delete_update(update, context, delay=5)
        return

    # Hapus file tertentu: /delete [nomor]
    try:
        await _confirm_delete_single(update, user_id, int(parts[1]), lang)
    except ValueError:
        await update.message.reply_text(
            get_text("delete.invalid_format", lang),
            parse_mode="HTML"
        )

    await safe_delete_update(update, context, delay=5)


async def _show_delete_help(update, user_id, lang, is_admin_view=False):
    """
    Tampilkan panduan penggunaan /delete.
    
    Args:
        update: Telegram Update object
        user_id: User ID yang dicek
        lang: Kode bahasa
        is_admin_view: True jika admin melihat file user lain
    """
    total_files = await MediaFile.get_total_count(owner_id=user_id)
    total_size = await MediaFile.get_total_size(owner_id=user_id)
    
    if is_admin_view:
        profile = await UserProfile.get(user_id)
        user_name = profile.get("first_name", "Unknown") if profile else "Unknown"
        msg = get_text("delete.help_admin", lang,
                      uid=user_id, name=user_name,
                      count=total_files, size=format_bytes(total_size))
    else:
        msg = (
            get_text("delete.help_title", lang) + "\n\n" +
            get_text("delete.help_desc", lang) + "\n\n" +
            get_text("delete.help_commands", lang) + "\n" +
            get_text("delete.help_single", lang) + "\n" +
            get_text("delete.help_all", lang) + "\n\n" +
            get_text("delete.help_note", lang) + "\n\n" +
            get_text("delete.help_total", lang, count=total_files) + "\n" +
            get_text("delete.help_size", lang, size=format_bytes(total_size))
        )
    
    await update.message.reply_text(msg, parse_mode="HTML")


async def _confirm_delete_single(update, user_id, file_num, lang, admin_id=None):
    """
    Tampilkan konfirmasi hapus satu file dengan inline keyboard.
    
    Args:
        update: Telegram Update object
        user_id: User ID pemilik file
        file_num: Nomor file (1 = terbaru)
        lang: Kode bahasa
        admin_id: Admin ID jika admin yang menghapus (None untuk user biasa)
    """
    # Cari file berdasarkan posisi
    file_data = await MediaFile.get_by_position(file_num, user_id)
    
    if not file_data:
        await update.message.reply_text(
            get_text("delete.not_found", lang, num=file_num),
            parse_mode="HTML"
        )
        return
    
    file_data = dict(file_data)
    file_name = file_data.get("file_name") or f"{file_data['media_type']}_{file_data['id']}"
    file_size = format_bytes(file_data["file_size"])
    file_type = file_data["media_type"]
    
    # Emoji berdasarkan tipe file
    emoji_map = {"photo": "📸", "video": "🎥", "document": "📄"}
    emoji = emoji_map.get(file_type, "📎")
    
    # Pesan konfirmasi berbeda untuk admin
    if admin_id:
        confirm_msg = get_text(
            "delete.confirm_single_admin", lang,
            num=file_num, emoji=emoji, name=file_name,
            type=file_type, size=file_size, uid=user_id
        )
    else:
        confirm_msg = get_text(
            "delete.confirm_single", lang,
            num=file_num, emoji=emoji, name=file_name,
            type=file_type, size=file_size
        )
    
    # Simpan data untuk callback konfirmasi
    confirm_key = _store_delete_callback({
        "action": "confirm_single",
        "file_id": file_data["id"],
        "file_unique_id": file_data["file_unique_id"],
        "file_signature": file_data.get("file_signature", ""),
        "file_num": file_num,
        "file_name": file_name,
        "file_size": file_data["file_size"],
        "file_type": file_type,
        "owner_id": user_id,
        "admin_id": admin_id,
        "lang": lang
    })
    
    cancel_key = _store_delete_callback({
        "action": "cancel",
        "lang": lang
    })
    
    # Inline keyboard konfirmasi
    keyboard = [[
        InlineKeyboardButton(
            get_text("delete.btn_confirm", lang),
            callback_data=confirm_key
        ),
        InlineKeyboardButton(
            get_text("delete.btn_cancel", lang),
            callback_data=cancel_key
        ),
    ]]
    
    await update.message.reply_text(
        confirm_msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


async def _confirm_delete_all(update, user_id, lang, admin_id=None):
    """
    Tampilkan konfirmasi hapus semua file dengan inline keyboard.
    
    Args:
        update: Telegram Update object
        user_id: User ID pemilik file
        lang: Kode bahasa
        admin_id: Admin ID jika admin yang menghapus (None untuk user biasa)
    """
    total_files = await MediaFile.get_total_count(owner_id=user_id)
    total_size = await MediaFile.get_total_size(owner_id=user_id)
    
    if total_files == 0:
        await update.message.reply_text(
            get_text("delete.no_files", lang),
            parse_mode="HTML"
        )
        return
    
    # Pesan konfirmasi berbeda untuk admin
    if admin_id:
        profile = await UserProfile.get(user_id)
        user_name = profile.get("first_name", "Unknown") if profile else "Unknown"
        confirm_msg = get_text(
            "delete.confirm_all_admin", lang,
            count=total_files, size=format_bytes(total_size),
            uid=user_id, name=user_name
        )
    else:
        confirm_msg = get_text(
            "delete.confirm_all", lang,
            count=total_files, size=format_bytes(total_size)
        )
    
    # Simpan data untuk callback konfirmasi
    confirm_key = _store_delete_callback({
        "action": "confirm_all",
        "owner_id": user_id,
        "admin_id": admin_id,
        "total_files": total_files,
        "total_size": total_size,
        "lang": lang
    })
    
    cancel_key = _store_delete_callback({
        "action": "cancel",
        "lang": lang
    })
    
    # Inline keyboard konfirmasi
    keyboard = [[
        InlineKeyboardButton(
            get_text("delete.btn_confirm_all", lang),
            callback_data=confirm_key
        ),
        InlineKeyboardButton(
            get_text("delete.btn_cancel", lang),
            callback_data=cancel_key
        ),
    ]]
    
    await update.message.reply_text(
        confirm_msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


# ============================================
# DELETE CALLBACK HANDLER
# ============================================
async def handle_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle semua callback delete (pattern: del_XXXXXXXX).
    
    Memproses:
    - Konfirmasi hapus single file
    - Konfirmasi hapus semua file
    - Pembatalan hapus
    """
    query = update.callback_query
    user_id = query.from_user.id
    short_key = query.data
    
    # Ambil data callback
    data = _get_delete_callback(short_key)
    if not data:
        # Fallback language jika data tidak tersedia
        fallback_lang = "id"
        try:
            profile = await UserProfile.get(user_id)
            if profile and profile.get("language_code"):
                fallback_lang = profile["language_code"]
        except Exception:
            pass
        await query.answer(
            get_text("delete.popup_session_expired", fallback_lang),
            show_alert=True
        )
        return
    
    action = data.get("action")
    lang = data.get("lang", "id")
    
    if action == "cancel":
        # User membatalkan penghapusan
        await query.edit_message_text(
            get_text("delete.cancelled", lang),
            parse_mode="HTML"
        )
    
    elif action == "confirm_single":
        # User mengkonfirmasi hapus single file
        await _execute_delete_single(query, data, user_id, lang)
    
    elif action == "confirm_all":
        # User mengkonfirmasi hapus semua file
        await _execute_delete_all(query, data, user_id, lang)
    
    await query.answer()


async def _execute_delete_single(query, data, user_id, lang):
    file_id = data["file_id"]
    file_name = data["file_name"]
    file_num = data["file_num"]
    file_size = data["file_size"]
    file_type = data.get("file_type", "unknown")
    owner_id = data["owner_id"]
    admin_id = data.get("admin_id")

    # ✅ Verifikasi ulang status admin (jika admin yang menghapus)
    if admin_id and not await is_admin(user_id):
        await query.edit_message_text(
            get_text("admin.access_denied", lang),
            parse_mode="HTML"
        )
        return

    # === Verifikasi kepemilikan atau hak admin ===
    if admin_id:
        if user_id != admin_id:
            await query.edit_message_text(
                get_text("delete.not_admin", lang),
                parse_mode="HTML"
            )
            return
    else:
        if user_id != owner_id:
            await query.edit_message_text(
                get_text("delete.not_owner", lang),
                parse_mode="HTML"
            )
            return

    try:
        # === Dapatkan info file sebelum dihapus ===
        file_row = await db.fetchone(
            "SELECT media_type, DATE(created_at) as created_date FROM media_files WHERE id = ? AND owner_id = ?",
            (file_id, owner_id)
        )
        if not file_row:
            # File sudah tidak ada, batalkan (mungkin dihapus bersamaan)
            await query.edit_message_text(
                get_text("delete.not_found", lang, num=file_num),
                parse_mode="HTML"
            )
            return
        media_type = file_row["media_type"]
        created_date = file_row["created_date"]  # string 'YYYY-MM-DD'

        # === Hapus file dari database ===
        await db.execute(
            "DELETE FROM media_files WHERE id = ? AND owner_id = ?",
            (file_id, owner_id)
        )

        # === Update counter di tabel users ===
        await db.execute("""
            UPDATE users 
            SET total_files = MAX(0, total_files - 1),
                total_size = MAX(0, total_size - ?),
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (file_size, owner_id))

        # === Update daily statistics ===
        try:
            await db.execute("""
                UPDATE daily_stats 
                SET files_added = MAX(0, files_added - 1),
                    total_size_bytes = MAX(0, total_size_bytes - ?)
                WHERE owner_id = ? AND stat_date = ?
            """, (file_size, owner_id, created_date))

            if media_type == "photo":
                await db.execute(
                    "UPDATE daily_stats SET photos_added = MAX(0, photos_added - 1) "
                    "WHERE owner_id = ? AND stat_date = ?",
                    (owner_id, created_date)
                )
            elif media_type == "video":
                await db.execute(
                    "UPDATE daily_stats SET videos_added = MAX(0, videos_added - 1) "
                    "WHERE owner_id = ? AND stat_date = ?",
                    (owner_id, created_date)
                )
            elif media_type == "document":
                await db.execute(
                    "UPDATE daily_stats SET documents_added = MAX(0, documents_added - 1) "
                    "WHERE owner_id = ? AND stat_date = ?",
                    (owner_id, created_date)
                )
        except Exception as stats_err:
            logger.warning("Failed to update daily stats after delete: %s", stats_err)

        await db.commit()

        # === Clear cache deduplikasi ===
        try:
            fast_filter.clear_user_cache(owner_id)
        except Exception as cache_err:
            logger.warning("Failed to clear cache after delete: %s", cache_err)

        logger.info(
            "File deleted: id=%s, owner=%s, name=%s, size=%s, type=%s (by user %s)",
            file_id, owner_id, file_name, file_size, media_type, user_id
        )

        log_admin_action(
            admin_id=user_id,
            admin_name="Admin" if admin_id else str(user_id),
            action="DELETE_FILE" if not admin_id else "ADMIN_DELETE_FILE",
            target_id=owner_id,
            target_name=file_name,
            details=f"Deleted file #{file_num}: {file_name} "
                    f"({format_bytes(file_size)}, type: {media_type})",
            success=True
        )

        if admin_id:
            await query.edit_message_text(
                get_text("delete.success_single_admin", lang,
                        num=file_num, name=file_name, uid=owner_id),
                parse_mode="HTML"
            )
        else:
            await query.edit_message_text(
                get_text("delete.success_single", lang,
                        num=file_num, name=file_name),
                parse_mode="HTML"
            )

    except Exception as exc:
        logger.error("Failed to delete file %s (owner=%s): %s", file_id, owner_id, exc, exc_info=True)
        await query.edit_message_text(
            get_text("delete.failed", lang),
            parse_mode="HTML"
        )


async def _execute_delete_all(query, data, user_id, lang):
    owner_id = data["owner_id"]
    admin_id = data.get("admin_id")
    total_files = data["total_files"]
    total_size = data.get("total_size", 0)

    # ✅ Verifikasi ulang status admin (jika admin yang menghapus)
    if admin_id and not await is_admin(user_id):
        await query.edit_message_text(
            get_text("admin.access_denied", lang),
            parse_mode="HTML"
        )
        return

    # === Verifikasi hak akses ===
    if admin_id:
        if user_id != admin_id:
            await query.edit_message_text(
                get_text("delete.not_admin", lang),
                parse_mode="HTML"
            )
            return
    else:
        if user_id != owner_id:
            await query.edit_message_text(
                get_text("delete.not_owner", lang),
                parse_mode="HTML"
            )
            return

    try:
        # === Hapus semua file milik user ===
        await db.execute("DELETE FROM media_files WHERE owner_id = ?", (owner_id,))

        # === Reset counter di tabel users ===
        await db.execute("""
            UPDATE users 
            SET total_files = 0,
                total_size = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (owner_id,))

        # === Bersihkan daily stats untuk hari ini ===
        try:
            today = date.today()
            await db.execute("""
                DELETE FROM daily_stats 
                WHERE owner_id = ? AND stat_date = ?
            """, (owner_id, today))
        except Exception as stats_err:
            logger.warning("Failed to clear daily stats after delete all: %s", stats_err)

        await db.commit()

        # === Clear cache deduplikasi ===
        try:
            fast_filter.clear_user_cache(owner_id)
        except Exception as cache_err:
            logger.warning("Failed to clear cache after delete all: %s", cache_err)

        logger.info(
            "All files deleted for user %s: %s files, %s bytes (by user %s)",
            owner_id, total_files, total_size, user_id
        )

        log_admin_action(
            admin_id=user_id,
            admin_name="Admin" if admin_id else str(user_id),
            action="DELETE_ALL_FILES" if not admin_id else "ADMIN_DELETE_ALL_FILES",
            target_id=owner_id,
            target_name=f"User {owner_id}",
            details=f"Deleted all {total_files} files (total size: {format_bytes(total_size)})",
            success=True
        )

        if admin_id:
            await query.edit_message_text(
                get_text("delete.success_all_admin", lang,
                        count=total_files, uid=owner_id),
                parse_mode="HTML"
            )
        else:
            await query.edit_message_text(
                get_text("delete.success_all", lang,
                        count=total_files),
                parse_mode="HTML"
            )

    except Exception as exc:
        logger.error("Failed to delete all files for user %s: %s", owner_id, exc, exc_info=True)
        await query.edit_message_text(
            get_text("delete.failed", lang),
            parse_mode="HTML"
        )