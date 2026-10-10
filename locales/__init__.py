"""
Locales Package

Multi-language support for bot messages.
Supports: id, en, ru, zh, ja, es, hi, pt
"""

from .loader import (
    get_text,
    get_user_language,
    set_user_language,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
)

__all__ = [
    "get_text",
    "get_user_language", 
    "set_user_language",
    "SUPPORTED_LANGUAGES",
    "DEFAULT_LANGUAGE",
]