# PitchMind — Handoff

> **Stop point:** ROAST_REVIEW code fixes complete (credential items deferred)  
> **Date:** 2026-06-13  
> **Next:** Production deploy when cloud credentials are ready

---

## What's ready

| Area | Status |
|------|--------|
| Full audit pipeline | visibility → site → action plan → PDF |
| Bilingual UI (EN/ID) | landing, auth, onboarding, dashboard, audit |
| Semantic ML | sentiment + hallucination (`all-MiniLM-L6-v2`) |
| AgentHarness | budget + circuit breaker + retry |
| SSE progress | Redis pub/sub + 5s DB fallback |
| CI | pytest (41) + ruff + `.env` guard + ML eval gate |
| API route tests | health, workspaces, brand 403 |
| Realistic Perplexity mocks | 4 variants |
| Architecture docs | [STRUCTURE.md](../../STRUCTURE.md), [system-design.md](./system-design.md) |

---

## Run locally

```bash
# .env: DATABASE_URL, REDIS_URL, SUPABASE_JWT_SECRET, optional PERPLEXITY + OLLAMA
make dev-up && make migrate
make api && make worker && make web
make test        # 41 passed
make lint
```

Perplexity mock mode works without API key. Ollama action plan falls back to template without key.

---

## Key API routes

| Route | Purpose |
|-------|---------|
| `GET /health` | Liveness |
| `GET /api/v1/workspaces` | List workspaces |
| `GET /api/v1/brands/{id}` | Brand detail + facts + competitors |
| `GET /api/v1/audits/{id}/stream` | SSE via Redis `audit:progress:{id}` |
| `/dashboard/brands/[id]/settings` | Brand management UI |

---

## ROAST_REVIEW status

| Item | Status |
|------|--------|
| P1 ML component | DONE |
| P2 CI pytest + ruff | DONE |
| P3 AgentHarness | DONE |
| P4 Realistic mocks | DONE |
| #5 sys.path.insert | DONE → PYTHONPATH |
| #7 get_owned_brand dedup | DONE |
| #8 SSE SQL polling | DONE → Redis pub/sub |
| #9 .env git safety | DONE → CI guard |
| API route tests | DONE |
| P5 Eval pipeline | DONE (dataset + CI gate) |
| P0 Deploy | **skipped** — credentials |
| Langfuse + Sentry | **skipped** — credentials |
| Supabase RLS | **skipped** — credentials |
| Stripe live | **skipped** — by choice |

---

## Deploy (when credentials ready)

| Service | Notes |
|---------|-------|
| Vercel | `apps/web`, set `NEXT_PUBLIC_*` |
| Railway API | `apps/api/Dockerfile` |
| Railway Worker + Beat | `apps/worker/Dockerfile` |
| Supabase | Postgres + Auth JWT secret |
| Upstash | Redis for Celery + SSE pub/sub |

---

## Phase 7 checklist

- [ ] Public URL live
- [ ] 10 beta users (5 EN + 5 ID)
- [ ] Case study with before/after SoM
- [ ] Product Hunt draft

See [Plan.md](./Plan.md) Phase 7.
