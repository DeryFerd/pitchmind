# PitchMind — Project Memory

> Session memory for agents/devs continuing this project.  
> Last updated: 2026-06-12

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
| Visibility AI | Perplexity API (Phase 2) |
| Action plan LLM | **Ollama Cloud** — `https://ollama.com`, NOT local Ollama |
| Action plan model | `gpt-oss:20b-cloud` (default), `qwen3.5:cloud` (deep) |
| Billing | Stripe (Phase 6) |

---

## Monorepo Layout

```
projects/pitchmind/
├── apps/web/          → Next.js, run: cd apps/web && npm run dev
├── apps/api/          → FastAPI, PYTHONPATH=packages/db;apps
├── apps/worker/       → Celery
├── packages/db/       → pitchmind_db models + alembic/
├── packages/geo-engine/   → stub (Phase 2)
├── packages/site-auditor/ → stub (Phase 3)
├── packages/harness/      → stub
├── infra/docker-compose.yml
└── Makefile
```

**PYTHONPATH for Python apps:** `packages/db` and `apps` (see Makefile).

**Alembic:** run from `packages/db` with `DATABASE_URL` set.

---

## What Was Built (2026-06-11)

1. Full SQLAlchemy schema: users, workspaces, brands, competitors, golden_queries, audit_runs, query_results, site_audits, action_plans, subscriptions
2. Alembic migration `001_initial_schema.py`
3. Query seed templates: saas/local/ecom × EN/ID (20 queries each)
4. FastAPI routers with ownership checks
5. Next.js bilingual landing + auth UI + onboarding (localStorage) + dashboard shell
6. Celery `run_visibility_audit` placeholder
7. CI workflow, API Dockerfile, railway.toml

---

## Known Gaps / Stubs

- Auth pages need real Supabase env vars to work (middleware + API JWT)
- DB migration requires Docker Desktop running (`make dev-up` then `make migrate`)
- `POST /audits` not implemented (Phase 2)
- Worker task returns placeholder JSON
- No Stripe, Resend, Perplexity, Ollama Cloud clients yet

## What Was Built (2026-06-12)

1. `apps/web/lib/api.ts` — client-side API helper with Supabase Bearer token
2. `apps/web/lib/api-server.ts` — server-side fetch for dashboard
3. Onboarding wired: workspace → brand → competitors → query seed (`saas`)
4. `GET /api/v1/workspaces/{id}/brands` endpoint
5. Dashboard loads brands from API (PostgreSQL-backed)
6. Next.js middleware protects `/dashboard` and `/onboarding` routes
7. Locale-aware redirects on login/signup/onboarding

---

## Dev Commands

```bash
# From projects/pitchmind/
make dev-up          # postgres:5433, redis:6380
make migrate         # alembic upgrade head
make api             # :8000
make web             # :3000
make worker          # celery
```

Copy `.env.example` → `.env` at pitchmind root and `apps/web/.env.local`.

---

## Conventions

- API prefix: `/api/v1`
- Locales: `en`, `id` via next-intl `[locale]` routes
- Brand ownership: workspace.owner_id must match JWT sub
- Do NOT add local Ollama daemon — use Ollama Cloud API only
