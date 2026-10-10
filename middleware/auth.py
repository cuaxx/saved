"""
Telegram Media Storage Bot v3.0.0
Authentication and Authorization Middleware

Provides helper functions to check admin privileges and decorators
for protecting admin-only commands.
"""

from functools import wraps
from typing import Callable, List

from config import SUPER_ADMIN_IDS
from database.models import AdminUsers


def is_super_admin(user_id: int) -> bool:
    """
    Check if a user is a super admin (configured in .env).

    Super admins cannot be removed via runtime commands.

    Args:
        user_id: Telegram user ID.

    Returns:
        True if super admin.
    """
    return user_id in SUPER_ADMIN_IDS


async def is_admin(user_id: int) -> bool:
    """
    Check if a user has admin privileges.

    Admins can be either super admins (from .env) or runtime
    admins (from the admin_users table).

    Args:
        user_id: Telegram user ID.

    Returns:
        True if admin.
    """
    if is_super_admin(user_id):
        return True
    return await AdminUsers.exists(user_id)


async def get_admin_level(user_id: int) -> str:
    """
    Get the admin level of a user.

    Returns:
        'super_admin', 'admin', or 'user'.
    """
    if is_super_admin(user_id):
        return "super_admin"
    if await AdminUsers.exists(user_id):
        return "admin"
    return "user"


def admin_required(func: Callable) -> Callable:
    """
    Decorator to restrict a command handler to admin users only.

    Usage:
        @admin_required
        async def handle_admin_command(update, context):
            ...

    Args:
        func: The async handler function to wrap.

    Returns:
        Wrapped function that checks admin status before execution.
    """
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.message.from_user.id
        if not await is_admin(user_id):
            await update.message.reply_text(
                "❌ Access denied. Admin privileges required."
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper