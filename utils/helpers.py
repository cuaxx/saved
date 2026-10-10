"""
Telegram Media Storage Bot v3.0.2
Utility Helpers

Provides media data extraction, file signature generation,
validation, formatting, and command parsing utilities.

FIXES v3.0.2:
- Added input validation for all public functions
- Added sanitize_filename for security
- Added validate_user_id and validate_file_limit
- Enhanced generate_file_signature with bounds checking
"""

import hashlib
import logging
import os
from typing import Optional, Tuple

from config import ALLOWED_TYPES, MAX_FILE_SIZE_MB

logger = logging.getLogger(__name__)

# Constants for validation
MAX_FILENAME_LENGTH = 255
MAX_USER_ID = 2**63 - 1  # Maximum Telegram user ID
MAX_FILE_LIMIT = 1000000   # Maximum configurable file limit


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """
    Sanitize filename untuk mencegah path traversal dan karakter berbahaya.
    
    Args:
        filename: Nama file original
        max_length: Panjang maksimum yang diizinkan
        
    Returns:
        Nama file yang aman untuk disimpan
        
    Examples:
        >>> sanitize_filename("../../../etc/passwd")
        '______etc_passwd'
        >>> sanitize_filename("my file.txt")
        'my file.txt'
    """
    if not filename:
        return "unnamed_file"
    
    # Strip whitespace
    filename = filename.strip()
    
    # Hapus path separator dan karakter berbahaya
    dangerous_chars = ['/', '\\', '\0', '\n', '\r', '\t']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Hapus leading dots (hidden files)
    filename = filename.lstrip('.')
    
    # Jika kosong setelah sanitasi
    if not filename:
        return "unnamed_file"
    
    # Batasi panjang
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        # Preserve extension
        ext = ext[:20] if ext else ''  # Limit extension length
        max_name_length = max_length - len(ext)
        if max_name_length > 0:
            name = name[:max_name_length]
        filename = name + ext
    
    return filename


def validate_user_id(user_id_str: str) -> int:
    """
    Validasi dan konversi string user ID ke integer.
    
    Args:
        user_id_str: String user ID dari input
        
    Returns:
        Integer user ID yang valid
        
    Raises:
        ValueError: Jika user ID tidak valid
        
    Examples:
        >>> validate_user_id("123456789")
        123456789
        >>> validate_user_id("-1")
        ValueError: User ID must be positive: -1
    """
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid user ID format: {user_id_str}")
    
    if user_id <= 0:
        raise ValueError(f"User ID must be positive: {user_id}")
    
    if user_id > MAX_USER_ID:
        raise ValueError(f"User ID too large (max {MAX_USER_ID}): {user_id}")
    
    return user_id


def validate_file_limit(limit_str: str, max_limit: int = MAX_FILE_LIMIT) -> int:
    """
    Validasi file limit input.
    
    Args:
        limit_str: String limit dari input
        max_limit: Maksimum limit yang diizinkan
        
    Returns:
        Integer limit yang valid
        
    Raises:
        ValueError: Jika limit tidak valid
        
    Examples:
        >>> validate_file_limit("5000")
        5000
        >>> validate_file_limit("-100")
        ValueError: File limit cannot be negative: -100
    """
    try:
        limit = int(limit_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid file limit format: {limit_str}")
    
    if limit < 0:
        raise ValueError(f"File limit cannot be negative: {limit}")
    
    if limit > max_limit:
        raise ValueError(
            f"File limit too large (max {max_limit}): {limit}"
        )
    
    return limit


def validate_page_number(page_str: str, total_pages: int) -> int:
    """
    Validasi nomor halaman untuk navigasi.
    
    Args:
        page_str: String nomor halaman
        total_pages: Total halaman yang tersedia
        
    Returns:
        Nomor halaman yang valid (1-indexed)
        
    Raises:
        ValueError: Jika nomor halaman tidak valid
    """
    try:
        page = int(page_str.strip())
    except (ValueError, TypeError):
        raise ValueError(f"Invalid page number: {page_str}")
    
    if page < 1:
        raise ValueError("Page number must be at least 1")
    
    if page > total_pages:
        raise ValueError(
            f"Page {page} exceeds total pages ({total_pages})"
        )
    
    return page


def generate_file_signature(media_data: dict) -> str:
    """
    Generate a 16-character hex signature from file metadata.

    Used for fuzzy duplicate matching based on file properties.
    
    The signature is built from: file_size, mime_type, width,
    height, duration, and media_type. This creates a unique
    fingerprint that can detect duplicates even when Telegram
    generates different file_unique_ids.

    Args:
        media_data: Dictionary with file metadata.
            Required keys: file_size, media_type
            Optional keys: mime_type, width, height, duration

    Returns:
        16-character hexadecimal signature, or empty string
        if data is insufficient.

    Raises:
        ValueError: Jika media_data adalah None atau empty
    """
    if not media_data:
        raise ValueError("media_data cannot be None or empty")
    
    # Extract and sanitize components with bounds checking
    file_size = media_data.get("file_size") or 0
    if not isinstance(file_size, (int, float)) or file_size < 0:
        file_size = 0
    
    mime_type = str(media_data.get("mime_type", "")).strip()[:100]
    
    width = media_data.get("width", 0)
    if not isinstance(width, (int, float)) or width < 0:
        width = 0
    
    height = media_data.get("height", 0)
    if not isinstance(height, (int, float)) or height < 0:
        height = 0
    
    duration = media_data.get("duration", 0)
    if not isinstance(duration, (int, float)) or duration < 0:
        duration = 0
    
    media_type = str(media_data.get("media_type", "")).strip()[:20]
    
    # Build signature components
    components = [
        str(int(file_size)),
        mime_type,
        str(int(width)),
        str(int(height)),
        str(int(duration)),
        media_type,
    ]
    
    signature_string = "|".join(components)
    
    # Generate MD5 hash (first 16 chars for compact storage)
    return hashlib.md5(signature_string.encode()).hexdigest()[:16]


def extract_media_data(message) -> Optional[dict]:
    """
    Extract standardized media metadata from a Telegram message.

    Handles photos (highest resolution), videos, and documents.
    Adds owner_id placeholder (populated by caller).

    Args:
        message: Telegram Message object.

    Returns:
        Dictionary with file metadata, or None if no media found.
    """
    if message is None:
        return None
        
    media_data = {
        "message_id": message.message_id,
        "chat_id": message.chat_id,
        "media_group_id": message.media_group_id,
    }

    if message.photo:
        # Use highest resolution photo (last in array)
        photo = message.photo[-1]
        media_data.update({
            "file_id": photo.file_id,
            "file_unique_id": photo.file_unique_id,
            "file_size": photo.file_size or 0,
            "file_name": None,
            "mime_type": "image/jpeg",
            "media_type": "photo",
            "width": photo.width or 0,
            "height": photo.height or 0,
            "duration": 0,
        })
    elif message.video:
        video = message.video
        media_data.update({
            "file_id": video.file_id,
            "file_unique_id": video.file_unique_id,
            "file_size": video.file_size or 0,
            "file_name": sanitize_filename(video.file_name) if video.file_name else None,
            "mime_type": video.mime_type or "video/mp4",
            "media_type": "video",
            "width": video.width or 0,
            "height": video.height or 0,
            "duration": video.duration or 0,
        })
    elif message.document:
        doc = message.document
        media_data.update({
            "file_id": doc.file_id,
            "file_unique_id": doc.file_unique_id,
            "file_size": doc.file_size or 0,
            "file_name": sanitize_filename(doc.file_name) if doc.file_name else None,
            "mime_type": doc.mime_type or "application/octet-stream",
            "media_type": "document",
            "width": 0,
            "height": 0,
            "duration": 0,
        })
    else:
        return None

    # Generate signature for deduplication
    try:
        media_data["file_signature"] = generate_file_signature(media_data)
    except Exception as exc:
        logger.warning("Failed to generate file signature: %s", exc)
        media_data["file_signature"] = ""

    return media_data


def is_allowed_type(media_type: str) -> bool:
    """
    Check if a media type is in the allowed types list.
    
    Args:
        media_type: Media type string (photo, video, document).
        
    Returns:
        True if allowed.
    """
    if not media_type:
        return False
    return media_type in ALLOWED_TYPES


def is_within_size_limit(file_size: int) -> bool:
    """
    Check if file size is within configured limit (0 = unlimited).
    
    Args:
        file_size: File size in bytes.
        
    Returns:
        True if within limit or unlimited.
    """
    if MAX_FILE_SIZE_MB <= 0:
        return True
    if not isinstance(file_size, (int, float)) or file_size < 0:
        return False
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    return file_size <= max_bytes


def format_bytes(size: int) -> str:
    """
    Convert bytes to a human-readable string.
    
    Args:
        size: Size in bytes.
        
    Returns:
        Formatted string (e.g., "1.5 MB").
    """
    if not isinstance(size, (int, float)) or size < 0:
        return "0 B"
    if size == 0:
        return "0 B"
        
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def parse_get_command(text: str, default_limit: int = 10) -> Tuple[int, int]:
    """
    Parse /get command arguments.

    Examples:
        /get 7      -> (7, 7)
        /get 1-10   -> (1, 10)
        /get        -> (1, default_limit)

    Args:
        text: Command text.
        default_limit: Default number of files to return.

    Returns:
        Tuple of (start, end) positions (1-indexed).
    """
    if not text:
        return (1, default_limit)
        
    parts = text.strip().split()

    if len(parts) < 2:
        return (1, default_limit)

    range_str = parts[1]

    if "-" in range_str:
        try:
            s, e = range_str.split("-", 1)
            start_val = int(s)
            end_val = int(e)
            # Ensure valid range
            if start_val < 1:
                start_val = 1
            if end_val < start_val:
                end_val = start_val
            return (start_val, end_val)
        except ValueError:
            return (1, default_limit)

    try:
        pos = int(range_str)
        if pos < 1:
            pos = 1
        return (pos, pos)
    except ValueError:
        return (1, default_limit)