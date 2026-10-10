"""
Telegram Media Storage Bot v3.0.2
Resilient Cache Wrapper

Wraps cache operations dengan fallback mechanisms
dan automatic error recovery untuk mencegah crash
akibat cache failure.

FIXES v3.0.2:
- Graceful degradation saat cache error
- Automatic recovery setelah periode stabil
- Detailed error tracking dan statistics
"""

import logging
from typing import Any, Dict, Optional

from config import CACHE_MAX_SIZE
from .cache import LRUCache

logger = logging.getLogger(__name__)


class ResilientCache:
    """
    Cache wrapper yang tahan terhadap error.
    
    Jika cache mengalami kegagalan berulang (misal: memory penuh,
    corrupted data), akan otomatis fallback ke mode no-op
    tanpa menyebabkan crash pada aplikasi utama.
    
    Setelah periode stabil, cache akan otomatis recover.
    
    Attributes:
        _cache: Internal LRUCache instance
        failure_count: Jumlah kegagalan berturut-turut
        max_failures: Batas kegagalan sebelum degradasi
        degraded: Status degradasi cache
        recovery_threshold: Jumlah success untuk recovery
        success_count: Jumlah keberhasilan berturut-turut
    """
    
    def __init__(
        self,
        max_size: int = None,
        max_failures: int = 10,
        recovery_threshold: int = 100
    ):
        """
        Initialize resilient cache.
        
        Args:
            max_size: Maksimum entri cache
            max_failures: Batas kegagalan sebelum degradasi
            recovery_threshold: Jumlah success untuk auto-recovery
        """
        if max_size is None:
            max_size = CACHE_MAX_SIZE
            
        self._cache = LRUCache(max_size=max_size)
        self.failure_count: int = 0
        self.max_failures: int = max_failures
        self.degraded: bool = False
        self.recovery_threshold: int = recovery_threshold
        self.success_count: int = 0
        self.stats: Dict[str, int] = {
            "total_operations": 0,
            "successful_ops": 0,
            "failed_ops": 0,
            "degradations": 0,
            "recoveries": 0,
        }
        
        logger.info(
            "ResilientCache initialized: max_size=%s, "
            "max_failures=%s, recovery=%s",
            max_size, max_failures, recovery_threshold
        )
    
    def __contains__(self, key: str) -> bool:
        """
        Check if key exists dalam cache.
        
        Jika cache dalam mode terdegradasi, selalu return False
        tanpa error.
        
        Args:
            key: Cache key
            
        Returns:
            True jika key ditemukan dan valid
        """
        self.stats["total_operations"] += 1
        
        if self.degraded:
            self._try_recovery()
            return False
        
        try:
            result = key in self._cache
            self._handle_success()
            return result
        except Exception as exc:
            self._handle_failure("contains", exc)
            return False
    
    def add(self, key: str, value: Optional[Dict[str, Any]] = None) -> None:
        """
        Add atau update cache entry.
        
        Dalam mode terdegradasi, operasi diabaikan tanpa error.
        
        Args:
            key: Cache key
            value: Optional data payload
        """
        self.stats["total_operations"] += 1
        
        if self.degraded:
            self._try_recovery()
            return
        
        try:
            self._cache.add(key, value)
            self._handle_success()
        except Exception as exc:
            self._handle_failure("add", exc)
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cache entry.
        
        Dalam mode terdegradasi, selalu return None tanpa error.
        
        Args:
            key: Cache key
            
        Returns:
            Stored data dict atau None
        """
        self.stats["total_operations"] += 1
        
        if self.degraded:
            self._try_recovery()
            return None
        
        try:
            result = self._cache.get(key)
            self._handle_success()
            return result
        except Exception as exc:
            self._handle_failure("get", exc)
            return None
    
    def remove(self, key: str) -> None:
        """
        Remove cache entry.
        
        Args:
            key: Cache key
        """
        if self.degraded:
            return
        
        try:
            self._cache.remove(key)
            self._handle_success()
        except Exception as exc:
            self._handle_failure("remove", exc)
    
    def _handle_success(self) -> None:
        """
        Handle successful cache operation.
        
        Reset failure counter dan track successful operations
        untuk potensi auto-recovery.
        """
        self.failure_count = 0
        self.stats["successful_ops"] += 1
        self.success_count += 1
    
    def _handle_failure(self, operation: str, error: Exception) -> None:
        """
        Handle cache failure dengan automatic degradation.
        
        Args:
            operation: Nama operasi yang gagal
            error: Exception yang terjadi
        """
        self.failure_count += 1
        self.stats["failed_ops"] += 1
        self.success_count = 0
        
        logger.error(
            "Cache %s failed (failure %s/%s): %s",
            operation, self.failure_count, self.max_failures, error
        )
        
        # Degradasi jika terlalu banyak kegagalan
        if self.failure_count >= self.max_failures and not self.degraded:
            self.degraded = True
            self.stats["degradations"] += 1
            logger.critical(
                "Cache DEGRADED after %s consecutive failures. "
                "Falling back to no-op mode. "
                "Will attempt recovery after %s successful operations.",
                self.failure_count, self.recovery_threshold
            )
    
    def _try_recovery(self) -> None:
        """
        Attempt cache recovery setelah periode stabil.
        
        Recovery dilakukan setelah mencapai recovery_threshold
        operasi berturut-turut tanpa error.
        """
        if not self.degraded:
            return
        
        self.success_count += 1
        
        if self.success_count >= self.recovery_threshold:
            self.degraded = False
            self.failure_count = 0
            self.stats["recoveries"] += 1
            logger.info(
                "Cache RECOVERED after %s successful operations. "
                "Resuming normal operation.",
                self.success_count
            )
    
    @property
    def size(self) -> int:
        """Current cache size."""
        try:
            return self._cache.size
        except Exception:
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Return comprehensive cache statistics.
        
        Returns:
            Dictionary dengan statistik cache dan status
        """
        base_stats = {
            "degraded": self.degraded,
            "failure_count": self.failure_count,
            "success_streak": self.success_count,
            **self.stats,
        }
        
        try:
            cache_stats = self._cache.get_stats()
            base_stats.update(cache_stats)
        except Exception:
            base_stats["cache_internal"] = "unavailable"
        
        return base_stats
    
    def clear(self) -> None:
        """Clear all cache entries."""
        try:
            self._cache.clear()
            self.failure_count = 0
            self.success_count = 0
            self.degraded = False
            logger.info("Cache cleared and reset to normal mode")
        except Exception as exc:
            logger.error("Failed to clear cache: %s", exc)
    
    def reset(self) -> None:
        """
        Force reset cache ke mode normal.
        
        Berguna untuk manual recovery setelah issue teratasi.
        """
        self.degraded = False
        self.failure_count = 0
        self.success_count = 0
        logger.info("Cache manually reset to normal mode")