# PitchMind

**GEO (Generative Engine Optimization) SaaS** — measure and improve how AI search engines (ChatGPT, Perplexity, Gemini) cite and recommend your brand.

Bilingual EN + ID | Ollama Cloud + Perplexity API | Full-stack production portfolio project.

## Status

**Phase 1 in progress** — monorepo scaffolded, API + web foundation, DB migrations ready.

## Repository structure

```
├── docs/                         # Portfolio research (AI/ML trends 2026)
├── projects/pitchmind/
│   ├── PRD.md, system-design.md, Plan.md, progress.md, memory.md, handoff.md
│   ├── apps/web/                 # Next.js 15 + next-intl (EN/ID)
│   ├── apps/api/                 # FastAPI
│   ├── apps/worker/              # Celery skeleton
│   ├── packages/db/              # SQLAlchemy + Alembic
│   ├── packages/geo-engine/      # Phase 2
│   ├── infra/docker-compose.yml
│   └── Makefile
└── .github/workflows/ci.yml
```

## PitchMind docs

| Document | Purpose |
|----------|---------|
| [PRD](projects/pitchmind/PRD.md) | Product requirements |
| [System Design](projects/pitchmind/system-design.md) | Architecture & API |
| [Plan](projects/pitchmind/Plan.md) | End-to-end implementation roadmap |
| [Progress](projects/pitchmind/progress.md) | Live progress tracker |

## Stack (planned)

- **Frontend:** Next.js 15, next-intl (EN/ID)
- **Backend:** FastAPI, Celery, PostgreSQL (Supabase)
- **AI:** Perplexity API (visibility scan), Ollama Cloud (`gpt-oss:20b-cloud` action plans)
- **Billing:** Stripe | **Auth:** Supabase

## Author

[DeryFerd](https://github.com/DeryFerd)
