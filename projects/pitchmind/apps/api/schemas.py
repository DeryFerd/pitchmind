from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class WorkspaceOut(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class BrandFactsIn(BaseModel):
    pricing: dict | None = None
    features: list[str] | None = None
    location: str | None = None
    founded_year: int | None = None


class BrandCreate(BaseModel):
    workspace_id: UUID
    name: str = Field(min_length=1, max_length=255)
    website_url: HttpUrl
    description: str | None = None
    facts: BrandFactsIn | None = None


class BrandUpdate(BaseModel):
    name: str | None = None
    website_url: HttpUrl | None = None
    description: str | None = None
    facts: BrandFactsIn | None = None


class BrandOut(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    website_url: str
    description: str | None

    model_config = {"from_attributes": True}


class CompetitorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    website_url: HttpUrl | None = None


class CompetitorOut(BaseModel):
    id: UUID
    name: str
    website_url: str | None

    model_config = {"from_attributes": True}


class GoldenQueryOut(BaseModel):
    id: UUID
    text: str
    lang: str
    category: str
    is_custom: bool

    model_config = {"from_attributes": True}


class QuerySeedRequest(BaseModel):
    template: str = Field(pattern="^(saas|local|ecom)$")
    category: str = "software"


class GoldenQueryCreate(BaseModel):
    text: str = Field(min_length=5, max_length=500)
    lang: str = Field(pattern="^(en|id)$")
    category: str = "custom"


class AuditCreate(BaseModel):
    engines: list[str] = ["perplexity"]
    languages: list[str] = Field(default=["en", "id"])
    include_site_audit: bool = False
    include_action_plan: bool = False


class AuditOut(BaseModel):
    audit_id: UUID
    brand_id: UUID
    status: str
    estimated_duration_seconds: int


class AuditSummary(BaseModel):
    audit_id: UUID
    brand_id: UUID
    status: str
    scorecard: dict | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    query_results_count: int = 0
    readiness_score: int | None = None
    site_findings_count: int = 0


class SiteFindingOut(BaseModel):
    check_type: str
    severity: str
    message: str
    recommendation: str | None = None


class QueryResultOut(BaseModel):
    id: UUID
    query_text: str
    engine: str
    brand_mentioned: bool
    sentiment: str | None = None
    citations: list | None = None
    hallucination_flags: list | None = None
    competitors_mentioned: dict | None = None


class AuditDetail(AuditSummary):
    query_results: list[QueryResultOut] = []
    site_findings: list[SiteFindingOut] = []
