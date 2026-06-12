# PitchMind — Handoff

> **Stop point:** Phase 1 Foundation ~70% complete (scaffold done, deploy + live auth pending)  
> **Date:** 2026-06-11  
> **Repo:** https://github.com/DeryFerd/pitchmind

---

## Where We Stopped

Phase 1 monorepo is scaffolded and builds successfully. Documentation, database schema, API skeleton, web UI shell, and CI are in place. **Not yet wired to live services** (Supabase, deployed DB, API-to-web integration).

---

## Immediate Next Steps (in order)

### Step 1: Local infra + DB (15 min)

```bash
cd projects/pitchmind
cp .env.example .env
make dev-up
# Set DATABASE_URL=postgresql://pitchmind:pitchmind_dev@localhost:5433/pitchmind
make migrate
```

Verify: `psql` or check tables exist in postgres.

### Step 2: Supabase setup (30 min)

1. Create project at https://supabase.com
2. Enable Email + Google auth providers
3. Copy to `.env` and `apps/web/.env.local`:
   - `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_JWT_SECRET`
   - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Get JWT secret: Project Settings → API → JWT Secret

### Step 3: Wire onboarding → API (1-2 hrs)

File: `apps/web/app/[locale]/onboarding/page.tsx`

Replace `localStorage` stub with:
1. Get Supabase session token
2. `POST /api/v1/workspaces` (auto-created if first login)
3. `POST /api/v1/brands` with competitors
4. `POST /api/v1/brands/{id}/queries/seed` template `saas`

Create `apps/web/lib/api.ts` helper with `Authorization: Bearer <token>`.

### Step 4: Test API locally (30 min)

```bash
make api
curl http://localhost:8000/health
# With valid JWT:
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/workspaces
```

### Step 5: Protected dashboard (1 hr)

- Add Next.js middleware to redirect unauthenticated users from `/dashboard`
- Load user's brands from API on dashboard page

### Step 6: Complete Phase 1 exit criteria

- [ ] User can sign up → onboard → see dashboard with brand name
- [ ] Data persisted in PostgreSQL (not localStorage)
- [ ] Push to GitHub
- [ ] Deploy API to Railway, web to Vercel (optional but Phase 1 exit criteria)

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
| `packages/db/pitchmind_db/models.py` | DB schema |
| `apps/api/routers/brands.py` | Main API logic |
| `apps/web/app/[locale]/onboarding/page.tsx` | Needs API wire |

---

## Environment Checklist

```bash
# Required for Phase 1 completion
DATABASE_URL=
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
