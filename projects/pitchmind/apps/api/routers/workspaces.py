import uuid

from fastapi import APIRouter, Depends, HTTPException
from pitchmind_db.models import Brand, Subscription, SubscriptionTier, User, Workspace
from sqlalchemy.orm import Session

from apps.api.deps import get_db
from apps.api.middleware.auth import AuthUser, get_current_user
from apps.api.schemas import BrandOut, WorkspaceCreate, WorkspaceOut

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


@router.get("/{workspace_id}/brands", response_model=list[BrandOut])
def list_workspace_brands(
    workspace_id: uuid.UUID,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workspace = db.get(Workspace, workspace_id)
    if not workspace or workspace.owner_id != auth.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(Brand).filter(Brand.workspace_id == workspace_id).all()
