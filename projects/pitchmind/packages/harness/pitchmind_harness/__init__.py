"""Agent harness: retry with exponential backoff."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def retry_async(
    fn: Callable[[], Awaitable[T]],
    *,
    retries: int = 3,
    base_delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> T:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return await fn()
        except exceptions as exc:
            last_error = exc
            if attempt < retries - 1:
                await asyncio.sleep(base_delay * (2**attempt))
    raise RuntimeError(f"Failed after {retries} retries") from last_error
