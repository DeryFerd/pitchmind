import os
import sys
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "packages", "db"))

from pitchmind_db.models import Subscription, SubscriptionTier, User, Workspace

from apps.api.deps import get_db
from apps.api.middleware.auth import AuthUser, get_current_user
from apps.api.schemas import WorkspaceCreate, WorkspaceOut

router = APIRouter(prefix="/api/v1/workspaces", tags=["workspaces"])


def _ensure_user(db: Session, auth: AuthUser) -> User:
    user = db.get(User, auth.id)
    if not user:
        user = User(id=auth.id, email=auth.email)
        db.add(user)
        db.add(Subscription(user_id=auth.id, tier=SubscriptionTier.FREE))
        db.commit()
        db.refresh(user)
    return user


@router.post("", response_model=WorkspaceOut, status_code=201)
def create_workspace(
    body: WorkspaceCreate,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_user(db, auth)
    workspace = Workspace(id=uuid.uuid4(), owner_id=auth.id, name=body.name)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


@router.get("", response_model=list[WorkspaceOut])
def list_workspaces(
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_user(db, auth)
    return db.query(Workspace).filter(Workspace.owner_id == auth.id).all()
