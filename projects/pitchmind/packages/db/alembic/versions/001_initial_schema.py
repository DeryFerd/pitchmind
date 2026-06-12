"""Initial schema: users through subscriptions

Revision ID: 001
Revises:
Create Date: 2026-06-11

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("locale", sa.String(5), server_default="en"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "workspaces",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "brands",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("workspaces.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("website_url", sa.String(512), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "brand_facts",
        sa.Column("brand_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("brands.id"), primary_key=True),
        sa.Column("pricing", postgresql.JSON),
        sa.Column("features", postgresql.JSON),
        sa.Column("location", sa.String(255)),
        sa.Column("founded_year", sa.Integer),
    )
    op.create_table(
        "competitors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("brand_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("brands.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("website_url", sa.String(512)),
    )
    op.create_table(
        "golden_queries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("brand_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("brands.id"), nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("lang", sa.Enum("en", "id", name="querylang"), nullable=False),
        sa.Column("category", sa.String(50), server_default="general"),
        sa.Column("is_custom", sa.Boolean, server_default="false"),
    )
    op.create_table(
        "audit_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("brand_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("brands.id"), nullable=False),
        sa.Column("status", sa.Enum("queued", "running", "completed", "failed", "partial", name="auditstatus"), server_default="queued"),
        sa.Column("scorecard", postgresql.JSON),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "query_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("audit_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("audit_runs.id"), nullable=False),
        sa.Column("query_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("golden_queries.id"), nullable=False),
        sa.Column("engine", sa.String(50), nullable=False),
        sa.Column("response", sa.Text),
        sa.Column("brand_mentioned", sa.Boolean, server_default="false"),
        sa.Column("competitors_mentioned", postgresql.JSON),
        sa.Column("citations", postgresql.JSON),
        sa.Column("sentiment", sa.String(20)),
        sa.Column("hallucination_flags", postgresql.JSON),
    )
    op.create_table(
        "site_audits",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("audit_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("audit_runs.id"), unique=True, nullable=False),
        sa.Column("readiness_score", sa.Integer, server_default="0"),
    )
    op.create_table(
        "audit_findings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("site_audit_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("site_audits.id"), nullable=False),
        sa.Column("check_type", sa.String(50), nullable=False),
        sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("recommendation", sa.Text),
    )
    op.create_table(
        "action_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("audit_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("audit_runs.id"), unique=True, nullable=False),
        sa.Column("items", postgresql.JSON, nullable=False, server_default="[]"),
    )
    op.create_table(
        "subscriptions",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("tier", sa.Enum("free", "pro", "team", name="subscriptiontier"), server_default="free"),
        sa.Column("stripe_customer_id", sa.String(255)),
        sa.Column("queries_used_this_period", sa.Integer, server_default="0"),
        sa.Column("period_reset_at", sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table("subscriptions")
    op.drop_table("action_plans")
    op.drop_table("audit_findings")
    op.drop_table("site_audits")
    op.drop_table("query_results")
    op.drop_table("audit_runs")
    op.drop_table("golden_queries")
    op.drop_table("competitors")
    op.drop_table("brand_facts")
    op.drop_table("brands")
    op.drop_table("workspaces")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS subscriptiontier")
    op.execute("DROP TYPE IF EXISTS auditstatus")
    op.execute("DROP TYPE IF EXISTS querylang")
