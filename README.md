# PitchMind

**GEO (Generative Engine Optimization) SaaS** — measure and improve how AI search engines (ChatGPT, Perplexity, Gemini) cite and recommend your brand.

Bilingual EN + ID · Perplexity + Ollama Cloud · Full-stack production portfolio project.

## Status

**MVP ~95% complete** — core product shipped in code; production deploy + beta pending.  
Stripe billing implemented in code but **not live** (skipped by choice).

| Area | Status |
|------|--------|
| Audit pipeline (visibility → site → action plan → PDF) | Done |
| Dashboard + brand settings + i18n (EN/ID) | Done |
| Tier limits + billing API | Done (Stripe live deferred) |
| Deploy + beta (Phase 7) | Pending |

## Quick start

```bash
cd projects/pitchmind
cp .env.example .env          # fill SUPABASE_JWT_SECRET, etc.
make dev-up && make migrate   # Postgres + Redis
make api && make worker && make web
pytest tests/                 # 26 passed
```

See [handoff.md](projects/pitchmind/handoff.md) for full env vars and deploy notes.

## Repository layout

```
SaaS ML-AI-DL/
├── README.md                   # This file
├── STRUCTURE.md                # Final architecture map (layers + connections)
├── docs/                       # Portfolio research
├── .github/workflows/ci.yml    # Lint + build (web + API)
└── projects/pitchmind/         # PitchMind application (monorepo)
    ├── apps/
    │   ├── web/                # Next.js 15 frontend
    │   ├── api/                # FastAPI REST gateway
    │   └── worker/             # Celery async jobs + beat
    ├── packages/               # Shared Python libraries
    │   ├── db/                 # SQLAlchemy models + Alembic
    │   ├── geo-engine/         # Perplexity scan, scorer, action plan
    │   ├── site-auditor/       # Website GEO readiness checks
    │   └── harness/            # Retry helpers
    ├── infra/                  # docker-compose, Railway configs
    ├── tests/                  # unit + integration
    └── *.md                    # PRD, Plan, progress, handoff, memory
```

Full layer diagram, connection map, and API ↔ UI mapping → **[STRUCTURE.md](STRUCTURE.md)**

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, next-intl, Tailwind, Supabase Auth client |
| API | FastAPI, JWT middleware, rate limiting |
| Worker | Celery + Redis, Beat scheduler |
| Database | PostgreSQL (Supabase-compatible), Alembic migrations |
| AI visibility | Perplexity API (7-day Redis cache, mock without key) |
| AI action plan | Ollama Cloud (`gpt-oss:20b-cloud`, template fallback) |
| Email | Resend (Pro/Team weekly digest) |
| Billing | Stripe Checkout + webhooks (code only, not live) |
| CI | GitHub Actions |

## Documentation

| Document | Purpose |
|----------|---------|
| [STRUCTURE.md](STRUCTURE.md) | Architecture map — what connects to what |
| [PRD](projects/pitchmind/PRD.md) | Product requirements |
| [System Design](projects/pitchmind/system-design.md) | Original design spec |
| [Plan](projects/pitchmind/Plan.md) | Implementation roadmap |
| [Progress](projects/pitchmind/progress.md) | Live progress tracker |
| [Handoff](projects/pitchmind/handoff.md) | Run/deploy checklist |

## Author

[DeryFerd](https://github.com/DeryFerd)
