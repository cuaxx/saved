"""
Telegram Media Storage Bot v3.0.4
Health Check Server

Menyediakan HTTP endpoint sederhana untuk monitoring
uptime, database health, dan metrik bot.

FIXES v3.0.4:
- ✅ Added HEALTH_SERVER_TOKEN authentication for /health and /metrics
- ✅ Configurable via HEALTH_SERVER_TOKEN in .env
- ✅ Supports ?token=... query parameter and Authorization: Bearer header
- ✅ Token verification skipped if HEALTH_SERVER_TOKEN is empty (backward compatible)
"""

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Dict, Optional

from aiohttp import web

from config import BOT_TOKEN, HEALTH_SERVER_HOST, HEALTH_SERVER_PORT, HEALTH_SERVER_TOKEN

logger = logging.getLogger(__name__)


class HealthServer:
    """
    Simple HTTP health check server untuk monitoring.

    Menyediakan endpoint:
    - GET /: Welcome page (selalu publik)
    - GET /health: Basic health check (terproteksi jika HEALTH_SERVER_TOKEN diatur)
    - GET /metrics: Statistik bot real-time (terproteksi jika HEALTH_SERVER_TOKEN diatur)

    Attributes:
        host: Bind address
        port: Bind port
        token: Token akses (dari HEALTH_SERVER_TOKEN config)
        app: aiohttp Application instance
        runner: aiohttp AppRunner
        start_time: Waktu server dimulai
    """

    def __init__(self, host: str = None, port: int = None, token: str = None):
        """
        Initialize health server.

        Args:
            host: Host address untuk binding (default: dari HEALTH_SERVER_HOST)
            port: Port untuk binding (default: dari HEALTH_SERVER_PORT)
            token: Token untuk proteksi endpoint (default: dari HEALTH_SERVER_TOKEN)
        """
        self.host: str = host or HEALTH_SERVER_HOST
        self.port: int = port or HEALTH_SERVER_PORT
        self.token: str = token if token is not None else HEALTH_SERVER_TOKEN
        self.app: web.Application = web.Application()
        self.runner: Optional[web.AppRunner] = None
        self.start_time: float = time.time()

        # Security: mask token in responses only if set
        self._masked_token = self._mask_sensitive_data(BOT_TOKEN) if BOT_TOKEN else "not_set"

        # Register routes
        self.app.router.add_get("/", self.index)
        self.app.router.add_get("/health", self.health_check)
        self.app.router.add_get("/metrics", self.metrics)

        if self.token:
            logger.info("Health server endpoints protected with token authentication")
        else:
            logger.warning(
                "Health server running without token authentication. "
                "Set HEALTH_SERVER_TOKEN in .env to protect endpoints."
            )

    @staticmethod
    def _mask_sensitive_data(data: str) -> str:
        """
        Mask sensitive data untuk response.

        Args:
            data: Data sensitif

        Returns:
            Data yang sudah dimask
        """
        if not data or len(data) < 10:
            return "***"
        return data[:4] + "..." + data[-4:]

    async def index(self, request: web.Request) -> web.Response:
        """
        Welcome page endpoint (always public).

        Returns:
            Simple text response
        """
        return web.Response(
            text=(
                "Telegram Media Storage Bot v3.0.4\n"
                "Health Server Running\n"
                f"Uptime: {int(time.time() - self.start_time)}s\n"
            ),
            content_type="text/plain",
            status=200
        )

    async def _check_token(self, request: web.Request) -> bool:
        """
        Verifikasi token akses untuk endpoint terproteksi.

        Jika token tidak dikonfigurasi (kosong), semua akses diizinkan.
        Token dapat dikirim melalui:
        - Query parameter: ?token=...
        - Header: Authorization: Bearer ...

        Args:
            request: aiohttp Request object

        Returns:
            True jika token valid atau token tidak dikonfigurasi.
        """
        # Jika tidak ada token yang dikonfigurasi, izinkan akses
        if not self.token:
            return True

        # Check query parameter
        query_token = request.rel_url.query.get("token")
        if query_token == self.token:
            return True

        # Check Authorization header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            bearer_token = auth_header[7:]
            if bearer_token == self.token:
                return True

        return False

    async def health_check(self, request: web.Request) -> web.Response:
        """
        Basic health check endpoint.

        Memeriksa:
        - Database connectivity
        - Bot token validity (basic check)
        - Token authentication (jika dikonfigurasi)

        Returns:
            JSON response dengan status kesehatan
        """
        # Verifikasi token
        if not await self._check_token(request):
            return web.Response(
                text="Forbidden: Invalid or missing token",
                status=403
            )

        health_data = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": int(time.time() - self.start_time),
            "version": "3.0.4",
            "components": {
                "database": "unknown",
                "bot_token": "configured" if BOT_TOKEN else "missing",
            }
        }

        # Check database
        try:
            from database.connection import db
            if hasattr(db, 'db') and db.db:
                await db.fetchone("SELECT 1")
                health_data["components"]["database"] = "healthy"
            else:
                health_data["components"]["database"] = "not_connected"
                health_data["status"] = "degraded"
        except Exception as exc:
            health_data["components"]["database"] = f"error: {str(exc)[:100]}"
            health_data["status"] = "unhealthy"
            logger.error("Health check database error: %s", exc)

        # Determine HTTP status
        status_map = {
            "healthy": 200,
            "degraded": 200,  # Still responding
            "unhealthy": 503,
        }

        return web.json_response(
            health_data,
            status=status_map.get(health_data["status"], 500)
        )

    async def metrics(self, request: web.Request) -> web.Response:
        """
        Enhanced metrics endpoint.

        Returns statistik bot real-time termasuk:
        - Jumlah user dan file
        - Uptime
        - Penggunaan memori

        Returns:
            JSON response dengan metrik
        """
        # Verifikasi token
        if not await self._check_token(request):
            return web.Response(
                text="Forbidden: Invalid or missing token",
                status=403
            )

        metrics_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_hours": round(
                (time.time() - self.start_time) / 3600, 2
            ),
            "version": "3.0.4",
        }

        # Get database stats
        try:
            from database.models import MediaFile, UserProfile

            metrics_data["users"] = await UserProfile.get_count()
            metrics_data["files"] = await MediaFile.get_total_count()
            metrics_data["storage_bytes"] = await MediaFile.get_total_size()
        except Exception as exc:
            logger.warning("Failed to get database metrics: %s", exc)
            metrics_data["users"] = -1
            metrics_data["files"] = -1
            metrics_data["storage_bytes"] = -1

        # Get memory usage (optional)
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            metrics_data["memory"] = {
                "rss_mb": round(memory_info.rss / 1024 / 1024, 2),
                "vms_mb": round(memory_info.vms / 1024 / 1024, 2),
                "percent": round(process.memory_percent(), 2),
            }
        except ImportError:
            metrics_data["memory"] = {"note": "psutil not installed"}
        except Exception as exc:
            logger.debug("Failed to get memory metrics: %s", exc)
            metrics_data["memory"] = {"error": str(exc)[:100]}

        return web.json_response(metrics_data, status=200)

    async def start(self) -> None:
        """
        Start the health check server.

        Memulai aiohttp server di background.
        """
        try:
            self.runner = web.AppRunner(self.app)
            await self.runner.setup()
            site = web.TCPSite(self.runner, self.host, self.port)
            await site.start()

            if self.token:
                logger.info(
                    "Health server started at http://%s:%s (token protected)",
                    self.host, self.port
                )
            else:
                logger.info(
                    "Health server started at http://%s:%s (no token)",
                    self.host, self.port
                )
        except Exception as exc:
            logger.error(
                "Failed to start health server: %s",
                exc, exc_info=True
            )
            raise

    async def stop(self) -> None:
        """
        Stop the health check server gracefully.
        """
        if self.runner:
            try:
                await self.runner.cleanup()
                logger.info("Health server stopped")
            except Exception as exc:
                logger.error(
                    "Error stopping health server: %s", exc
                )


# Global singleton instance
health_server = HealthServer()