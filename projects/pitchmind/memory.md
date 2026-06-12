# PitchMind — Project Memory

> Last updated: 2026-06-12 (Phase 6 code committed)

---

## Project Identity

- **Name:** PitchMind — GEO audit SaaS
- **Repo:** https://github.com/DeryFerd/pitchmind
- **Local path:** `projects/pitchmind`
- **Latest commit:** Phase 6 — Stripe billing + tier enforcement + deploy prep

---

## Stack (locked)

| Layer | Choice |
|-------|--------|
| Frontend | Next.js 15, next-intl, Tailwind, Supabase Auth |
| API | FastAPI, JWT, Stripe webhooks |
| Worker | Celery + Redis + Beat |
| Visibility | Perplexity API (mock if no key) |
| Action plan | Ollama Cloud — `https://ollama.com`, `gpt-oss:20b-cloud` |
| Email | Resend (optional) |
| Billing | Stripe Checkout + Customer Portal |
| PDF | reportlab |

---

## Completed Phases

| Phase | Scope |
|-------|-------|
| 1 | Monorepo, API, auth UI, onboarding |
| 2 | Geo engine — Perplexity, scorer, audit API |
| 3 | Site auditor — 7 checks, readiness score |
| 4 | Dashboard UI — brand/audit pages, polling, i18n |
| 5 | Action plan — Ollama Cloud, weekly email, PDF export |
| 6 (code) | Stripe billing, tier limits, settings UI, deploy configs |

---

## Key paths (Phase 6)

```
apps/api/services/billing.py
apps/api/services/stripe_service.py
apps/api/routers/billing.py
apps/api/routers/webhooks.py
apps/api/middleware/rate_limit.py
apps/web/components/BillingPanel.tsx
apps/web/app/[locale]/dashboard/settings/page.tsx
apps/worker/tasks/billing.py
packages/db/alembic/versions/002_billing_fields.py
infra/railway.worker.toml
```

---

## Tier limits (PRD)

| Tier | Brands | Queries/mo | Queries/audit | Site audits/mo |
|------|--------|------------|---------------|----------------|
| Free | 1 | 10 | 5 | 1 |
| Pro | 5 | 200 | 50 | 4 |
| Team | 20 | 1000 | 100 | 20 |

---

## Env vars (never commit)

```
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PRICE_ID_PRO=
STRIPE_PRICE_ID_TEAM=
WEB_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
OLLAMA_API_KEY=
RESEND_API_KEY=
SUPABASE_JWT_SECRET=
```

---

## Dev commands

```bash
make api && make worker && make beat && make web
make migrate
pytest tests/unit/          # 25 tests
cd apps/web && npm run build
```

Local Stripe webhook:

```bash
stripe listen --forward-to localhost:8000/api/v1/webhooks/stripe
```

---

## Next session

1. Create Stripe products (Pro $19, Team $49) → price IDs in `.env`
2. Deploy Railway (API + worker) + Vercel (web)
3. Smoke test upgrade flow end-to-end
4. Phase 7 — beta users + Product Hunt launch
