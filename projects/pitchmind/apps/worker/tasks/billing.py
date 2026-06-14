"""Reset subscription usage counters for expired billing periods."""

from __future__ import annotations

import logging

from pitchmind_db.base import get_session_factory

from apps.api.services.billing import reset_all_periods
from apps.worker.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="billing.reset_usage_periods")
def reset_usage_periods() -> dict:
    db = get_session_factory()()
    try:
        count = reset_all_periods(db)
        logger.info("Reset billing periods for %s subscriptions", count)
        return {"reset_count": count}
    finally:
        db.close()
