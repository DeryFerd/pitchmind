"""Agent harness: budget cap, retry with backoff, circuit breaker."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


class BudgetExhausted(Exception):
    """Raised when an operation would exceed the remaining budget."""


class CircuitOpen(Exception):
    """Raised when the circuit breaker is open after consecutive failures."""


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


class AgentHarness:
    """Wraps async agent calls with budget tracking, retry, and circuit breaker."""

    def __init__(
        self,
        budget_usd: float,
        *,
        circuit_failure_threshold: int = 5,
        retries: int = 3,
        base_delay: float = 1.0,
    ):
        self.budget_remaining = budget_usd
        self._circuit_failure_threshold = circuit_failure_threshold
        self._consecutive_failures = 0
        self._circuit_open = False
        self._retries = retries
        self._base_delay = base_delay

    @property
    def circuit_open(self) -> bool:
        return self._circuit_open

    async def execute(
        self,
        fn: Callable[[], Awaitable[T]],
        *,
        cost_estimate: float = 0.0,
        actual_cost: float | None = None,
    ) -> T:
        if self._circuit_open:
            raise CircuitOpen("Too many failures — circuit breaker is open")

        if cost_estimate > self.budget_remaining:
            raise BudgetExhausted(
                f"Cost ${cost_estimate:.4f} exceeds remaining budget ${self.budget_remaining:.4f}"
            )

        try:
            result = await retry_async(
                fn,
                retries=self._retries,
                base_delay=self._base_delay,
            )
            self._consecutive_failures = 0
            self.budget_remaining -= actual_cost if actual_cost is not None else cost_estimate
            return result
        except Exception:
            self._consecutive_failures += 1
            if self._consecutive_failures >= self._circuit_failure_threshold:
                self._circuit_open = True
            raise
