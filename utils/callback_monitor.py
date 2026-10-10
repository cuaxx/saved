"""
Telegram Media Storage Bot v3.0.3
Callback Store Monitor

Memantau ukuran callback store secara periodik dan mengirim
peringatan ke admin jika ukuran melebihi threshold.
Mencegah memory leak dari callback data yang tidak dibersihkan.

FIXES v3.0.3:
- Periodic monitoring setiap 30 menit
- Alert admin jika callback store > 80% kapasitas
- Automatic cleanup jika melebihi MAX_CALLBACK_STORE_SIZE
- Cooldown 1 jam antar alert untuk mencegah spam
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class CallbackStoreMonitor:
    """
    Periodic monitor untuk callback store.
    
    Memantau jumlah entri dalam callback store dan mengirim
    peringatan ke admin jika mendekati batas maksimum.
    Melakukan auto-cleanup saat kondisi kritis.
    
    Attributes:
        callback_store: Reference ke dictionary callback store
        bot: Telegram Bot instance untuk kirim alert
        admin_ids: List admin user IDs untuk notifikasi
        max_size: Batas maksimum callback store
        warning_threshold: Persentase untuk warning (default: 0.8 = 80%)
        interval: Interval pengecekan dalam detik (default: 1800 = 30 menit)
    """
    
    def __init__(
        self,
        callback_store: Dict,
        bot,
        admin_ids: List[int],
        max_size: int = 10000,
        warning_threshold: float = 0.8,
        interval: int = 1800
    ):
        """
        Initialize callback store monitor.
        
        Args:
            callback_store: Reference ke dictionary callback store
            bot: Telegram Bot instance
            admin_ids: List admin user IDs untuk notifikasi
            max_size: Batas maksimum callback store
            warning_threshold: Persentase kapasitas untuk warning (0.0 - 1.0)
            interval: Interval pengecekan dalam detik
        """
        self.callback_store = callback_store
        self.bot = bot
        self.admin_ids = admin_ids
        self.max_size = max_size
        self.warning_threshold = warning_threshold
        self.interval = interval
        
        # Background task
        self.worker_task: Optional[asyncio.Task] = None
        self.running: bool = False
        
        # Statistics
        self.stats: Dict[str, int] = {
            "total_checks": 0,
            "warnings_sent": 0,
            "critical_alerts": 0,
            "auto_cleanups": 0,
            "total_entries_cleaned": 0,
        }
        
        # Alert cooldown
        self._last_alert_time: float = 0
        self._alert_cooldown: int = 3600  # 1 jam antar alert
        
        logger.info(
            "CallbackStoreMonitor initialized: "
            "max=%s, warning_threshold=%s%%, interval=%ss",
            max_size, int(warning_threshold * 100), interval
        )
    
    async def start(self) -> None:
        """
        Start background monitoring task.
        
        Task akan menunggu 5 menit pertama sebelum mulai
        mengecek untuk memberi waktu bot startup.
        """
        if self.running:
            logger.warning("CallbackStoreMonitor already running")
            return
            
        self.running = True
        self.worker_task = asyncio.create_task(self._worker())
        logger.info(
            "CallbackStoreMonitor started "
            "(interval: %ss, warning at: %s%%)",
            self.interval, int(self.warning_threshold * 100)
        )
    
    async def stop(self) -> None:
        """
        Stop the monitor gracefully.
        
        Melakukan cleanup task dan mencatat statistik akhir.
        """
        if not self.running:
            return
            
        self.running = False
        
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                logger.debug("CallbackStoreMonitor task cancelled")
            self.worker_task = None
        
        logger.info(
            "CallbackStoreMonitor stopped "
            "(checks: %s, warnings: %s, cleanups: %s)",
            self.stats["total_checks"],
            self.stats["warnings_sent"],
            self.stats["auto_cleanups"]
        )
    
    async def _worker(self) -> None:
        """
        Background worker loop.
        
        Menunggu 5 menit pertama, lalu menjalankan pengecekan
        secara periodik sesuai interval yang dikonfigurasi.
        """
        # Tunggu 5 menit untuk startup
        await asyncio.sleep(300)
        logger.debug("CallbackStoreMonitor worker started checking")
        
        while self.running:
            try:
                await self._check_store()
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                logger.debug("CallbackStoreMonitor worker cancelled")
                break
            except Exception as exc:
                logger.error(
                    "CallbackStoreMonitor worker error: %s",
                    exc, exc_info=True
                )
                # Tunggu lebih lama jika terjadi error
                await asyncio.sleep(600)
    
    async def _check_store(self) -> None:
        """
        Periksa ukuran callback store dan ambil tindakan.
        
        Level tindakan:
        - Normal: Hanya log ukuran
        - Warning (>80%): Kirim alert ke admin
        - Critical (>95%): Force cleanup expired entries
        """
        self.stats["total_checks"] += 1
        
        if not self.callback_store:
            logger.debug("Callback store is empty or None")
            return
        
        current_size = len(self.callback_store)
        usage_percent = (current_size / self.max_size * 100) if self.max_size > 0 else 0
        
        # Hitung entri expired (TTL 24 jam)
        now = time.time()
        expired_count = sum(
            1 for v in self.callback_store.values()
            if now - v.get("_created", 0) > 86400
        )
        
        # Log status saat ini
        logger.debug(
            "Callback store check #%s: %s/%s (%.1f%%), expired: %s",
            self.stats["total_checks"],
            current_size, self.max_size,
            usage_percent, expired_count
        )
        
        # Level 1: Warning threshold
        if current_size > self.max_size * self.warning_threshold:
            await self._send_warning(current_size, usage_percent, expired_count)
        
        # Level 2: Critical threshold - force cleanup
        if current_size > self.max_size * 0.95:
            await self._force_cleanup(current_size)
        
        # Level 3: Normal cleanup jika banyak expired
        if expired_count > 50:
            await self._cleanup_expired(expired_count)
    
    async def _send_warning(
        self,
        current_size: int,
        usage_percent: float,
        expired_count: int
    ) -> None:
        """
        Kirim peringatan ke admin jika kapasitas mencapai threshold.
        
        Dilengkapi cooldown untuk mencegah spam alert.
        
        Args:
            current_size: Ukuran callback store saat ini
            usage_percent: Persentase penggunaan
            expired_count: Jumlah entri expired
        """
        now = time.time()
        
        # Cegah spam alert
        if now - self._last_alert_time < self._alert_cooldown:
            return
        
        self._last_alert_time = now
        self.stats["warnings_sent"] += 1
        
        message = (
            f"⚠️ <b>Callback Store Warning</b>\n\n"
            f"📊 Usage: <b>{current_size:,}/{self.max_size:,}</b> "
            f"({usage_percent:.1f}%)\n"
            f"🗑️ Expired entries: {expired_count:,}\n"
            f"🕐 Check: #{self.stats['total_checks']}\n\n"
            f"<i>Auto-cleanup akan trigger di atas 95% kapasitas.\n"
            f"Pertimbangkan untuk meningkatkan "
            f"MAX_CALLBACK_STORE_SIZE atau mengurangi "
            f"CALLBACK_STORE_TTL di konfigurasi.</i>"
        )
        
        for admin_id in self.admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=message,
                    parse_mode="HTML",
                    disable_notification=True
                )
            except Exception as exc:
                logger.warning(
                    "Failed to send callback warning to admin %s: %s",
                    admin_id, exc
                )
        
        logger.warning(
            "Callback store warning sent: %.1f%% capacity (%s/%s), "
            "%s expired",
            usage_percent, current_size, self.max_size, expired_count
        )
    
    async def _force_cleanup(self, current_size: int) -> None:
        """
        Paksa bersihkan expired entries saat kondisi kritis.
        
        Args:
            current_size: Ukuran callback store sebelum cleanup
        """
        self.stats["critical_alerts"] += 1
        self.stats["auto_cleanups"] += 1
        
        now = time.time()
        expired_keys = [
            k for k, v in self.callback_store.items()
            if now - v.get("_created", 0) > 86400
        ]
        
        for k in expired_keys:
            self.callback_store.pop(k, None)
        
        new_size = len(self.callback_store)
        removed = len(expired_keys)
        self.stats["total_entries_cleaned"] += removed
        
        logger.warning(
            "CRITICAL: Force cleanup removed %s entries "
            "(was %s, now %s, %.1f%% freed)",
            removed, current_size, new_size,
            (removed / current_size * 100) if current_size > 0 else 0
        )
        
        # Notifikasi admin
        message = (
            f"🚨 <b>Callback Store Force Cleanup</b>\n\n"
            f"📊 Before: <b>{current_size:,}</b> entries\n"
            f"🗑️ Removed: <b>{removed:,}</b> expired entries\n"
            f"📊 After: <b>{new_size:,}</b> entries\n"
            f"💾 Freed: <b>{removed - (current_size - new_size):,}</b> slots\n\n"
            f"<i>Auto-cleanup triggered at critical level.\n"
            f"Review callback store configuration.</i>"
        )
        
        for admin_id in self.admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=message,
                    parse_mode="HTML"
                )
            except Exception as exc:
                logger.warning(
                    "Failed to send cleanup alert to admin %s: %s",
                    admin_id, exc
                )
    
    async def _cleanup_expired(self, expired_count: int) -> None:
        """
        Bersihkan entri expired secara normal.
        
        Args:
            expired_count: Perkiraan jumlah entri expired
        """
        now = time.time()
        expired_keys = [
            k for k, v in self.callback_store.items()
            if now - v.get("_created", 0) > 86400
        ]
        
        actual_expired = len(expired_keys)
        
        for k in expired_keys:
            self.callback_store.pop(k, None)
        
        if actual_expired > 0:
            self.stats["total_entries_cleaned"] += actual_expired
            logger.debug(
                "Normal cleanup: removed %s expired entries "
                "(was estimated %s, remaining: %s)",
                actual_expired, expired_count,
                len(self.callback_store)
            )
    
    def get_stats(self) -> Dict:
        """
        Return comprehensive monitor statistics.
        
        Returns:
            Dictionary dengan statistik monitoring lengkap
        """
        current_size = len(self.callback_store) if self.callback_store else 0
        usage_percent = (current_size / self.max_size * 100) if self.max_size > 0 else 0
        
        return {
            "monitor_status": "running" if self.running else "stopped",
            "current_store_size": current_size,
            "max_size": self.max_size,
            "usage_percent": round(usage_percent, 1),
            "warning_threshold": f"{int(self.warning_threshold * 100)}%",
            "interval_minutes": self.interval // 60,
            "last_alert_ago_seconds": (
                int(time.time() - self._last_alert_time)
                if self._last_alert_time else None
            ),
            **self.stats,
        }


# Global singleton instance
callback_monitor: Optional[CallbackStoreMonitor] = None


def init_callback_monitor(
    callback_store: Dict,
    bot,
    admin_ids: List[int],
    max_size: int = 10000,
    interval: int = 1800,
    warning_threshold: float = 0.8
) -> CallbackStoreMonitor:
    """
    Initialize global callback monitor singleton.
    
    Args:
        callback_store: Reference ke dictionary callback store
        bot: Telegram Bot instance
        admin_ids: List admin user IDs
        max_size: Maksimum ukuran callback store
        interval: Interval pengecekan dalam detik
        warning_threshold: Threshold warning (0.0 - 1.0)
        
    Returns:
        CallbackStoreMonitor instance
    """
    global callback_monitor
    callback_monitor = CallbackStoreMonitor(
        callback_store=callback_store,
        bot=bot,
        admin_ids=admin_ids,
        max_size=max_size,
        warning_threshold=warning_threshold,
        interval=interval
    )
    return callback_monitor