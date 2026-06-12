import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pitchmind_db.base import Base


class AuditStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class QueryLang(str, enum.Enum):
    EN = "en"
    ID = "id"


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    TEAM = "team"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    locale: Mapped[str] = mapped_column(String(5), default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    workspaces: Mapped[list["Workspace"]] = relationship(back_populates="owner")
    subscription: Mapped["Subscription | None"] = relationship(back_populates="user", uselist=False)


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner: Mapped["User"] = relationship(back_populates="workspaces")
    brands: Mapped[list["Brand"]] = relationship(back_populates="workspace")


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website_url: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    workspace: Mapped["Workspace"] = relationship(back_populates="brands")
    facts: Mapped["BrandFacts | None"] = relationship(back_populates="brand", uselist=False)
    competitors: Mapped[list["Competitor"]] = relationship(back_populates="brand")
    queries: Mapped[list["GoldenQuery"]] = relationship(back_populates="brand")
    audit_runs: Mapped[list["AuditRun"]] = relationship(back_populates="brand")


class BrandFacts(Base):
    __tablename__ = "brand_facts"

    brand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("brands.id"), primary_key=True)
    pricing: Mapped[dict | None] = mapped_column(JSON)
    features: Mapped[list | None] = mapped_column(JSON)
    location: Mapped[str | None] = mapped_column(String(255))
    founded_year: Mapped[int | None] = mapped_column(Integer)

    brand: Mapped["Brand"] = relationship(back_populates="facts")


class Competitor(Base):
    __tablename__ = "competitors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("brands.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website_url: Mapped[str | None] = mapped_column(String(512))

    brand: Mapped["Brand"] = relationship(back_populates="competitors")


class GoldenQuery(Base):
    __tablename__ = "golden_queries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("brands.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    lang: Mapped[QueryLang] = mapped_column(Enum(QueryLang), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="general")
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False)

    brand: Mapped["Brand"] = relationship(back_populates="queries")


class AuditRun(Base):
    __tablename__ = "audit_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("brands.id"), nullable=False)
    status: Mapped[AuditStatus] = mapped_column(Enum(AuditStatus), default=AuditStatus.QUEUED)
    scorecard: Mapped[dict | None] = mapped_column(JSON)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    brand: Mapped["Brand"] = relationship(back_populates="audit_runs")
    query_results: Mapped[list["QueryResult"]] = relationship(back_populates="audit_run")
    site_audit: Mapped["SiteAudit | None"] = relationship(back_populates="audit_run", uselist=False)
    action_plan: Mapped["ActionPlan | None"] = relationship(back_populates="audit_run", uselist=False)


class QueryResult(Base):
    __tablename__ = "query_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audit_runs.id"), nullable=False)
    query_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("golden_queries.id"), nullable=False)
    engine: Mapped[str] = mapped_column(String(50), nullable=False)
    response: Mapped[str | None] = mapped_column(Text)
    brand_mentioned: Mapped[bool] = mapped_column(Boolean, default=False)
    competitors_mentioned: Mapped[dict | None] = mapped_column(JSON)
    citations: Mapped[list | None] = mapped_column(JSON)
    sentiment: Mapped[str | None] = mapped_column(String(20))
    hallucination_flags: Mapped[list | None] = mapped_column(JSON)

    audit_run: Mapped["AuditRun"] = relationship(back_populates="query_results")


class SiteAudit(Base):
    __tablename__ = "site_audits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audit_runs.id"), unique=True, nullable=False)
    readiness_score: Mapped[int] = mapped_column(Integer, default=0)

    audit_run: Mapped["AuditRun"] = relationship(back_populates="site_audit")
    findings: Mapped[list["AuditFinding"]] = relationship(back_populates="site_audit")


class AuditFinding(Base):
    __tablename__ = "audit_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("site_audits.id"), nullable=False)
    check_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str | None] = mapped_column(Text)

    site_audit: Mapped["SiteAudit"] = relationship(back_populates="findings")


class ActionPlan(Base):
    __tablename__ = "action_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audit_runs.id"), unique=True, nullable=False)
    items: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    audit_run: Mapped["AuditRun"] = relationship(back_populates="action_plan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    tier: Mapped[SubscriptionTier] = mapped_column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255))
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(255))
    queries_used_this_period: Mapped[int] = mapped_column(Integer, default=0)
    site_audits_used_this_period: Mapped[int] = mapped_column(Integer, default=0)
    period_reset_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="subscription")
