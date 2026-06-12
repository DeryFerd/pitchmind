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
