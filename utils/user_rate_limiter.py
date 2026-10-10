"""
Telegram Media Storage Bot v3.0.2
Per-User Rate Limiter

Mencegah abuse dan spam pada tombol callback dengan membatasi
jumlah callback per user dalam periode waktu tertentu.

FIXES v3.0.2:
- Rate limiting per-user untuk callback queries
- Automatic cleanup entri lama
- Configurable limits per operation type
"""

import logging
import time
from collections import defaultdict
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class UserRateLimiter:
    """
    Rate limiter per-user untuk operasi callback.
    
    Mencegah user melakukan spam dengan membatasi jumlah
    panggilan dalam periode waktu tertentu. Mendukung
    multiple operation types dengan limit berbeda.
    
    Attributes:
        max_calls: Maksimum panggilan per periode (default)
        period: Periode waktu dalam detik (default)
        user_calls: Dictionary tracking panggilan per user
        operation_limits: Custom limits per operation type
    """
    
    def __init__(
        self,
        max_calls: int = 5,
        period: float = 1.0,
        max_age: float = 3600.0
    ):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maksimum panggilan per periode (default: 5)
            period: Periode waktu dalam detik (default: 1.0)
            max_age: Umur maksimum entri user tanpa aktivitas (default: 1 jam)
        """
        self.default_max_calls: int = max_calls
        self.default_period: float = period
        self.max_age: float = max_age
        self.user_calls: Dict[int, List[float]] = defaultdict(list)
        self.operation_limits: Dict[str, tuple] = {}
        self.stats: Dict[str, int] = {
            "total_checks": 0,
            "total_allowed": 0,
            "total_blocked": 0,
            "active_users": 0,
        }
        
        # Periodic cleanup
        self._last_cleanup: float = time.time()
        self._cleanup_interval: float = 300.0  # 5 menit
        
        logger.info(
            "UserRateLimiter initialized: %s calls/%ss",
            max_calls, period
        )
    
    def set_operation_limit(
        self,
        operation: str,
        max_calls: int,
        period: float
    ) -> None:
        """
        Set custom limit untuk tipe operasi tertentu.
        
        Args:
            operation: Nama operasi (contoh: "callback", "command")
            max_calls: Maksimum panggilan
            period: Periode dalam detik
        """
        self.operation_limits[operation] = (max_calls, period)
        logger.debug(
            "Set limit for '%s': %s/%ss",
            operation, max_calls, period
        )
    
    def is_allowed(
        self,
        user_id: int,
        operation: str = "default"
    ) -> bool:
        """
        Check if user is allowed to perform operation.
        
        Args:
            user_id: Telegram user ID
            operation: Tipe operasi (default: "default")
            
        Returns:
            True jika diizinkan, False jika terkena rate limit
        """
        self.stats["total_checks"] += 1
        self._cleanup_if_needed()
        
        # Get limits for this operation
        if operation in self.operation_limits:
            max_calls, period = self.operation_limits[operation]
        else:
            max_calls, period = self.default_max_calls, self.default_period
        
        now = time.time()
        calls = self.user_calls[user_id]
        
        # Hapus panggilan yang sudah di luar periode
        self.user_calls[user_id] = [
            t for t in calls if now - t < period
        ]
        
        # Check limit
        current_calls = len(self.user_calls[user_id])
        if current_calls >= max_calls:
            self.stats["total_blocked"] += 1
            logger.debug(
                "User %s rate limited for '%s' (%s/%s calls in %ss)",
                user_id, operation, current_calls, max_calls, period
            )
            return False
        
        # Catat panggilan baru
        self.user_calls[user_id].append(now)
        self.stats["total_allowed"] += 1
        self.stats["active_users"] = len(self.user_calls)
        return True
    
    def get_user_rate(self, user_id: int) -> Dict[str, float]:
        """
        Get current usage rate for user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dictionary dengan statistik penggunaan user
        """
        now = time.time()
        calls = self.user_calls[user_id]
        
        # Hitung rate untuk default period
        recent_calls = [
            t for t in calls
            if now - t < self.default_period
        ]
        
        return {
            "calls_per_second": len(recent_calls) / self.default_period,
            "total_recent_calls": len(recent_calls),
            "limit": self.default_max_calls,
            "remaining": max(0, self.default_max_calls - len(recent_calls)),
        }
    
    def _cleanup_if_needed(self) -> None:
        """
        Periodic cleanup entri user yang sudah lama tidak aktif.
        """
        now = time.time()
        
        # Only cleanup every _cleanup_interval seconds
        if now - self._last_cleanup < self._cleanup_interval:
            return
        
        self._last_cleanup = now
        expired_users = []
        
        for user_id, calls in self.user_calls.items():
            if not calls or now - max(calls) > self.max_age:
                expired_users.append(user_id)
        
        for user_id in expired_users:
            del self.user_calls[user_id]
        
        if expired_users:
            self.stats["active_users"] = len(self.user_calls)
            logger.debug(
                "Cleaned %s expired rate limit entries "
                "(%s active users remaining)",
                len(expired_users), self.stats["active_users"]
            )
    
    def get_stats(self) -> Dict[str, int]:
        """
        Return rate limiter statistics.
        
        Returns:
            Dictionary dengan statistik lengkap
        """
        self._cleanup_if_needed()
        return {
            **self.stats,
            "active_users": len(self.user_calls),
        }
    
    def reset_user(self, user_id: int) -> None:
        """
        Reset rate limit counter untuk user tertentu.
        
        Args:
            user_id: Telegram user ID
        """
        if user_id in self.user_calls:
            del self.user_calls[user_id]
            logger.debug("Rate limit reset for user %s", user_id)


# Global singleton dengan konfigurasi yang masuk akal
callback_rate_limiter = UserRateLimiter(
    max_calls=5,     # 5 panggilan
    period=1.0,      # per detik
    max_age=3600.0   # bersihkan setelah 1 jam tidak aktif
)

# Set custom limits untuk operasi berbeda
callback_rate_limiter.set_operation_limit("command", max_calls=3, period=2.0)
callback_rate_limiter.set_operation_limit("admin", max_calls=10, period=1.0)