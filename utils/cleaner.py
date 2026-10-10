"""
Telegram Media Storage Bot v3.0.0
Background Message Cleaner

Provides a non-blocking message deletion worker that processes
a priority queue of messages scheduled for deletion.
"""

import asyncio
import logging
from collections import deque

from telegram import Bot

from config import (
    DELETE_DELAY_SECONDS,
    DELETE_GET_DELAY_SECONDS,
    DELETE_GET_RESULTS,
)

logger = logging.getLogger(__name__)


class MessageCleaner:
    """
    Non-blocking message deletion worker.

    Maintains an internal queue of messages to be deleted at
    specific times. A background asyncio task processes the
    queue without blocking bot operations.
    """

    def __init__(self):
        self.queue = deque()
        self.worker_task = None
        self.running = False

    async def start(self):
        """Start the background worker task."""
        if not self.running:
            self.running = True
            self.worker_task = asyncio.create_task(self._worker())
            logger.info("MessageCleaner worker started")

    async def stop(self):
        """Stop the background worker and flush the queue."""
        self.running = False
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass

        while self.queue:
            bot, chat_id, message_id, delete_at = self.queue.popleft()
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass
            # Jeda untuk menghindari flood
            await asyncio.sleep(0.05)      # 50 ms = maks 20 msg/detik

        logger.info("MessageCleaner worker stopped")

    async def _worker(self):
        """Background worker loop that processes deletion queue."""
        while self.running:
            try:
                if self.queue:
                    bot, chat_id, message_id, delete_at = self.queue[0]
                    now = asyncio.get_event_loop().time()

                    if now >= delete_at:
                        self.queue.popleft()
                        try:
                            await bot.delete_message(
                                chat_id=chat_id,
                                message_id=message_id,
                            )
                            logger.debug("Deleted message: %s", message_id)
                        except Exception as exc:
                            logger.debug(
                                "Delete failed (msg %s): %s",
                                message_id, exc
                            )
                    else:
                        await asyncio.sleep(0.5)
                else:
                    await asyncio.sleep(1.0)

            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error("Worker error: %s", exc)
                await asyncio.sleep(1.0)

    async def schedule_delete(
        self,
        bot: Bot,
        chat_id: int,
        message_id: int,
        delay: int = None,
    ):
        """
        Schedule a message for deletion after a specified delay.

        Args:
            bot: The Telegram Bot instance.
            chat_id: Target chat ID.
            message_id: ID of the message to delete.
            delay: Seconds to wait before deletion (default: DELETE_DELAY_SECONDS).
        """
        if delay is None:
            delay = DELETE_DELAY_SECONDS

        if delay <= 0:
            return

        delete_at = asyncio.get_event_loop().time() + delay
        self.queue.append((bot, chat_id, message_id, delete_at))
        logger.debug(
            "Scheduled delete: msg_id=%s in %ss",
            message_id, delay
        )

    async def schedule_delete_get_result(
        self,
        bot: Bot,
        chat_id: int,
        message_id: int,
    ):
        """
        Schedule deletion of a /get command result message.

        Args:
            bot: The Telegram Bot instance.
            chat_id: Target chat ID.
            message_id: ID of the message to delete.
        """
        if not DELETE_GET_RESULTS:
            return
        await self.schedule_delete(
            bot, chat_id, message_id, DELETE_GET_DELAY_SECONDS
        )

    async def delete_multiple(
        self,
        bot: Bot,
        chat_id: int,
        message_ids: list,
    ):
        """
        Schedule multiple messages for deletion at the same time.

        Args:
            bot: The Telegram Bot instance.
            chat_id: Target chat ID.
            message_ids: List of message IDs to delete.
        """
        if DELETE_DELAY_SECONDS <= 0:
            return

        delete_at = asyncio.get_event_loop().time() + DELETE_DELAY_SECONDS
        for msg_id in message_ids:
            self.queue.append((bot, chat_id, msg_id, delete_at))
        logger.debug(
            "Scheduled delete %s messages in %ss",
            len(message_ids), DELETE_DELAY_SECONDS
        )

    async def delete_multiple_get_results(
        self,
        bot: Bot,
        chat_id: int,
        message_ids: list,
    ):
        """
        Schedule multiple /get result messages for deletion.

        Args:
            bot: The Telegram Bot instance.
            chat_id: Target chat ID.
            message_ids: List of message IDs to delete.
        """
        if not DELETE_GET_RESULTS:
            return

        delete_at = (
            asyncio.get_event_loop().time() + DELETE_GET_DELAY_SECONDS
        )
        for msg_id in message_ids:
            self.queue.append((bot, chat_id, msg_id, delete_at))
        logger.debug(
            "Scheduled delete %s get results in %ss",
            len(message_ids), DELETE_GET_DELAY_SECONDS
        )


# Global singleton instance
cleaner = MessageCleaner()