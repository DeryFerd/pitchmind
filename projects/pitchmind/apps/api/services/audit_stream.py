"""SSE audit progress via Redis pub/sub with lightweight DB fallback."""

from __future__ import annotations

from collections.abc import AsyncIterator

import asyncio
import json
import uuid

from sqlalchemy.orm import Session

from pitchmind_db.audit_progress import TERMINAL_STATUSES, _redis_client, progress_channel
from pitchmind_db.models import AuditRun, QueryResult


def _progress_payload(audit_id: uuid.UUID, audit: AuditRun, query_count: int) -> dict:
    return {
        "audit_id": str(audit_id),
        "status": audit.status.value,
        "query_results_count": query_count,
    }


async def stream_audit_events(
    db: Session,
    audit_id: uuid.UUID,
    *,
    max_wait_seconds: int = 180,
) -> AsyncIterator[str]:
    audit = db.get(AuditRun, audit_id)
    if not audit:
        return

    count = db.query(QueryResult).filter(QueryResult.audit_run_id == audit_id).count()
    payload = _progress_payload(audit_id, audit, count)
    yield f"data: {json.dumps(payload)}\n\n"

    if audit.status.value in TERMINAL_STATUSES:
        return

    client = _redis_client()
    if client:
        pubsub = client.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe(progress_channel(str(audit_id)))
        iterations = max_wait_seconds // 2
        try:
            for _ in range(iterations):
                msg = await asyncio.to_thread(pubsub.get_message, timeout=2.0)
                if msg and msg.get("type") == "message":
                    yield f"data: {msg['data']}\n\n"
                    data = json.loads(msg["data"])
                    if data.get("status") in TERMINAL_STATUSES:
                        break
        finally:
            pubsub.unsubscribe()
            pubsub.close()
        return

    # Fallback when Redis unavailable: one DB read every 5s (not 2s × 2 queries)
    polls = max_wait_seconds // 5
    for _ in range(polls):
        await asyncio.sleep(5)
        db.expire_all()
        current = db.get(AuditRun, audit_id)
        if not current:
            break
        count = db.query(QueryResult).filter(QueryResult.audit_run_id == audit_id).count()
        payload = _progress_payload(audit_id, current, count)
        yield f"data: {json.dumps(payload)}\n\n"
        if current.status.value in TERMINAL_STATUSES:
            break
