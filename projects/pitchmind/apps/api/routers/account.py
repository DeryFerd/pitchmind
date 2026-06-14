from fastapi import APIRouter, Depends
from pitchmind_db.models import User
from sqlalchemy.orm import Session

from apps.api.deps import get_db
from apps.api.middleware.auth import AuthUser, get_current_user
from apps.api.schemas import EmailPrefsUpdate

router = APIRouter(prefix="/api/v1/account", tags=["account"])


@router.patch("/email-preferences")
def update_email_preferences(
    body: EmailPrefsUpdate,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.get(User, auth.id)
    if not user:
        user = User(id=auth.id, email=auth.email, email_digest_enabled=body.email_digest_enabled)
        db.add(user)
    else:
        user.email_digest_enabled = body.email_digest_enabled
    db.commit()
    return {"email_digest_enabled": body.email_digest_enabled}


@router.get("/email-preferences")
def get_email_preferences(
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.get(User, auth.id)
    enabled = user.email_digest_enabled if user else True
    return {"email_digest_enabled": enabled}
