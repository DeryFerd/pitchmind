"""FastAPI route tests with dependency overrides."""

from __future__ import annotations

import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from apps.api.deps import get_db
from apps.api.main import app
from apps.api.middleware.auth import AuthUser, get_current_user
from pitchmind_db.base import Base
from pitchmind_db.models import Brand, User, Workspace


@pytest.fixture
def db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def auth_user(db: Session) -> AuthUser:
    user_id = uuid.uuid4()
    db.add(User(id=user_id, email="api@test.com"))
    ws = Workspace(id=uuid.uuid4(), owner_id=user_id, name="Test WS")
    db.add(ws)
    db.add(
        Brand(
            id=uuid.uuid4(),
            workspace_id=ws.id,
            name="PitchMind",
            website_url="https://pitchmind.example.com",
        )
    )
    db.commit()
    return AuthUser(id=user_id, email="api@test.com")


@pytest.fixture
def client(db: Session, auth_user: AuthUser) -> Generator[TestClient, None, None]:
    def override_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = lambda: auth_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_workspaces(client: TestClient):
    response = client.get("/api/v1/workspaces")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test WS"


def test_get_brand_forbidden_for_other_user(db: Session, auth_user: AuthUser):
    other_id = uuid.uuid4()
    db.add(User(id=other_id, email="other@test.com"))
    other_ws = Workspace(id=uuid.uuid4(), owner_id=other_id, name="Other")
    db.add(other_ws)
    other_brand = Brand(
        id=uuid.uuid4(),
        workspace_id=other_ws.id,
        name="OtherBrand",
        website_url="https://other.example.com",
    )
    db.add(other_brand)
    db.commit()

    def override_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = lambda: auth_user
    with TestClient(app) as test_client:
        response = test_client.get(f"/api/v1/brands/{other_brand.id}")
        assert response.status_code == 403
    app.dependency_overrides.clear()
