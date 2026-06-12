# PitchMind — Handoff

> **Stop point:** Phase 1 Foundation ~90% complete (API-web integration done, live services pending)  
> **Date:** 2026-06-12  
> **Repo:** https://github.com/DeryFerd/pitchmind

---

## Where We Stopped

Phase 1 code integration is complete. Onboarding persists to PostgreSQL via API, dashboard loads brands, and protected routes redirect unauthenticated users. **Blocked on user actions:** Docker Desktop (for local DB) and Supabase keys (for live auth).

---

## Immediate Next Steps (in order)

### Step 1: Start Docker + run migrations (15 min)

```bash
# Start Docker Desktop first, then:
cd projects/pitchmind
cp .env.example .env          # if not done
make dev-up
make migrate
```

Verify: tables exist in postgres on port 5433.

### Step 2: Supabase setup (30 min)

1. Create project at https://supabase.com
2. Enable Email + Google auth providers
3. Copy to `.env` (pitchmind root):
   - `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_JWT_SECRET`
4. Copy to `apps/web/.env.local` (see `.env.local.example`):
   - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_API_URL=http://localhost:8000`
5. JWT secret: Project Settings → API → JWT Secret

### Step 3: End-to-end local test (30 min)

```bash
make api    # :8000
make web    # :3000
```

Flow to verify:
1. Sign up at `/en/signup`
2. Complete onboarding at `/en/onboarding`
3. Dashboard at `/en/dashboard` shows brand name + website
4. Data in PostgreSQL (not localStorage)

```bash
curl http://localhost:8000/health
# With valid JWT:
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/workspaces
```

### Step 4: Complete Phase 1 exit criteria

- [ ] User can sign up → onboard → see dashboard with brand name
- [ ] Data persisted in PostgreSQL (not localStorage) — **code ready, needs Docker + Supabase**
- [ ] Push to GitHub
- [ ] Deploy API to Railway, web to Vercel (optional but Phase 1 exit criteria)

---

## What Was Done (2026-06-12)

| Task | File(s) |
|------|---------|
| API helper (client) | `apps/web/lib/api.ts` |
| API helper (server) | `apps/web/lib/api-server.ts` |
| Onboarding → API | `apps/web/app/[locale]/onboarding/page.tsx` |
| Dashboard brand list | `apps/web/app/[locale]/dashboard/page.tsx` |
| Auth middleware | `apps/web/middleware.ts` |
| List brands endpoint | `apps/api/routers/workspaces.py` → `GET /workspaces/{id}/brands` |
| Locale redirects | login, signup, onboarding pages |
| i18n strings | `messages/en.json`, `messages/id.json` |

---

## Phase 2 Preview (after Phase 1 done)

Start in `packages/geo-engine/`:

1. `clients/perplexity.py` — API client
2. `clients/ollama_cloud.py` — use pattern from system-design.md:
   ```python
   Client(host="https://ollama.com", headers={"Authorization": f"Bearer {key}"})
   model="gpt-oss:20b-cloud"
   ```
3. Citation parser + scorer
4. Implement `apps/worker/tasks/audit.py` fully
5. Add `POST /api/v1/brands/{id}/audits` endpoint

---

## Key Files to Read First

| File | Why |
|------|-----|
| [Plan.md](./Plan.md) | Full phased roadmap |
| [system-design.md](./system-design.md) | Architecture, API spec, data model |
| [memory.md](./memory.md) | Stack decisions, conventions |
| [progress.md](./progress.md) | What's DONE vs not |
| `apps/web/lib/api.ts` | Client API helper |
| `apps/api/routers/workspaces.py` | Workspace + brand list |
| `apps/web/middleware.ts` | Auth protection |

---

## Environment Checklist

```bash
# Required for Phase 1 completion
DATABASE_URL=postgresql://pitchmind:pitchmind_dev@localhost:5433/pitchmind
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
SUPABASE_JWT_SECRET=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_API_URL=http://localhost:8000

# Required for Phase 2
PERPLEXITY_API_KEY=
OLLAMA_API_KEY=
OLLAMA_CLOUD_HOST=https://ollama.com
OLLAMA_ACTION_PLAN_MODEL=gpt-oss:20b-cloud
```

---

## Do NOT

- Add local Ollama daemon / GPU sidecar on Railway
- Skip bilingual support — all user-facing strings via `messages/en.json` + `id.json`
- Build audit UI before Phase 2 geo-engine works

---

## Questions for User (if blocked)

1. Supabase project URL + keys?
2. Use Supabase hosted Postgres or local docker for dev?
3. Railway vs Fly.io for API deploy preference?
4. Start Docker Desktop so migrations can run?
