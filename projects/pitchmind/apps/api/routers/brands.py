import uuid

from fastapi import APIRouter, Depends, HTTPException
from pitchmind_db.models import Brand, BrandFacts, Competitor, GoldenQuery, QueryLang, Workspace
from pitchmind_db.seed_templates import render_templates
from sqlalchemy.orm import Session

from apps.api.deps import get_db, get_owned_brand
from apps.api.middleware.auth import AuthUser, get_current_user
from apps.api.schemas import (
    BrandCreate,
    BrandDetailOut,
    BrandFactsOut,
    BrandOut,
    BrandUpdate,
    CompetitorCreate,
    CompetitorOut,
    GoldenQueryCreate,
    GoldenQueryOut,
    QuerySeedRequest,
)
from apps.api.services.billing import check_brand_limit, check_competitor_limit

router = APIRouter(prefix="/api/v1", tags=["brands"])


def _brand_detail(brand: Brand) -> BrandDetailOut:
    facts_out = None
    if brand.facts:
        facts_out = BrandFactsOut(
            pricing=brand.facts.pricing,
            features=brand.facts.features,
            location=brand.facts.location,
            founded_year=brand.facts.founded_year,
        )
    competitors = [
        CompetitorOut(id=c.id, name=c.name, website_url=c.website_url) for c in brand.competitors
    ]
    return BrandDetailOut(
        id=brand.id,
        workspace_id=brand.workspace_id,
        name=brand.name,
        website_url=brand.website_url,
        description=brand.description,
        facts=facts_out,
        competitors=competitors,
    )


@router.get("/brands/{brand_id}", response_model=BrandDetailOut)
def get_brand(
    brand_id: uuid.UUID,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    brand = get_owned_brand(db, brand_id, auth)
    return _brand_detail(brand)


@router.post("/brands", response_model=BrandOut, status_code=201)
def create_brand(
    body: BrandCreate,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workspace = db.get(Workspace, body.workspace_id)
    if not workspace or workspace.owner_id != auth.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    check_brand_limit(db, auth.id)

    brand = Brand(
        id=uuid.uuid4(),
        workspace_id=body.workspace_id,
        name=body.name,
        website_url=str(body.website_url),
        description=body.description,
    )
    db.add(brand)
    if body.facts:
        db.add(BrandFacts(
            brand_id=brand.id,
            pricing=body.facts.pricing,
            features=body.facts.features,
            location=body.facts.location,
            founded_year=body.facts.founded_year,
        ))
    db.commit()
    db.refresh(brand)
    return brand


@router.patch("/brands/{brand_id}", response_model=BrandOut)
def update_brand(
    brand_id: uuid.UUID,
    body: BrandUpdate,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    brand = get_owned_brand(db, brand_id, auth)
    if body.name is not None:
        brand.name = body.name
    if body.website_url is not None:
        brand.website_url = str(body.website_url)
    if body.description is not None:
        brand.description = body.description
    if body.facts:
        facts = brand.facts or BrandFacts(brand_id=brand.id)
        if body.facts.pricing is not None:
            facts.pricing = body.facts.pricing
        if body.facts.features is not None:
            facts.features = body.facts.features
        if body.facts.location is not None:
            facts.location = body.facts.location
        if body.facts.founded_year is not None:
            facts.founded_year = body.facts.founded_year
        db.merge(facts)
    db.commit()
    db.refresh(brand)
    return brand


@router.post("/brands/{brand_id}/competitors", response_model=CompetitorOut, status_code=201)
def add_competitor(
    brand_id: uuid.UUID,
    body: CompetitorCreate,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_brand(db, brand_id, auth)
    check_competitor_limit(db, auth.id, brand_id)
    competitor = Competitor(
        id=uuid.uuid4(),
        brand_id=brand_id,
        name=body.name,
        website_url=str(body.website_url) if body.website_url else None,
    )
    db.add(competitor)
    db.commit()
    db.refresh(competitor)
    return competitor


@router.delete("/brands/{brand_id}/competitors/{competitor_id}", status_code=204)
def delete_competitor(
    brand_id: uuid.UUID,
    competitor_id: uuid.UUID,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_brand(db, brand_id, auth)
    competitor = db.get(Competitor, competitor_id)
    if not competitor or competitor.brand_id != brand_id:
        raise HTTPException(status_code=404, detail="Competitor not found")
    db.delete(competitor)
    db.commit()


@router.get("/brands/{brand_id}/queries", response_model=list[GoldenQueryOut])
def list_queries(
    brand_id: uuid.UUID,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_brand(db, brand_id, auth)
    return db.query(GoldenQuery).filter(GoldenQuery.brand_id == brand_id).all()


@router.post("/brands/{brand_id}/queries", response_model=GoldenQueryOut, status_code=201)
def add_query(
    brand_id: uuid.UUID,
    body: GoldenQueryCreate,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_brand(db, brand_id, auth)
    query = GoldenQuery(
        id=uuid.uuid4(),
        brand_id=brand_id,
        text=body.text,
        lang=QueryLang(body.lang),
        category=body.category,
        is_custom=True,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


@router.delete("/brands/{brand_id}/queries/{query_id}", status_code=204)
def delete_query(
    brand_id: uuid.UUID,
    query_id: uuid.UUID,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_brand(db, brand_id, auth)
    query = db.get(GoldenQuery, query_id)
    if not query or query.brand_id != brand_id:
        raise HTTPException(status_code=404, detail="Query not found")
    db.delete(query)
    db.commit()


@router.post(
    "/brands/{brand_id}/queries/seed",
    response_model=list[GoldenQueryOut],
    status_code=201,
)
def seed_queries(
    brand_id: uuid.UUID,
    body: QuerySeedRequest,
    auth: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    brand = get_owned_brand(db, brand_id, auth)
    competitors = db.query(Competitor).filter(Competitor.brand_id == brand_id).all()
    competitor_name = competitors[0].name if competitors else "Competitor"

    rendered = render_templates(body.template, brand.name, competitor_name, body.category)
    created = []
    for item in rendered:
        query = GoldenQuery(
            id=uuid.uuid4(),
            brand_id=brand_id,
            text=item["text"],
            lang=QueryLang(item["lang"]),
            category=item["category"],
            is_custom=False,
        )
        db.add(query)
        created.append(query)
    db.commit()
    for q in created:
        db.refresh(q)
    return created
