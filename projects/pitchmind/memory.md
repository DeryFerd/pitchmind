# PitchMind — Project Memory

> Session memory for agents/devs continuing this project.  
> Last updated: 2026-06-12 (Phase 4)

---

## Project Identity

- **Name:** PitchMind
- **Type:** GEO (Generative Engine Optimization) audit SaaS
- **Repo:** https://github.com/DeryFerd/pitchmind
- **Local path:** `D:\Portfolio Data\Production-Level AI Projects\SaaS ML-AI-DL\projects\pitchmind`
- **Target:** Hybrid EN + ID market, portfolio-grade end-to-end product

---

## Stack Decisions (locked)

| Layer | Choice |
|-------|--------|
| Frontend | Next.js 15, next-intl (`en`, `id`), Tailwind, Supabase Auth |
| API | FastAPI, JWT via Supabase secret |
| Worker | Celery + Redis |
| DB | PostgreSQL (Supabase prod / docker local port 5433) |
| Redis | Upstash prod / docker local port 6380 |
| Visibility AI | Perplexity API (mock mode if no key) |
| Action plan LLM | **Ollama Cloud** — `https://ollama.com`, NOT local Ollama |
| Billing | Stripe (Phase 6) |

---

## Monorepo Layout

```
projects/pitchmind/
├── apps/web/              → Next.js 15 + next-intl
├── apps/api/              → FastAPI routers: workspaces, brands, audits
├── apps/worker/           → Celery audit task (visibility + site)
├── packages/db/           → SQLAlchemy + Alembic
├── packages/geo-engine/   → Perplexity, parser, scorer, runner
├── packages/site-auditor/ → llms.txt, robots, schema, readiness
├── infra/docker-compose.yml
└── Makefile
```

**PYTHONPATH:** `packages/db` and `apps` (+ geo-engine, site-auditor in worker).

---

## Completed Phases

| Phase | Summary |
|-------|---------|
| 1 | Monorepo, API, web auth/onboarding, CI |
| 2 | Geo-engine, audit API, Celery visibility task, mock Perplexity |
| 3 | Site auditor (7 checks), readiness score, worker chain |
| 4 | **in progress** — dashboard UI, audit detail pages |

---

## Known Gaps

- Supabase + Docker deferred (auth/migrations need user setup)
- Action plan (Ollama Cloud) — Phase 5
- Stripe, Resend — Phase 5/6
- Rate limiter, SSE progress — optional MVP

---

## Dev Commands

```bash
make dev-up && make migrate
make api    # :8000
make worker # celery
make web    # :3000
pytest tests/unit/   # 17 tests, no Docker needed
```

---

## Conventions

- API prefix: `/api/v1`
- Locales: `en`, `id` via `[locale]` routes
- User-facing strings: `messages/en.json` + `id.json` only
- Do NOT add local Ollama daemon — Ollama Cloud only
