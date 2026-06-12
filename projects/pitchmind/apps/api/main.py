import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "db"))

from apps.api.config import settings
from apps.api.middleware.rate_limit import RateLimitMiddleware
from apps.api.routers import audits, billing, brands, webhooks, workspaces

app = FastAPI(
    title="PitchMind API",
    description="GEO audit platform API",
    version="0.1.0",
)

cors_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)

app.include_router(workspaces.router)
app.include_router(brands.router)
app.include_router(audits.router)
app.include_router(billing.router)
app.include_router(webhooks.router)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("apps.api.main:app", host=settings.api_host, port=settings.api_port, reload=True)
