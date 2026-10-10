"""
Telegram Media Storage Bot v3.0.4
Admin Action Logger

Mencatat semua tindakan admin ke file log terpisah
untuk audit trail dan monitoring keamanan.

Format log: JSON untuk memudahkan parsing dan analisis.
Rotasi otomatis setiap 10MB dengan 5 file backup.

FIXES v3.0.3:
- Separate admin audit log with automatic rotation
- Structured JSON logging format
- Helper functions for easy integration

FIXES v3.0.4:
- ✅ Fixed: Permission handling with console fallback
- ✅ Fixed: Graceful degradation when log directory not writable
- ✅ Added: Logger health check function
"""

import json
import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional

# ============================================
# CONSTANTS
# ============================================
LOG_DIR = "logs"
LOG_FILE_NAME = "admin_actions.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

# ============================================
# ADMIN LOGGER SETUP WITH FALLBACK
# ============================================
admin_logger = logging.getLogger("admin_audit")
admin_logger.setLevel(logging.INFO)
admin_logger.propagate = False  # Don't propagate to root logger

# Track logger status
_logger_status = {
    "initialized": False,
    "file_logging": False,
    "console_fallback": False,
    "init_error": None,
    "log_file_path": None,
}

def _setup_admin_logger() -> None:
    """
    Setup admin logger with graceful fallback.
    
    Tries file-based logging first, falls back to console
    if directory is not writable.
    """
    global _logger_status
    
    try:
        # Attempt to create log directory
        os.makedirs(LOG_DIR, exist_ok=True)
        
        # Test write permission
        test_file = os.path.join(LOG_DIR, ".admin_write_test")
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            
            # Permission OK — use file handler
            log_file = os.path.join(LOG_DIR, LOG_FILE_NAME)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=MAX_LOG_SIZE,
                backupCount=BACKUP_COUNT,
                encoding="utf-8"
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                )
            )
            
            admin_logger.addHandler(file_handler)
            
            _logger_status.update({
                "initialized": True,
                "file_logging": True,
                "console_fallback": False,
                "log_file_path": log_file,
            })
            
            # Log successful initialization
            admin_logger.info(
                json.dumps({
                    "action": "LOGGER_INIT",
                    "details": "Admin audit logger initialized (file-based)",
                    "log_file": log_file,
                    "max_size_mb": MAX_LOG_SIZE // (1024 * 1024),
                    "backup_count": BACKUP_COUNT,
                    "timestamp": datetime.now().isoformat()
                }, ensure_ascii=False)
            )
            return
            
        except (OSError, PermissionError, IOError) as perm_error:
            _logger_status["init_error"] = str(perm_error)
            raise perm_error
            
    except Exception as exc:
        # Fallback: use console handler
        _logger_status["init_error"] = str(exc)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter(
                "[ADMIN_AUDIT] %(asctime)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        admin_logger.addHandler(console_handler)
        
        _logger_status.update({
            "initialized": True,
            "file_logging": False,
            "console_fallback": True,
            "log_file_path": None,
        })
        
        # Log fallback status
        admin_logger.warning(
            json.dumps({
                "action": "LOGGER_INIT",
                "details": f"Admin audit logger using CONSOLE FALLBACK. "
                          f"Error: {exc}",
                "error_type": type(exc).__name__,
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False)
        )

# Initialize on module load
_setup_admin_logger()


# ============================================
# PUBLIC FUNCTIONS
# ============================================

def log_admin_action(
    admin_id: int,
    admin_name: str,
    action: str,
    target_id: Optional[int] = None,
    target_name: Optional[str] = None,
    details: Optional[str] = None,
    success: bool = True
) -> None:
    """
    Log tindakan admin ke file audit.
    
    Args:
        admin_id: User ID admin yang melakukan tindakan
        admin_name: Nama admin (first_name dari Telegram)
        action: Jenis tindakan (BAN_USER, UNBAN_USER, DELETE_FILE, dll)
        target_id: User ID target (jika ada)
        target_name: Nama target (jika ada)
        details: Detail tambahan tentang tindakan
        success: Apakah tindakan berhasil
        
    Action types yang umum:
        - BAN_USER              : Membanned user
        - UNBAN_USER            : Membuka banned user
        - ADD_ADMIN             : Menambah admin baru
        - REMOVE_ADMIN          : Menghapus admin
        - SET_FILE_LIMIT        : Mengatur limit file user
        - BROADCAST             : Mengirim broadcast message
        - REPLY_USER            : Membalas pesan user
        - DELETE_FILE           : User menghapus file sendiri
        - ADMIN_DELETE_FILE     : Admin menghapus file user
        - DELETE_ALL_FILES      : User menghapus semua file
        - ADMIN_DELETE_ALL_FILES: Admin menghapus semua file user
        - BOT_STARTUP           : Bot berhasil start
        - BOT_SHUTDOWN          : Bot shutdown
        
    Example:
        >>> log_admin_action(
        ...     admin_id=123456789,
        ...     admin_name="John",
        ...     action="BAN_USER",
        ...     target_id=987654321,
        ...     target_name="Spammer",
        ...     details="Banned for violating terms of service"
        ... )
    """
    try:
        status = "SUCCESS" if success else "FAILED"
        
        # Buat pesan log terstruktur dalam format JSON
        log_entry = json.dumps({
            "admin_id": admin_id,
            "admin_name": str(admin_name),
            "action": str(action),
            "target_id": target_id,
            "target_name": str(target_name) if target_name else "",
            "details": str(details) if details else "",
            "status": "success" if success else "failed",
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False)
        
        admin_logger.info(f"[{status}] {log_entry}")
        
    except Exception as exc:
        # Last resort: print to stderr
        print(
            f"[ADMIN_AUDIT_ERROR] Failed to log action: {exc}",
            file=sys.stderr
        )


def get_admin_name(update) -> str:
    """
    Dapatkan nama admin dari Telegram Update object.
    
    Mendukung multiple update types:
    - Message update
    - Callback query update
    
    Args:
        update: Telegram Update atau CallbackQuery object
        
    Returns:
        Nama admin (first_name) atau "Unknown" jika tidak ditemukan
        
    Example:
        >>> async def handler(update, context):
        ...     admin_name = get_admin_name(update)
        ...     log_admin_action(..., admin_name=admin_name, ...)
    """
    user = None
    
    # Coba dari message (command handler)
    if hasattr(update, 'message') and update.message:
        user = update.message.from_user
    
    # Coba dari callback_query (button handler)
    elif hasattr(update, 'callback_query') and update.callback_query:
        user = update.callback_query.from_user
    
    # Coba dari effective_user (generic)
    elif hasattr(update, 'effective_user') and update.effective_user:
        user = update.effective_user
    
    if user:
        # Gunakan first_name, fallback ke username atau ID
        return (
            user.first_name or
            f"@{user.username}" if user.username else
            f"User_{user.id}"
        )
    
    return "Unknown"


def get_admin_name_from_query(query) -> str:
    """
    Dapatkan nama admin dari CallbackQuery object.
    
    Args:
        query: Telegram CallbackQuery object
        
    Returns:
        Nama admin atau "Unknown"
    """
    if query and query.from_user:
        user = query.from_user
        return (
            user.first_name or
            f"@{user.username}" if user.username else
            f"User_{user.id}"
        )
    return "Unknown"


def get_logger_status() -> dict:
    """
    Return admin logger health status.
    
    Returns:
        Dictionary dengan status logger saat ini
        
    Example:
        >>> status = get_logger_status()
        >>> print(status)
        {
            "initialized": True,
            "file_logging": True,
            "console_fallback": False,
            "log_file_path": "logs/admin_actions.log",
            ...
        }
    """
    status = _logger_status.copy()
    status["timestamp"] = datetime.now().isoformat()
    return status


def check_logger_health() -> bool:
    """
    Check if admin logger is healthy.
    
    Returns:
        True if logger is working (either file or console fallback)
    """
    return _logger_status.get("initialized", False)


# ============================================
# MODULE LOAD LOG
# ============================================
if _logger_status.get("file_logging"):
    print(f"✅ Admin audit logger ready: {_logger_status['log_file_path']}")
elif _logger_status.get("console_fallback"):
    print(
        f"⚠️  Admin audit logger using console fallback. "
        f"Error: {_logger_status.get('init_error', 'Unknown')}"
    )
else:
    print("❌ Admin audit logger failed to initialize!")