"""
Telegram Media Storage Bot v3.0.4
Configuration Module

Loads all application settings from environment variables with
sensible defaults. Centralizes configuration management for
maintainability and security.

CHANGES v3.0.4:
- Synchronized USER_DEFAULT_FILE_LIMIT default with .env.example (200000)
- Added HEALTH_SERVER_TOKEN for endpoint security
- Added language validation utilities (existing)
- Added SUPPORTED_LANGUAGES for consistency (8 languages)
- Enhanced type safety with constants
- NEW: Per-user queue configuration (USER_QUEUE_MAXSIZE, TOTAL_QUEUED_LIMIT, etc.)
- NEW: SQLite optimization pragmas
"""

import os
from typing import List, Set

from dotenv import load_dotenv

load_dotenv()


def _get_bool(key: str, default: str = "true") -> bool:
    """Parse environment variable as boolean."""
    return os.getenv(key, default).lower() == "true"


def _get_int(key: str, default: str) -> int:
    """Parse environment variable as integer."""
    return int(os.getenv(key, default))


def _get_float(key: str, default: str) -> float:
    """Parse environment variable as float."""
    return float(os.getenv(key, default))


def _get_list(key: str, default: str) -> List[str]:
    """Parse environment variable as comma-separated list."""
    return os.getenv(key, default).split(",")


def _get_int_list(key: str, default: str) -> List[int]:
    """Parse environment variable as comma-separated list of integers."""
    value = os.getenv(key, default)
    if not value.strip():
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip()]


# ============================================
# SUPPORTED LANGUAGES (v3.0.3 - 8 languages)
# ============================================
SUPPORTED_LANGUAGES: Set[str] = {"id", "en", "ru", "zh", "ja", "es", "hi", "pt"}
DEFAULT_LANGUAGE: str = "id"


def validate_language(lang: str) -> str:
    """
    Validate and normalize language code.
    
    Args:
        lang: Language code from user or config
        
    Returns:
        Valid language code or DEFAULT_LANGUAGE
    """
    if lang and lang in SUPPORTED_LANGUAGES:
        return lang
    return DEFAULT_LANGUAGE


# ============================================
# BOT CONFIGURATION
# ============================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN is not set in .env file. "
        "Create a .env file with your bot token from @BotFather."
    )

# ============================================
# SUPER ADMIN CONFIGURATION
# ============================================
SUPER_ADMIN_IDS: List[int] = _get_int_list("ADMIN_IDS", "")

# ============================================
# DATABASE CONFIGURATION
# ============================================
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/media_bot.db")

# ============================================
# CACHE CONFIGURATION
# ============================================
CACHE_MAX_SIZE = _get_int("CACHE_MAX_SIZE", "50000")
CACHE_TTL_HOURS = _get_int("CACHE_TTL_HOURS", "24")

# ============================================
# GROUP BUFFER CONFIGURATION
# ============================================
GROUP_BUFFER_SECONDS = _get_float("GROUP_BUFFER_SECONDS", "2.0")

# ============================================
# AUTO DELETE CONFIGURATION
# ============================================
DELETE_DELAY_SECONDS = _get_int("DELETE_DELAY_SECONDS", "5")
DELETE_MEDIA_ONLY = _get_bool("DELETE_MEDIA_ONLY", "true")
DELETE_GET_RESULTS = _get_bool("DELETE_GET_RESULTS", "true")
DELETE_GET_DELAY_SECONDS = _get_int("DELETE_GET_DELAY_SECONDS", "120")

# ============================================
# RATE LIMITER CONFIGURATION
# ============================================
RATE_LIMIT_PER_SECOND = _get_int("RATE_LIMIT_PER_SECOND", "5")
RATE_LIMIT_BURST = _get_int("RATE_LIMIT_BURST", "10")

# ============================================
# DEDUPLICATION CONFIGURATION
# ============================================
DEDUP_STRICT_MODE = _get_bool("DEDUP_STRICT_MODE", "true")
DEDUP_SIGNATURE_WEIGHTS = _get_list(
    "DEDUP_SIGNATURE_WEIGHTS", "size,mime,resolution,duration"
)

# ============================================
# GET COMMAND CONFIGURATION
# ============================================
GET_DEFAULT_LIMIT = _get_int("GET_DEFAULT_LIMIT", "10")
GET_SEND_AS_GROUP = _get_bool("GET_SEND_AS_GROUP", "true")
GET_MAX_RANGE = _get_int("GET_MAX_RANGE", "50")

# ============================================
# STATISTICS CONFIGURATION
# ============================================
STATS_ANONYMOUS = _get_bool("STATS_ANONYMOUS", "true")
STATS_RETENTION_DAYS = _get_int("STATS_RETENTION_DAYS", "90")

# ============================================
# STORAGE CONFIGURATION
# ============================================
MAX_FILES_TOTAL = _get_int("MAX_FILES_TOTAL", "0")
MAX_FILE_SIZE_MB = _get_int("MAX_FILE_SIZE_MB", "0")
ALLOWED_TYPES = _get_list("ALLOWED_TYPES", "photo,video,document")

# ============================================
# USER LIMITS CONFIGURATION
# (Sinkron dengan .env.example v3.0.4)
# ============================================
USER_DEFAULT_FILE_LIMIT = _get_int("USER_DEFAULT_FILE_LIMIT", "200000")
USER_DEFAULT_STORAGE_MB = _get_int("USER_DEFAULT_STORAGE_MB", "0")

# ============================================
# PER-USER QUEUE CONFIGURATION (NEW)
# ============================================
USER_QUEUE_MAXSIZE = _get_int("USER_QUEUE_MAXSIZE", "100")      # Maks antrean per user
TOTAL_QUEUED_LIMIT = _get_int("TOTAL_QUEUED_LIMIT", "5000")     # Maks total antrean global
MAX_CONCURRENT_WORKERS = _get_int("MAX_CONCURRENT_WORKERS", "50") # Maks worker paralel
WORKER_IDLE_TIMEOUT = _get_int("WORKER_IDLE_TIMEOUT", "30")     # Detik idle sebelum worker dihapus

# ============================================
# AUTO BAN CONFIGURATION
# ============================================
AUTO_BAN_ENABLED = _get_bool("AUTO_BAN_ENABLED", "false")
AUTO_BAN_THRESHOLD = _get_int("AUTO_BAN_THRESHOLD", "10")

# ============================================
# LOGGING CONFIGURATION
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")

# ============================================
# HEALTH SERVER CONFIGURATION
# ============================================
HEALTH_SERVER_HOST = os.getenv("HEALTH_SERVER_HOST", "0.0.0.0")
HEALTH_SERVER_PORT = _get_int("HEALTH_SERVER_PORT", "8080")
HEALTH_SERVER_TOKEN = os.getenv("HEALTH_SERVER_TOKEN", "")