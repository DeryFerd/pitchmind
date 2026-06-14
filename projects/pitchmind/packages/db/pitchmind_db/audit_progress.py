"""Redis pub/sub for audit progress (SSE) — avoids polling Postgres."""

from __future__ import annotations

import json
import os

_CHANNEL_PREFIX = "audit:progress:"
TERMINAL_STATUSES = frozenset({"completed", "partial", "failed"})


def _redis_client():
    try:
        import redis

        url = os.environ.get("REDIS_URL", "redis://localhost:6380/0")
        return redis.from_url(url, decode_responses=True)
    except Exception:
        return None


def progress_channel(audit_id: str) -> str:
    return f"{_CHANNEL_PREFIX}{audit_id}"


def publish_audit_progress(
    audit_id: str,
    *,
    status: str,
    query_results_count: int,
) -> None:
    client = _redis_client()
    if not client:
        return
    payload = json.dumps({
        "audit_id": audit_id,
        "status": status,
        "query_results_count": query_results_count,
    })
    try:
        client.publish(progress_channel(audit_id), payload)
    except Exception:
        pass
