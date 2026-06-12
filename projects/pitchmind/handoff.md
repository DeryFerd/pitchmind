# PitchMind — Handoff

> **Stop point:** Phase 2 Geo Engine ~70% complete (visibility audit works; site auditor + action plan pending)  
> **Date:** 2026-06-12  
> **Repo:** https://github.com/DeryFerd/pitchmind

---

## Where We Stopped

Phase 2 visibility engine is implemented. Perplexity client runs in **mock mode** without API key (good for dev without Docker/Supabase). Full E2E audit flow needs Docker (Postgres + Redis) + Supabase — can be wired later.

---

## Deferred (OK to do later)

| Item | Why deferred |
|------|--------------|
| Docker Desktop | Local Postgres + Redis for migrations and Celery |
| Supabase keys | Live auth + JWT for API calls |
| `PERPLEXITY_API_KEY` | Real AI responses (mock works for dev) |
| Railway / Vercel deploy | After local E2E verified |

---

## Immediate Next Steps (when ready)

### Step 1: Local infra (15 min)

```bash
# Start Docker Desktop, then:
cd projects/pitchmind
make dev-up
make migrate
make api
make worker   # separate terminal
make web
```

### Step 2: Supabase (30 min)

Copy keys to `.env` and `apps/web/.env.local` — see `.env.example`.

### Step 3: Test audit E2E

1. Sign up → onboard → dashboard
2. Click "Run audit"
3. Worker processes queries (mock Perplexity if no API key)
4. `GET /api/v1/audits/{id}` returns scorecard

### Step 4: Phase 3 — Site Auditor

Start in `packages/site-auditor/`:
- `llms_txt.py`, `robots.py`, `schema.py`
- Wire into audit worker after visibility batch

---

## Phase 2 Delivered

| Component | Path |
|-----------|------|
| Perplexity client (mock + real) | `packages/geo-engine/pitchmind_geo/clients/perplexity.py` |
| Mention/citation parser | `packages/geo-engine/pitchmind_geo/parser.py` |
| Hallucination checker | `packages/geo-engine/pitchmind_geo/hallucination.py` |
| Scorecard scorer | `packages/geo-engine/pitchmind_geo/scorer.py` |
| Batch runner | `packages/geo-engine/pitchmind_geo/runner.py` |
| Celery audit task | `apps/worker/tasks/audit.py` |
| Audit API | `apps/api/routers/audits.py` |
| Run audit UI | `apps/web/components/RunAuditButton.tsx` |
| Unit tests | `tests/unit/test_geo_*.py` |

### API Endpoints (new)

- `POST /api/v1/brands/{id}/audits` — enqueue visibility audit
- `GET /api/v1/audits/{id}` — status + scorecard
- `GET /api/v1/brands/{id}/audits` — audit history
- `GET /api/v1/brands/{id}/scorecard` — latest scorecard

---

## Mock Mode

When `PERPLEXITY_API_KEY` is empty, geo-engine returns synthetic responses mentioning PitchMind + competitors. Lets you develop and test worker/scoring without paid API.

---

## Key Files

| File | Why |
|------|-----|
| [Plan.md](./Plan.md) | Full phased roadmap |
| [memory.md](./memory.md) | Stack decisions |
| [progress.md](./progress.md) | Live status |
| `packages/geo-engine/pitchmind_geo/runner.py` | Audit batch logic |
| `apps/worker/tasks/audit.py` | Celery task |
| `apps/api/routers/audits.py` | Audit endpoints |

---

## Do NOT

- Add local Ollama daemon — use Ollama Cloud only
- Skip bilingual support
- Require Docker/Supabase to run unit tests (`pytest tests/unit/` works standalone)
