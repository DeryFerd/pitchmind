"""Audit tasks — full implementation in Phase 2."""

from apps.worker.celery_app import celery_app


@celery_app.task(name="audit.run_visibility", bind=True, max_retries=3)
def run_visibility_audit(self, audit_run_id: str) -> dict:
    """Placeholder: Perplexity batch + scoring (Phase 2)."""
    return {"audit_run_id": audit_run_id, "status": "queued", "message": "Phase 2 not implemented"}
