import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "db"))

from apps.api.config import settings
from apps.api.routers import audits, brands, workspaces

app = FastAPI(
    title="PitchMind API",
    description="GEO audit platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workspaces.router)
app.include_router(brands.router)
app.include_router(audits.router)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("apps.api.main:app", host=settings.api_host, port=settings.api_port, reload=True)
