"""Response cache for Perplexity queries (7-day TTL)."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime

CACHE_TTL_SECONDS = 7 * 24 * 3600
_KEY_PREFIX = "pplx:"


def _cache_key(query: str, engine: str) -> str:
    bucket = datetime.now(UTC).strftime("%Y-%W")
    digest = hashlib.sha256(f"{query}:{engine}:{bucket}".encode()).hexdigest()
    return f"{_KEY_PREFIX}{digest}"


def _get_redis():
    try:
        import redis

        url = os.environ.get("REDIS_URL", "redis://localhost:6380/0")
        return redis.from_url(url, decode_responses=True)
    except Exception:
        return None


def get_cached_response(query: str, engine: str = "perplexity") -> dict | None:
    client = _get_redis()
    if not client:
        return None
    try:
        raw = client.get(_cache_key(query, engine))
        return json.loads(raw) if raw else None
    except Exception:
        return None


def set_cached_response(query: str, payload: dict, engine: str = "perplexity") -> None:
    client = _get_redis()
    if not client:
        return
    try:
        client.setex(_cache_key(query, engine), CACHE_TTL_SECONDS, json.dumps(payload))
    except Exception:
        pass
