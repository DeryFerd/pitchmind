"""Unit tests for subscription tier limits."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from pitchmind_db.base import Base
from pitchmind_db.models import Brand, Subscription, SubscriptionTier, User, Workspace

from apps.api.services.billing import (
    check_audit_limits,
    check_brand_limit,
    get_tier_limits,
    maybe_reset_period,
    record_audit_usage,
    subscription_status,
)


@pytest.fixture
def db() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


def _seed_user(db: Session, tier: SubscriptionTier = SubscriptionTier.FREE) -> uuid.UUID:
    user_id = uuid.uuid4()
    db.add(User(id=user_id, email="test@example.com"))
    db.add(
        Subscription(
            user_id=user_id,
            tier=tier,
            queries_used_this_period=0,
            site_audits_used_this_period=0,
            period_reset_at=datetime.now(UTC) + timedelta(days=30),
        )
    )
    db.commit()
    return user_id


def _add_brand(db: Session, user_id: uuid.UUID, name: str = "Acme") -> Brand:
    ws = Workspace(id=uuid.uuid4(), owner_id=user_id, name="WS")
    db.add(ws)
    brand = Brand(
        id=uuid.uuid4(),
        workspace_id=ws.id,
        name=name,
        website_url="https://acme.com",
    )
    db.add(brand)
    db.commit()
    return brand


def test_free_tier_limits():
    limits = get_tier_limits(SubscriptionTier.FREE)
    assert limits.max_brands == 1
    assert limits.max_competitors == 2
    assert limits.queries_per_month == 10
    assert limits.queries_per_audit == 5
    assert limits.weekly_email is False


def test_brand_limit_blocks_second_brand(db: Session):
    user_id = _seed_user(db)
    _add_brand(db, user_id)
    with pytest.raises(HTTPException) as exc:
        check_brand_limit(db, user_id)
    assert exc.value.status_code == 402


def test_audit_monthly_query_limit(db: Session):
    user_id = _seed_user(db)
    sub = db.get(Subscription, user_id)
    sub.queries_used_this_period = 8
    db.commit()

    with pytest.raises(HTTPException) as exc:
        check_audit_limits(db, user_id, query_count=5, include_site_audit=False)
    assert exc.value.status_code == 402
    assert "Monthly query limit" in exc.value.detail


def test_record_audit_usage_increments_counters(db: Session):
    user_id = _seed_user(db)
    record_audit_usage(db, user_id, query_count=3, include_site_audit=True)
    sub = db.get(Subscription, user_id)
    assert sub.queries_used_this_period == 3
    assert sub.site_audits_used_this_period == 1


def test_period_reset_clears_usage(db: Session):
    user_id = _seed_user(db)
    sub = db.get(Subscription, user_id)
    sub.queries_used_this_period = 7
    sub.site_audits_used_this_period = 1
    sub.period_reset_at = datetime.now(UTC) - timedelta(days=1)
    db.commit()

    maybe_reset_period(db, sub)
    db.refresh(sub)
    assert sub.queries_used_this_period == 0
    assert sub.site_audits_used_this_period == 0


def test_subscription_status_shape(db: Session):
    user_id = _seed_user(db, SubscriptionTier.PRO)
    _add_brand(db, user_id)
    status = subscription_status(db, user_id)
    assert status["tier"] == "pro"
    assert status["brands_used"] == 1
    assert status["queries_limit"] == 200
