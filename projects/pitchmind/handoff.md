# PitchMind — Handoff

> **Stop point:** MVP complete + repo architecture docs (`STRUCTURE.md`)  
> **Date:** 2026-06-12  
> **Next:** Production deploy + beta program (Phase 7)

---

## What's ready

| Area | Status |
|------|--------|
| Full audit pipeline | visibility → site → action plan → PDF |
| Bilingual UI (EN/ID) | landing, auth, onboarding, dashboard, audit |
| Brand facts + hallucination diff | onboarding + brand settings |
| Golden queries | 25/template, picker saas/local/ecom |
| Brand settings | facts, competitors, custom queries |
| Tier limits | brands, competitors, queries, site audits |
| Billing code | Stripe checkout/portal/webhook (not live) |
| Weekly email | Pro/Team, EN+ID, delta + actions, unsubscribe |
| SSE progress | `GET /api/v1/audits/{id}/stream` |
| Cache + cost | Perplexity 7-day cache, `estimated_cost_usd` in scorecard |
| Architecture docs | [STRUCTURE.md](../../STRUCTURE.md), [README.md](../../README.md) |

---

## Documentation (repo root)

| File | Purpose |
|------|---------|
| [STRUCTURE.md](../../STRUCTURE.md) | Final layer map — frontend, API, worker, packages, connections |
| [README.md](../../README.md) | Portfolio entry, quick start, stack summary |

PitchMind-specific docs stay in `projects/pitchmind/` (PRD, Plan, progress, this file).

---

## Key API & UI routes (MVP)

| Route | Purpose |
|-------|---------|
| `GET /api/v1/brands/{id}` | Brand detail + facts + competitors |
| `DELETE .../competitors/{id}` | Remove competitor |
| `DELETE .../queries/{id}` | Remove custom query |
| `GET/PATCH /api/v1/account/email-preferences` | Weekly digest opt-in/out |
| `GET /api/v1/audits/{id}/stream` | SSE audit progress |
| `/dashboard/brands/[id]/settings` | Brand management UI |

---

## Migrations

```bash
make migrate   # 001 → 002 → 003 (email_digest_enabled)
```

---

## Run locally

```bash
# .env: DATABASE_URL, REDIS_URL, SUPABASE_JWT_SECRET, optional PERPLEXITY + OLLAMA
make dev-up && make migrate
make api && make worker && make web
pytest tests/        # 26 passed
cd apps/web && npm run build
```

Perplexity mock mode works without API key. Ollama action plan falls back to template without key.

---

## Deploy (no Stripe needed)

| Service | Notes |
|---------|-------|
| Vercel | `apps/web`, set `NEXT_PUBLIC_*` |
| Railway API | `apps/api/Dockerfile` |
| Railway Worker + Beat | `apps/worker/Dockerfile` |
| Supabase | Postgres + Auth JWT secret |
| Upstash | Redis for Celery |

Skip `STRIPE_*` env vars until ready to accept payments.

---

## Intentionally deferred

- Stripe live checkout (user choice)
- ChatGPT / Gemini engines
- Langfuse, Sentry, Supabase RLS
- Historical trend charts (P2)
- Eval pipeline + labeled dataset (ROAST_REVIEW P5)

---

## ROAST_REVIEW upgrades (2026-06-13) — DONE

| Item | Status |
|------|--------|
| Semantic ML (`all-MiniLM-L6-v2`) | sentiment + hallucination |
| CI pytest + ruff | 35 tests, no `\|\| true` |
| AgentHarness | budget + circuit breaker + retry |
| Realistic Perplexity mocks | 4 variants |
| `get_owned_brand()` in deps.py | deduplicated |

See [ROAST_REVIEW.md](./ROAST_REVIEW.md) for full review context.

---

## Phase 7 checklist

- [ ] Public URL live
- [ ] 10 beta users (5 EN + 5 ID)
- [ ] Case study with before/after SoM
- [ ] Product Hunt draft

See [Plan.md](./Plan.md) Phase 7.
