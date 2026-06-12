import os
import sys

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "packages", "db"))

from pitchmind_db.models import SubscriptionTier

from apps.api.deps import get_db
from apps.api.middleware.auth import AuthUser, get_current_user
from apps.api.schemas import CheckoutRequest, CheckoutResponse, PortalResponse, SubscriptionStatus
from apps.api.services.billing import subscription_status
from apps.api.services.stripe_service import create_checkout_session, create_portal_session

router = APIRouter(prefix="/api/v1/billing", tags=["billing"])


@router.get("/subscription", response_model=SubscriptionStatus)
def get_subscription(
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return subscription_status(db, auth.id)


@router.post("/checkout", response_model=CheckoutResponse)
def start_checkout(
    body: CheckoutRequest,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tier = SubscriptionTier(body.tier)
    url = create_checkout_session(db, auth.id, auth.email, tier, locale=body.locale)
    return CheckoutResponse(checkout_url=url)


@router.post("/portal", response_model=PortalResponse)
def billing_portal(
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    url = create_portal_session(db, auth.id)
    return PortalResponse(portal_url=url)
