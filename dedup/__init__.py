"""
Deduplication Package

Implements a two-layer duplicate detection system:
- Fast Filter: In-memory LRU cache for sub-millisecond lookups.
- Deep Check: Database query for permanent, authoritative verification.

Cache entries are only added after confirmation by the deep check
or successful database insertion, preventing cache pollution.
"""

from .deep_check import deep_checker
from .fast_filter import fast_filter

__all__ = ["fast_filter", "deep_checker"]