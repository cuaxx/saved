"""
Telegram Media Storage Bot v3.0.2
Callback Store Cleaner

Background worker untuk membersihkan entri callback store
yang sudah kadaluarsa secara berkala. Mencegah kebocoran
memori pada penyimpanan data callback server-side.

FIXES v3.0.2:
- Periodic cleanup setiap 5 menit
- Final cleanup saat shutdown
- Thread-safe operations
"""

import asyncio
import logging
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CallbackStoreCleaner:
    """
    Periodic cleaner untuk callback store.
    
    Membersihkan entri yang sudah melewati TTL (default 24 jam)
    setiap 5 menit untuk mencegah akumulasi data yang tidak
    diperlukan di memori.
    
    Attributes:
        callback_store: Reference ke dictionary callback store
        callback_ttl: Time-to-live dalam detik
        worker_task: Background asyncio task
        running: Status worker
    """
    
    def __init__(self):
        self.worker_task: Optional[asyncio.Task] = None
        self.running: bool = False
        self.callback_store: Optional[Dict] = None
        self.callback_ttl: int = 86400  # 24 jam default
        self._cleanup_interval: int = 300  # 5 menit
        self.stats: Dict[str, int] = {
            "total_cleaned": 0,
            "cleanup_cycles": 0,
        }
        
    async def start(self, callback_store: Dict, ttl: int = 86400) -> None:
        """
        Start background cleanup task.
        
        Args:
            callback_store: Reference ke dictionary callback store
            ttl: Time-to-live dalam detik (default: 86400 = 24 jam)
            
        Raises:
            ValueError: Jika callback_store adalah None
        """
        if callback_store is None:
            raise ValueError("callback_store cannot be None")
            
        self.callback_store = callback_store
        self.callback_ttl = ttl
        self.running = True
        self.worker_task = asyncio.create_task(self._worker())
        logger.info(
            "CallbackStoreCleaner started (TTL: %ss, interval: %ss)",
            ttl, self._cleanup_interval
        )
    
    async def stop(self) -> None:
        """
        Stop the background worker gracefully.
        
        Melakukan final cleanup sebelum berhenti untuk memastikan
        tidak ada data kadaluarsa yang tersisa.
        """
        self.running = False
        
        # Cancel worker task
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                logger.debug("CallbackStoreCleaner task cancelled")
        
        # Final cleanup
        await self._cleanup()
        logger.info(
            "CallbackStoreCleaner stopped (total cleaned: %s)",
            self.stats["total_cleaned"]
        )
    
    async def _worker(self) -> None:
        """
        Background worker loop.
        
        Membersihkan entri kadaluarsa setiap _cleanup_interval detik.
        Menangani CancelledError untuk graceful shutdown.
        """
        while self.running:
            try:
                await self._cleanup()
                await asyncio.sleep(self._cleanup_interval)
            except asyncio.CancelledError:
                logger.debug("CallbackStoreCleaner worker cancelled")
                break
            except Exception as exc:
                logger.error(
                    "CallbackStoreCleaner worker error: %s",
                    exc, exc_info=True
                )
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _cleanup(self) -> int:
        """
        Hapus entri yang sudah expired dari callback store.
        
        Returns:
            Jumlah entri yang dibersihkan
        """
        if not self.callback_store:
            return 0
        
        now = time.time()
        expired_keys = [
            k for k, v in self.callback_store.items()
            if now - v.get("_created", 0) > self.callback_ttl
        ]
        
        for k in expired_keys:
            self.callback_store.pop(k, None)
        
        if expired_keys:
            self.stats["total_cleaned"] += len(expired_keys)
            logger.debug(
                "Cleaned %s expired callback entries "
                "(total: %s, remaining: %s)",
                len(expired_keys),
                self.stats["total_cleaned"],
                len(self.callback_store)
            )
        
        self.stats["cleanup_cycles"] += 1
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, int]:
        """
        Return cleaner statistics.
        
        Returns:
            Dictionary dengan statistik pembersihan
        """
        return {
            **self.stats,
            "current_store_size": len(self.callback_store) if self.callback_store else 0,
            "ttl_seconds": self.callback_ttl,
            "interval_seconds": self._cleanup_interval,
        }


# Global singleton instance
callback_cleaner = CallbackStoreCleaner()