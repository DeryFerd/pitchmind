"""Visibility audit Celery task — Perplexity batch + scoring."""

from __future__ import annotations

import asyncio
import os
import sys
import uuid
from datetime import UTC, datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "packages", "db"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "packages", "geo-engine"))

from pitchmind_db.base import get_session_factory
from pitchmind_db.models import AuditRun, AuditStatus, Brand, QueryResult
from pitchmind_geo.hallucination import BrandFactsData
from pitchmind_geo.runner import GoldenQueryInput, run_visibility_batch
from pitchmind_geo.scorer import QueryResultData, compute_scorecard

from apps.worker.celery_app import celery_app


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="audit.run_visibility", bind=True, max_retries=3)
def run_visibility_audit(self, audit_run_id: str) -> dict:
    session = get_session_factory()()
    audit_uuid = uuid.UUID(audit_run_id)

    try:
        audit = session.get(AuditRun, audit_uuid)
        if not audit:
            return {"error": "audit not found"}

        brand = session.get(Brand, audit.brand_id)
        if not brand:
            audit.status = AuditStatus.FAILED
            session.commit()
            return {"error": "brand not found"}

        audit.status = AuditStatus.RUNNING
        audit.started_at = datetime.now(UTC)
        session.commit()

        competitors = [c.name for c in brand.competitors]
        facts = None
        if brand.facts:
            facts = BrandFactsData(
                pricing=brand.facts.pricing,
                features=brand.facts.features,
                location=brand.facts.location,
                founded_year=brand.facts.founded_year,
            )

        queries = [
            GoldenQueryInput(id=q.id, text=q.text, lang=q.lang.value) for q in brand.queries
        ]

        parsed = _run_async(
            run_visibility_batch(
                queries,
                brand_name=brand.name,
                brand_website=brand.website_url,
                competitors=competitors,
                facts=facts,
            )
        )

        for item in parsed:
            session.add(
                QueryResult(
                    id=uuid.uuid4(),
                    audit_run_id=audit_uuid,
                    query_id=item.query_id,
                    engine=item.engine,
                    response=item.response,
                    brand_mentioned=item.brand_mentioned,
                    competitors_mentioned=item.competitors_mentioned,
                    citations=item.citations,
                    sentiment=item.sentiment,
                    hallucination_flags=item.hallucination_flags,
                )
            )

        scorecard_input = [
            QueryResultData(
                brand_mentioned=p.brand_mentioned,
                competitors_mentioned=p.competitors_mentioned,
                hallucination_flags=p.hallucination_flags,
                sentiment=p.sentiment,
            )
            for p in parsed
        ]
        scorecard = compute_scorecard(scorecard_input, brand.name, competitors)

        total_queries = len(queries)
        completed = len(parsed)
        if completed == 0:
            audit.status = AuditStatus.FAILED
        elif completed < total_queries:
            audit.status = AuditStatus.PARTIAL
        else:
            audit.status = AuditStatus.COMPLETED

        audit.scorecard = scorecard
        audit.completed_at = datetime.now(UTC)
        session.commit()

        return {
            "audit_run_id": audit_run_id,
            "status": audit.status.value,
            "queries_completed": completed,
            "queries_total": total_queries,
            "share_of_model": scorecard.get("share_of_model"),
        }

    except Exception as exc:
        session.rollback()
        audit = session.get(AuditRun, audit_uuid)
        if audit:
            audit.status = AuditStatus.FAILED
            audit.completed_at = datetime.now(UTC)
            session.commit()
        raise self.retry(exc=exc, countdown=30) from exc
    finally:
        session.close()
