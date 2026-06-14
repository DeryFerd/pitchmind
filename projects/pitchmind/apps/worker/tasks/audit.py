"""Visibility audit Celery task — visibility + site audit + action plan."""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime

from pitchmind_db.audit_progress import publish_audit_progress
from pitchmind_db.base import get_session_factory
from pitchmind_db.models import (
    ActionPlan,
    AuditFinding,
    AuditRun,
    AuditStatus,
    Brand,
    QueryResult,
    SiteAudit,
)
from pitchmind_geo.action_plan import generate_action_plan
from pitchmind_geo.clients.perplexity import ESTIMATED_COST_PER_QUERY_USD
from pitchmind_geo.hallucination import BrandFactsData
from pitchmind_geo.runner import GoldenQueryInput, run_visibility_batch
from pitchmind_geo.scorer import QueryResultData, compute_scorecard
from pitchmind_site.auditor import run_site_audit
from pitchmind_site.readiness_score import merge_into_scorecard

from apps.worker.celery_app import celery_app


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def _persist_site_audit(session, audit_uuid: uuid.UUID, site_result) -> None:
    site_audit = SiteAudit(
        id=uuid.uuid4(),
        audit_run_id=audit_uuid,
        readiness_score=site_result.readiness_score,
    )
    session.add(site_audit)
    session.flush()

    for finding in site_result.findings:
        session.add(
            AuditFinding(
                id=uuid.uuid4(),
                site_audit_id=site_audit.id,
                check_type=finding.check_type,
                severity=finding.severity,
                message=finding.message,
                recommendation=finding.recommendation,
            )
        )


def _site_findings_dicts(site_result) -> list[dict]:
    return [
        {
            "check_type": f.check_type,
            "severity": f.severity,
            "message": f.message,
            "recommendation": f.recommendation,
        }
        for f in site_result.findings
    ]


@celery_app.task(name="audit.run_visibility", bind=True, max_retries=3)
def run_visibility_audit(
    self,
    audit_run_id: str,
    include_site_audit: bool = True,
    include_action_plan: bool = True,
) -> dict:
    session = get_session_factory()()
    audit_uuid = uuid.UUID(audit_run_id)
    site_findings_data: list[dict] | None = None

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
        publish_audit_progress(
            str(audit_uuid),
            status=AuditStatus.RUNNING.value,
            query_results_count=0,
        )

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

        def _on_query_complete(count: int) -> None:
            publish_audit_progress(
                str(audit_uuid),
                status=AuditStatus.RUNNING.value,
                query_results_count=count,
            )

        parsed = _run_async(
            run_visibility_batch(
                queries,
                brand_name=brand.name,
                brand_website=brand.website_url,
                competitors=competitors,
                facts=facts,
                on_query_complete=_on_query_complete,
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

        readiness_score = None
        if include_site_audit:
            site_result = run_site_audit(brand.website_url)
            _persist_site_audit(session, audit_uuid, site_result)
            site_findings_data = _site_findings_dicts(site_result)
            scorecard = merge_into_scorecard(scorecard, site_result)
            readiness_score = site_result.readiness_score

        total_queries = len(queries)
        completed = len(parsed)
        if completed == 0 and not include_site_audit:
            final_status = AuditStatus.FAILED
        elif completed < total_queries:
            final_status = AuditStatus.PARTIAL
        else:
            final_status = AuditStatus.COMPLETED

        action_plan_source = None
        if include_action_plan and final_status != AuditStatus.FAILED:
            items, action_plan_source = generate_action_plan(
                brand.name,
                scorecard,
                site_findings_data or scorecard.get("site_findings"),
            )
            session.add(
                ActionPlan(
                    id=uuid.uuid4(),
                    audit_run_id=audit_uuid,
                    items=items,
                )
            )
            scorecard["action_plan_source"] = action_plan_source

        audit.status = final_status
        scorecard["estimated_cost_usd"] = round(completed * ESTIMATED_COST_PER_QUERY_USD, 2)
        scorecard["queries_completed"] = completed

        audit.scorecard = scorecard
        audit.completed_at = datetime.now(UTC)
        session.commit()

        publish_audit_progress(
            str(audit_uuid),
            status=final_status.value,
            query_results_count=completed,
        )

        return {
            "audit_run_id": audit_run_id,
            "status": audit.status.value,
            "queries_completed": completed,
            "queries_total": total_queries,
            "share_of_model": scorecard.get("share_of_model"),
            "readiness_score": readiness_score,
            "action_plan_source": action_plan_source,
        }

    except Exception as exc:
        session.rollback()
        audit = session.get(AuditRun, audit_uuid)
        if audit:
            audit.status = AuditStatus.FAILED
            audit.completed_at = datetime.now(UTC)
            session.commit()
            publish_audit_progress(
                str(audit_uuid),
                status=AuditStatus.FAILED.value,
                query_results_count=0,
            )
        raise self.retry(exc=exc, countdown=30) from exc
    finally:
        session.close()
