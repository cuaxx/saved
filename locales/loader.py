"""
Language Loader and Manager v3.0.3

Provides translation lookup, auto-detection, and user preference
management for multi-language bot messages.
Supports: id, en, ru, zh, ja, es, hi, pt
"""

import logging

from database.models import UserProfile

from .id import TEXTS as TEXTS_ID
from .en import TEXTS as TEXTS_EN
from .ru import TEXTS as TEXTS_RU
from .zh import TEXTS as TEXTS_ZH
from .ja import TEXTS as TEXTS_JA
from .es import TEXTS as TEXTS_ES
from .hi import TEXTS as TEXTS_HI
from .pt import TEXTS as TEXTS_PT

logger = logging.getLogger(__name__)

ALL_TEXTS = {
    "id": TEXTS_ID,
    "en": TEXTS_EN,
    "ru": TEXTS_RU,
    "zh": TEXTS_ZH,
    "ja": TEXTS_JA,
    "es": TEXTS_ES,
    "hi": TEXTS_HI,
    "pt": TEXTS_PT,
}

SUPPORTED_LANGUAGES = {
    "id": "🇮🇩 Bahasa Indonesia",
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "zh": "🇨🇳 中文",
    "ja": "🇯🇵 日本語",
    "es": "🇪🇸 Español",
    "hi": "🇮🇳 हिन्दी",
    "pt": "🇧🇷 Português",
}

DEFAULT_LANGUAGE = "id"


def get_text(key: str, lang: str = None, **kwargs) -> str:
    if lang is None or lang not in ALL_TEXTS:
        lang = DEFAULT_LANGUAGE
    texts = ALL_TEXTS.get(lang, ALL_TEXTS[DEFAULT_LANGUAGE])
    text = texts.get(key)
    if text is None:
        text = ALL_TEXTS[DEFAULT_LANGUAGE].get(key, f"⚠️ Missing translation key: {key}")
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError) as e:
            logger.warning("Format error for key '%s': %s", key, e)
            return text
    return text


async def get_user_language(update) -> str:
    user = update.message.from_user if update.message else None
    if user is None:
        return DEFAULT_LANGUAGE
    user_id = user.id
    try:
        profile = await UserProfile.get(user_id)
        if profile and profile.get("language_code"):
            saved_lang = profile["language_code"]
            if saved_lang in ALL_TEXTS:
                return saved_lang
    except Exception:
        pass
    telegram_lang = user.language_code
    if telegram_lang:
        lang_map = {
            "id": "id", "en": "en", "ru": "ru", "zh": "zh",
            "zh-hans": "zh", "zh-hant": "zh", "ja": "ja",
            "es": "es", "hi": "hi", "pt": "pt",
        }
        mapped = lang_map.get(telegram_lang.lower(), telegram_lang[:2].lower())
        if mapped in ALL_TEXTS:
            return mapped
    return DEFAULT_LANGUAGE


async def set_user_language(user_id: int, lang: str) -> bool:
    if lang not in ALL_TEXTS:
        return False
    await UserProfile.set_language(user_id, lang)
    return True