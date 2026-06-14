import uuid
from collections.abc import Generator

from fastapi import HTTPException
from pitchmind_db.base import get_session_factory
from pitchmind_db.models import Brand, Workspace
from sqlalchemy.orm import Session

from apps.api.middleware.auth import AuthUser


def get_db() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def get_owned_brand(db: Session, brand_id: uuid.UUID, auth: AuthUser) -> Brand:
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    workspace = db.get(Workspace, brand.workspace_id)
    if not workspace or workspace.owner_id != auth.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return brand
