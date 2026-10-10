"""
Telegram Media Storage Bot v3.0.2
Application Enums

Mengganti string literals dengan enum untuk type safety
dan mencegah typo di seluruh aplikasi.

FIXES v3.0.2:
- Type-safe constants untuk semua string literals
- Mencegah bug akibat typo pada string comparison
- Dokumentasi lengkap untuk setiap enum value
- FIXED: Menggunakan (str, Enum) untuk kompatibilitas Python 3.10+
"""

from enum import Enum


class MediaType(str, Enum):
    """
    Tipe media yang didukung oleh bot.
    
    Digunakan untuk klasifikasi file dan filtering.
    """
    PHOTO = "photo"
    VIDEO = "video"
    DOCUMENT = "document"


class AdminRole(str, Enum):
    """
    Role dalam sistem administrasi bot.
    
    Hierarchy: SUPER_ADMIN > ADMIN > USER
    """
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"


class StatsField(str, Enum):
    """
    Field statistik yang valid untuk operasi increment.
    
    Digunakan untuk memvalidasi field sebelum update database
    dan mencegah SQL injection melalui nama field.
    """
    FILES_ADDED = "files_added"
    PHOTOS_ADDED = "photos_added"
    VIDEOS_ADDED = "videos_added"
    DOCUMENTS_ADDED = "documents_added"
    DUPLICATES_REJECTED = "duplicates_rejected"
    FILES_SERVED = "files_served"


class CallbackAction(str, Enum):
    """
    Tipe aksi untuk callback queries.
    
    Digunakan untuk routing callback handler
    dan validasi data callback.
    """
    NAVIGATE = "nav"
    VIEW_FILE = "file"
    VIEW_PAGE = "view"
    JUMP_TO_PAGE = "jump"
    LANGUAGE_SELECT = "lang:"
    IGNORE = "ignore"


class BotMode(str, Enum):
    """
    Mode operasi bot untuk environment detection.
    """
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TESTING = "testing"


class Language(str, Enum):
    INDONESIAN = "id"
    ENGLISH = "en"
    RUSSIAN = "ru"
    CHINESE = "zh"
    JAPANESE = "ja"
    SPANISH = "es"
    HINDI = "hi"
    PORTUGUESE = "pt"

LANGUAGE_DISPLAY_NAMES = {
    Language.INDONESIAN: "🇮🇩 Indonesia",
    Language.ENGLISH: "🇬🇧 English",
    Language.RUSSIAN: "🇷🇺 Русский",
    Language.CHINESE: "🇨🇳 中文",
    Language.JAPANESE: "🇯🇵 日本語",
    Language.SPANISH: "🇪🇸 Español",
    Language.HINDI: "🇮🇳 हिन्दी",
    Language.PORTUGUESE: "🇧🇷 Português",
}

# Set untuk validasi cepat
SUPPORTED_LANGUAGES = set(Language)

# Default language
DEFAULT_LANGUAGE = Language.INDONESIAN