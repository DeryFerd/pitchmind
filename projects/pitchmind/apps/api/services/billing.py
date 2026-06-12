"""Subscription tier limits and usage enforcement."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pitchmind_db.models import Brand, Subscription, SubscriptionTier, User, Workspace


@dataclass(frozen=True)
class TierLimits:
    max_brands: int
    queries_per_month: int
    queries_per_audit: int
    site_audits_per_month: int


TIER_LIMITS: dict[SubscriptionTier, TierLimits] = {
    SubscriptionTier.FREE: TierLimits(
        max_brands=1,
        queries_per_month=10,
        queries_per_audit=5,
        site_audits_per_month=1,
    ),
    SubscriptionTier.PRO: TierLimits(
        max_brands=5,
        queries_per_month=200,
        queries_per_audit=50,
        site_audits_per_month=4,
    ),
    SubscriptionTier.TEAM: TierLimits(
        max_brands=20,
        queries_per_month=1000,
        queries_per_audit=100,
        site_audits_per_month=20,
    ),
}

BILLING_PERIOD_DAYS = 30


def get_or_create_subscription(db: Session, user_id: UUID) -> Subscription:
    sub = db.get(Subscription, user_id)
    if sub:
        return sub

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sub = Subscription(
        user_id=user_id,
        tier=SubscriptionTier.FREE,
        queries_used_this_period=0,
        site_audits_used_this_period=0,
        period_reset_at=_next_period_reset(),
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def _next_period_reset(now: datetime | None = None) -> datetime:
    base = now or datetime.now(UTC)
    return base + timedelta(days=BILLING_PERIOD_DAYS)


def maybe_reset_period(db: Session, sub: Subscription) -> None:
    now = datetime.now(UTC)
    reset_at = sub.period_reset_at
    if reset_at is not None and reset_at.tzinfo is None:
        reset_at = reset_at.replace(tzinfo=UTC)

    if reset_at is None or now >= reset_at:
        sub.queries_used_this_period = 0
        sub.site_audits_used_this_period = 0
        sub.period_reset_at = _next_period_reset(now)
        db.commit()
        db.refresh(sub)


def get_tier_limits(tier: SubscriptionTier) -> TierLimits:
    return TIER_LIMITS[tier]


def count_user_brands(db: Session, user_id: UUID) -> int:
    return (
        db.query(Brand)
        .join(Workspace, Brand.workspace_id == Workspace.id)
        .filter(Workspace.owner_id == user_id)
        .count()
    )


def check_brand_limit(db: Session, user_id: UUID) -> None:
    sub = get_or_create_subscription(db, user_id)
    maybe_reset_period(db, sub)
    limits = get_tier_limits(sub.tier)
    current = count_user_brands(db, user_id)
    if current >= limits.max_brands:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"{sub.tier.value.title()} tier limited to {limits.max_brands} brand(s). Upgrade to add more.",
        )


def check_audit_limits(
    db: Session,
    user_id: UUID,
    query_count: int,
    include_site_audit: bool,
) -> None:
    sub = get_or_create_subscription(db, user_id)
    maybe_reset_period(db, sub)
    limits = get_tier_limits(sub.tier)

    if query_count > limits.queries_per_audit:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=(
                f"{sub.tier.value.title()} tier limited to {limits.queries_per_audit} "
                f"queries per audit. Upgrade for higher limits."
            ),
        )

    remaining_queries = limits.queries_per_month - sub.queries_used_this_period
    if query_count > remaining_queries:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=(
                f"Monthly query limit reached ({sub.queries_used_this_period}/"
                f"{limits.queries_per_month}). Upgrade for more queries."
            ),
        )

    if include_site_audit:
        remaining_site = limits.site_audits_per_month - sub.site_audits_used_this_period
        if remaining_site <= 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=(
                    f"Monthly site audit limit reached ({sub.site_audits_used_this_period}/"
                    f"{limits.site_audits_per_month}). Upgrade for more site audits."
                ),
            )


def record_audit_usage(
    db: Session,
    user_id: UUID,
    query_count: int,
    include_site_audit: bool,
) -> None:
    sub = get_or_create_subscription(db, user_id)
    maybe_reset_period(db, sub)
    sub.queries_used_this_period += query_count
    if include_site_audit:
        sub.site_audits_used_this_period += 1
    db.commit()


def subscription_status(db: Session, user_id: UUID) -> dict:
    sub = get_or_create_subscription(db, user_id)
    maybe_reset_period(db, sub)
    limits = get_tier_limits(sub.tier)
    return {
        "tier": sub.tier.value,
        "queries_used": sub.queries_used_this_period,
        "queries_limit": limits.queries_per_month,
        "site_audits_used": sub.site_audits_used_this_period,
        "site_audits_limit": limits.site_audits_per_month,
        "brands_used": count_user_brands(db, user_id),
        "brands_limit": limits.max_brands,
        "period_reset_at": sub.period_reset_at.isoformat() if sub.period_reset_at else None,
        "has_stripe_customer": bool(sub.stripe_customer_id),
    }


def reset_all_periods(db: Session) -> int:
    """Reset usage counters for subscriptions past their billing period."""
    now = datetime.now(UTC)
    subs = db.query(Subscription).all()
    reset_count = 0
    for sub in subs:
        reset_at = sub.period_reset_at
        if reset_at is not None and reset_at.tzinfo is None:
            reset_at = reset_at.replace(tzinfo=UTC)
        if reset_at is None or now >= reset_at:
            sub.queries_used_this_period = 0
            sub.site_audits_used_this_period = 0
            sub.period_reset_at = _next_period_reset(now)
            reset_count += 1
    if reset_count:
        db.commit()
    return reset_count
