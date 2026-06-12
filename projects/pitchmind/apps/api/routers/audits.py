import os
import sys
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "packages", "db"))

from pitchmind_db.models import (
    AuditRun,
    AuditStatus,
    Brand,
    QueryResult,
    Subscription,
    SubscriptionTier,
    Workspace,
)

from apps.api.deps import get_db
from apps.api.middleware.auth import AuthUser, get_current_user
from apps.api.schemas import AuditCreate, AuditOut, AuditSummary

router = APIRouter(prefix="/api/v1", tags=["audits"])

FREE_TIER_MAX_QUERIES = 5
ESTIMATED_SECONDS_PER_QUERY = 8
SITE_AUDIT_SECONDS = 30


def _audit_summary(audit: AuditRun, query_count: int) -> AuditSummary:
    readiness = None
    if audit.scorecard:
        readiness = audit.scorecard.get("readiness_score")
    site_findings = len(audit.site_audit.findings) if audit.site_audit else 0
    if not site_findings and audit.scorecard:
        site_findings = len(audit.scorecard.get("site_findings", []))
    return AuditSummary(
        audit_id=audit.id,
        brand_id=audit.brand_id,
        status=audit.status.value,
        scorecard=audit.scorecard,
        started_at=audit.started_at,
        completed_at=audit.completed_at,
        query_results_count=query_count,
        readiness_score=readiness,
        site_findings_count=site_findings,
    )


def _get_owned_brand(db: Session, brand_id: uuid.UUID, auth: AuthUser) -> Brand:
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    workspace = db.get(Workspace, brand.workspace_id)
    if not workspace or workspace.owner_id != auth.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return brand


def _check_tier_limits(db: Session, auth: AuthUser, query_count: int) -> None:
    sub = db.get(Subscription, auth.id)
    tier = sub.tier if sub else SubscriptionTier.FREE
    if tier == SubscriptionTier.FREE and query_count > FREE_TIER_MAX_QUERIES:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Free tier limited to {FREE_TIER_MAX_QUERIES} queries per audit",
        )


@router.post(
    "/brands/{brand_id}/audits",
    response_model=AuditOut,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_audit(
    brand_id: uuid.UUID,
    body: AuditCreate,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    brand = _get_owned_brand(db, brand_id, auth)

    running = (
        db.query(AuditRun)
        .filter(
            AuditRun.brand_id == brand_id,
            AuditRun.status.in_([AuditStatus.QUEUED, AuditStatus.RUNNING]),
        )
        .first()
    )
    if running:
        raise HTTPException(status_code=409, detail="Audit already in progress for this brand")

    queries = [q for q in brand.queries if q.lang.value in body.languages]
    if not queries:
        raise HTTPException(status_code=400, detail="No golden queries for requested languages")

    _check_tier_limits(db, auth, len(queries))

    audit = AuditRun(
        id=uuid.uuid4(),
        brand_id=brand_id,
        status=AuditStatus.QUEUED,
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)

    from apps.worker.tasks.audit import run_visibility_audit

    run_visibility_audit.delay(str(audit.id), include_site_audit=body.include_site_audit)

    estimated = len(queries) * ESTIMATED_SECONDS_PER_QUERY
    if body.include_site_audit:
        estimated += SITE_AUDIT_SECONDS

    return AuditOut(
        audit_id=audit.id,
        brand_id=brand_id,
        status=audit.status.value,
        estimated_duration_seconds=estimated,
    )


@router.get("/audits/{audit_id}", response_model=AuditSummary)
def get_audit(
    audit_id: uuid.UUID,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    audit = db.get(AuditRun, audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    _get_owned_brand(db, audit.brand_id, auth)

    results = db.query(QueryResult).filter(QueryResult.audit_run_id == audit_id).all()
    return _audit_summary(audit, len(results))


@router.get("/brands/{brand_id}/audits", response_model=list[AuditSummary])
def list_audits(
    brand_id: uuid.UUID,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_owned_brand(db, brand_id, auth)
    audits = (
        db.query(AuditRun)
        .filter(AuditRun.brand_id == brand_id)
        .order_by(AuditRun.created_at.desc())
        .limit(20)
        .all()
    )
    return [_audit_summary(a, len(a.query_results)) for a in audits]


@router.get("/brands/{brand_id}/scorecard")
def get_latest_scorecard(
    brand_id: uuid.UUID,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_owned_brand(db, brand_id, auth)
    audit = (
        db.query(AuditRun)
        .filter(
            AuditRun.brand_id == brand_id,
            AuditRun.status.in_([AuditStatus.COMPLETED, AuditStatus.PARTIAL]),
        )
        .order_by(AuditRun.completed_at.desc())
        .first()
    )
    if not audit or not audit.scorecard:
        raise HTTPException(status_code=404, detail="No scorecard available")
    return {"brand_id": brand_id, "audit_id": audit.id, "scorecard": audit.scorecard}
