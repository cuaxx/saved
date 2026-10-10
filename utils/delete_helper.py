"""
Telegram Media Storage Bot v3.0.3
Delete Helper Utility

Menyediakan fungsi safe_delete untuk menghapus pesan
hanya jika DELETE_MEDIA_ONLY=false. Mencegah pesan
teks command terhapus saat DELETE_MEDIA_ONLY=true.

FIXES v3.0.3:
- safe_delete_message: Hapus pesan dengan cek DELETE_MEDIA_ONLY
- safe_delete_update: Hapus pesan dari Update object
- Mencegah 18 bug di 3 handler file
"""

import logging

from config import DELETE_DELAY_SECONDS, DELETE_MEDIA_ONLY
from utils.cleaner import cleaner

logger = logging.getLogger(__name__)


async def safe_delete_message(bot, chat_id: int, message_id: int, delay: int = None) -> None:
    """
    Hapus pesan hanya jika DELETE_MEDIA_ONLY=false.
    
    Fungsi ini digunakan untuk menghapus pesan teks command
    (seperti /start, /help, /get, /stats, dll) yang TIDAK
    seharusnya dihapus saat DELETE_MEDIA_ONLY=true.
    
    Args:
        bot: Telegram Bot instance
        chat_id: Chat ID tujuan
        message_id: Message ID yang akan dihapus
        delay: Delay dalam detik sebelum penghapusan
               (default: DELETE_DELAY_SECONDS dari config)
               
    Examples:
        # Hapus pesan dengan delay default
        await safe_delete_message(context.bot, chat_id, msg_id)
        
        # Hapus pesan dengan delay khusus
        await safe_delete_message(context.bot, chat_id, msg_id, delay=15)
        
        # Jika DELETE_MEDIA_ONLY=true, pesan TIDAK akan dihapus
        # Jika DELETE_MEDIA_ONLY=false, pesan akan dihapus
    """
    if not DELETE_MEDIA_ONLY:
        actual_delay = delay if delay is not None else DELETE_DELAY_SECONDS
        await cleaner.schedule_delete(bot, chat_id, message_id, delay=actual_delay)
        logger.debug(
            "Safe delete scheduled: msg_id=%s, delay=%ss",
            message_id, actual_delay
        )
    else:
        logger.debug(
            "Safe delete skipped (DELETE_MEDIA_ONLY=true): msg_id=%s",
            message_id
        )


async def safe_delete_update(update, context, delay: int = None) -> None:
    """
    Hapus pesan dari Update object hanya jika DELETE_MEDIA_ONLY=false.
    
    Convenience function yang mengekstrak chat_id dan message_id
    dari Telegram Update object secara otomatis.
    
    Args:
        update: Telegram Update object
        context: CallbackContext object (mengandung bot instance)
        delay: Delay dalam detik sebelum penghapusan
               (default: DELETE_DELAY_SECONDS dari config)
               
    Examples:
        # Di dalam handler command
        await safe_delete_update(update, context)
        
        # Dengan delay khusus
        await safe_delete_update(update, context, delay=10)
    """
    if update and update.message:
        await safe_delete_message(
            context.bot,
            update.message.chat_id,
            update.message.message_id,
            delay=delay
        )