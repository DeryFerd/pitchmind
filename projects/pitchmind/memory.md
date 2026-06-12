# PitchMind — Project Memory

> Last updated: 2026-06-12 (README + STRUCTURE.md at repo root)

---

## Project Identity

- **Name:** PitchMind — GEO audit SaaS
- **Repo:** https://github.com/DeryFerd/pitchmind
- **Local path:** `projects/pitchmind`
- **Status:** MVP product ~95% — deploy + beta next
- **Architecture map:** [STRUCTURE.md](../../STRUCTURE.md) (repo root)
- **Portfolio README:** [README.md](../../README.md)

---

## Stack (locked)

| Layer | Choice |
|-------|--------|
| Frontend | Next.js 15, next-intl, Tailwind, Supabase Auth |
| API | FastAPI, JWT, tier limits (Stripe code present, live skipped) |
| Worker | Celery + Redis + Beat |
| Visibility | Perplexity API (mock if no key, 7-day Redis cache) |
| Action plan | Ollama Cloud — `gpt-oss:20b-cloud` |
| Email | Resend — Pro/Team weekly digest only |
| PDF | reportlab |

---

## Key paths (latest)

```
apps/web/app/[locale]/dashboard/brands/[id]/settings/   # brand facts, competitors, queries
apps/web/components/BrandSettingsPanel.tsx
apps/web/components/QueryResultsTable.tsx               # hallucination diff expand
apps/api/routers/account.py                             # email preferences
apps/api/routers/audits.py                              # SSE stream
packages/geo-engine/pitchmind_geo/cache.py              # Perplexity cache
packages/db/alembic/versions/003_user_email_prefs.py
tests/integration/test_audit_pipeline.py
```

---

## Tier limits

| Tier | Brands | Competitors | Queries/mo | Queries/audit |
|------|--------|-------------|------------|---------------|
| Free | 1 | 2 | 10 | 5 |
| Pro | 5 | 5 | 200 | 50 |
| Team | 20 | 5 | 1000 | 100 |

Weekly email: **Pro + Team only** (`user_receives_weekly_email`).

Golden queries: **25** per template seed (13 EN + 12 ID).

---

## Decisions

- **Stripe live skipped** — billing code exists; focus product + free deploy first
- **Brand facts required for good hallucination checks** — collected in onboarding + brand settings
- **Perplexity only** for visibility MVP; ChatGPT/Gemini deferred to v1.1

---

## Dev commands

```bash
make migrate          # runs through 003
make api && make worker && make beat && make web
pytest tests/         # 26 tests
```

---

## Next session

1. Deploy Vercel (web) + Railway (API/worker) — free tiers OK
2. Supabase production + env secrets
3. Run full E2E audit with real Perplexity + Ollama keys
4. Phase 7: 10 beta users, case study, Product Hunt

New contributors: start with **STRUCTURE.md** for layer map, then `handoff.md` for run commands.
