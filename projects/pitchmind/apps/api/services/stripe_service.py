"""Stripe Checkout and Customer Portal helpers."""

from __future__ import annotations

from uuid import UUID

import stripe
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pitchmind_db.models import Subscription, SubscriptionTier, User

from apps.api.config import settings
from apps.api.services.billing import get_or_create_subscription

stripe.api_key = settings.stripe_secret_key


def _require_stripe() -> None:
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe is not configured",
        )


def _price_id_for_tier(tier: SubscriptionTier) -> str:
    if tier == SubscriptionTier.PRO:
        price_id = settings.stripe_price_id_pro
    elif tier == SubscriptionTier.TEAM:
        price_id = settings.stripe_price_id_team
    else:
        raise HTTPException(status_code=400, detail="Cannot checkout for free tier")

    if not price_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Stripe price ID not configured for {tier.value} tier",
        )
    return price_id


def _tier_for_price_id(price_id: str) -> SubscriptionTier | None:
    if price_id == settings.stripe_price_id_pro:
        return SubscriptionTier.PRO
    if price_id == settings.stripe_price_id_team:
        return SubscriptionTier.TEAM
    return None


def ensure_stripe_customer(db: Session, user_id: UUID, email: str) -> str:
    _require_stripe()
    sub = get_or_create_subscription(db, user_id)
    if sub.stripe_customer_id:
        return sub.stripe_customer_id

    customer = stripe.Customer.create(
        email=email,
        metadata={"user_id": str(user_id)},
    )
    sub.stripe_customer_id = customer.id
    db.commit()
    return customer.id


def create_checkout_session(
    db: Session,
    user_id: UUID,
    email: str,
    tier: SubscriptionTier,
    locale: str = "en",
) -> str:
    _require_stripe()
    if tier == SubscriptionTier.FREE:
        raise HTTPException(status_code=400, detail="Use customer portal to cancel paid plans")

    customer_id = ensure_stripe_customer(db, user_id, email)
    price_id = _price_id_for_tier(tier)
    success_url = f"{settings.web_url}/{locale}/dashboard/settings?billing=success"
    cancel_url = f"{settings.web_url}/{locale}/dashboard/settings?billing=cancel"

    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"user_id": str(user_id), "tier": tier.value},
        subscription_data={"metadata": {"user_id": str(user_id), "tier": tier.value}},
    )
    if not session.url:
        raise HTTPException(status_code=500, detail="Failed to create checkout session")
    return session.url


def create_portal_session(db: Session, user_id: UUID) -> str:
    _require_stripe()
    sub = get_or_create_subscription(db, user_id)
    if not sub.stripe_customer_id:
        raise HTTPException(
            status_code=400,
            detail="No billing account yet. Upgrade to Pro or Team first.",
        )

    session = stripe.billing_portal.Session.create(
        customer=sub.stripe_customer_id,
        return_url=f"{settings.web_url}/en/dashboard/settings",
    )
    return session.url


def apply_subscription_tier(
    db: Session,
    user_id: UUID,
    tier: SubscriptionTier,
    stripe_customer_id: str | None = None,
    stripe_subscription_id: str | None = None,
) -> None:
    sub = get_or_create_subscription(db, user_id)
    sub.tier = tier
    if stripe_customer_id:
        sub.stripe_customer_id = stripe_customer_id
    if stripe_subscription_id:
        sub.stripe_subscription_id = stripe_subscription_id
    db.commit()


def handle_checkout_completed(db: Session, session: dict) -> None:
    user_id_raw = session.get("metadata", {}).get("user_id")
    tier_raw = session.get("metadata", {}).get("tier")
    if not user_id_raw or not tier_raw:
        return

    user_id = UUID(user_id_raw)
    tier = SubscriptionTier(tier_raw)
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")
    apply_subscription_tier(
        db,
        user_id,
        tier,
        stripe_customer_id=customer_id,
        stripe_subscription_id=subscription_id,
    )


def handle_subscription_updated(db: Session, subscription: dict) -> None:
    user_id_raw = subscription.get("metadata", {}).get("user_id")
    status_value = subscription.get("status")
    customer_id = subscription.get("customer")
    subscription_id = subscription.get("id")

    if status_value in ("canceled", "unpaid", "incomplete_expired"):
        if user_id_raw:
            apply_subscription_tier(
                db,
                UUID(user_id_raw),
                SubscriptionTier.FREE,
                stripe_customer_id=customer_id,
                stripe_subscription_id=None,
            )
        return

    if status_value not in ("active", "trialing"):
        return

    items = subscription.get("items", {}).get("data", [])
    if not items:
        return

    price_id = items[0].get("price", {}).get("id")
    tier = _tier_for_price_id(price_id) if price_id else None
    if not tier and user_id_raw:
        tier_raw = subscription.get("metadata", {}).get("tier")
        if tier_raw:
            tier = SubscriptionTier(tier_raw)

    if not tier or not user_id_raw:
        return

    apply_subscription_tier(
        db,
        UUID(user_id_raw),
        tier,
        stripe_customer_id=customer_id,
        stripe_subscription_id=subscription_id,
    )


def handle_subscription_deleted(db: Session, subscription: dict) -> None:
    user_id_raw = subscription.get("metadata", {}).get("user_id")
    customer_id = subscription.get("customer")
    if not user_id_raw:
        return

    apply_subscription_tier(
        db,
        UUID(user_id_raw),
        SubscriptionTier.FREE,
        stripe_customer_id=customer_id,
        stripe_subscription_id=None,
    )


def resolve_user_from_customer(db: Session, customer_id: str | None) -> UUID | None:
    if not customer_id:
        return None
    sub = db.query(Subscription).filter(Subscription.stripe_customer_id == customer_id).first()
    if sub:
        return sub.user_id

    user = db.query(User).join(Subscription).filter(Subscription.stripe_customer_id == customer_id).first()
    if user:
        return user.id
    return None
