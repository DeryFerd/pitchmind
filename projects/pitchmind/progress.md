# PitchMind — Progress Tracker

> Last updated: 2026-06-12  
> Current phase: **Phase 1 — Foundation (near complete)**  
> Overall progress: **~75%**

---

## Quick Status

| Item | Status |
|------|--------|
| PRD | DONE |
| System Design | DONE |
| Plan | DONE |
| GitHub repo | DONE — https://github.com/DeryFerd/pitchmind |
| Monorepo scaffold | DONE |
| Database models + migration | DONE |
| FastAPI (basic endpoints) | DONE |
| Celery worker skeleton | DONE |
| Next.js web (landing, auth, onboarding, dashboard) | DONE |
| docker-compose (postgres + redis) | DONE |
| CI GitHub Actions | DONE |
| Onboarding → API wired | DONE |
| Protected dashboard routes | DONE |
| Dashboard loads brands from API | DONE |
| Supabase project wired | NOT STARTED (needs user keys) |
| Migrations run on live DB | BLOCKED — Docker Desktop not running |
| API deployed staging | NOT STARTED |
| Production URL | NOT STARTED |

---

## Phase Status

| Phase | Name | Status | Started | Completed | Notes |
|-------|------|--------|---------|-----------|-------|
| 0 | Documentation | **DONE** | 2026-06-11 | 2026-06-11 | |
| 1 | Foundation | **in_progress** | 2026-06-11 | — | ~90% of Phase 1 tasks |
| 2 | Geo Engine | not_started | — | — | |
| 3 | Site Auditor | not_started | — | — | |
| 4 | Dashboard UI | not_started | — | — | shell + brand list |
| 5 | Action Plan + Email | not_started | — | — | |
| 6 | Billing + Deploy | not_started | — | — | |
| 7 | Beta + Launch | not_started | — | — | |

---

## Phase 1 Checklist

### 1.1 Monorepo Scaffold

- [x] DONE — Git repo + GitHub push
- [x] DONE — `apps/web` Next.js 15 + TypeScript + Tailwind
- [x] DONE — `apps/api` FastAPI
- [x] DONE — `apps/worker` Celery skeleton
- [x] DONE — `packages/geo-engine`, `site-auditor`, `harness`, `db`
- [x] DONE — `infra/docker-compose.yml` (postgres + redis)
- [x] DONE — `pyproject.toml` + Ruff config
- [x] DONE — `.env.example`
- [x] DONE — `Makefile` dev commands

### 1.2 Database

- [x] DONE — Alembic setup
- [x] DONE — Migration 001 (all tables)
- [x] DONE — Seed templates EN + ID (saas, local, ecom)
- [ ] BLOCKED — Run migration on live DB (start Docker Desktop first)

### 1.3 Auth

- [x] DONE — Web Supabase client + SSR helpers
- [x] DONE — API JWT middleware (Supabase)
- [x] DONE — Login / signup / OAuth callback pages
- [x] DONE — Protected route middleware (web) — `/dashboard`, `/onboarding`
- [ ] NOT STARTED — Create Supabase project + env keys
- [ ] NOT STARTED — Auto-create workspace on first API call (code ready, needs live test)

### 1.4 Basic API

- [x] DONE — `GET /health`
- [x] DONE — `POST /api/v1/workspaces`
- [x] DONE — `GET /api/v1/workspaces`
- [x] DONE — `GET /api/v1/workspaces/{id}/brands`
- [x] DONE — `POST /api/v1/brands` + `PATCH`
- [x] DONE — `POST /api/v1/brands/{id}/competitors`
- [x] DONE — `GET/POST /api/v1/brands/{id}/queries`
- [x] DONE — `POST /api/v1/brands/{id}/queries/seed`

### 1.5 Basic Web

- [x] DONE — Landing page EN + ID
- [x] DONE — Auth pages (login, signup, callback)
- [x] DONE — Onboarding wizard wired to API (workspace → brand → competitors → seed)
- [x] DONE — Dashboard with brand list from API
- [x] DONE — `lib/api.ts` + `lib/api-server.ts` helpers

### 1.6 CI/CD

- [x] DONE — GitHub Actions lint + build
- [x] DONE — API Dockerfile + railway.toml
- [ ] NOT STARTED — Railway deploy
- [ ] NOT STARTED — Vercel deploy

---

## Blockers

| Blocker | Owner | Since | Resolution |
|---------|-------|-------|------------|
| Supabase keys not configured | User | 2026-06-11 | Create project, copy to `.env` + `apps/web/.env.local` |
| Docker Desktop not running | User | 2026-06-12 | Start Docker Desktop, then `make dev-up` + `make migrate` |

---

## Changelog

### 2026-06-12 — Phase 1 API integration

- Onboarding calls API: workspace → brand → competitors → query seed
- `GET /api/v1/workspaces/{id}/brands` endpoint added
- `lib/api.ts` (client) + `lib/api-server.ts` (server) helpers
- Middleware protects `/dashboard` and `/onboarding` (redirect to login)
- Dashboard displays brands from PostgreSQL via API
- Locale-aware redirects on login/signup/onboarding
- `apps/web/.env.local.example` added
- Web build verified (`npm run build` pass)

### 2026-06-11 — Phase 1 scaffold

- Monorepo: apps/web, apps/api, apps/worker, packages/*
- SQLAlchemy models + Alembic migration 001
- FastAPI endpoints: workspaces, brands, competitors, queries, seed
- Next.js 15 + next-intl (EN/ID): landing, login, signup, onboarding, dashboard
- Celery audit task placeholder
- docker-compose, Makefile, CI workflow, API Dockerfile
- Web build verified (`npm run build` pass)

### 2026-06-11 — Docs + repo

- GitHub: https://github.com/DeryFerd/pitchmind
- Ollama Cloud stack decision documented

---

## Links

- [PRD](./PRD.md) | [System Design](./system-design.md) | [Plan](./Plan.md)
- [handoff.md](./handoff.md) | [memory.md](./memory.md)
- Repo: https://github.com/DeryFerd/pitchmind
