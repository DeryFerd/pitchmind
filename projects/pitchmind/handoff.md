# PitchMind — Handoff

> **Stop point:** Phase 6 code complete — Stripe billing + tier enforcement committed  
> **Date:** 2026-06-12  
> **Next:** Production deploy + Stripe live keys + Phase 7 beta

---

## What's in the repo (Phase 6)

| Feature | Location |
|---------|----------|
| Tier limits + usage | `apps/api/services/billing.py` |
| Stripe Checkout / Portal | `apps/api/services/stripe_service.py` |
| Billing API | `GET/POST /api/v1/billing/*` |
| Stripe webhook | `POST /api/v1/webhooks/stripe` |
| Brand + audit enforcement | `routers/brands.py`, `routers/audits.py` |
| Monthly reset task | `apps/worker/tasks/billing.py` + beat (1st of month) |
| Billing UI | `/dashboard/settings` + `BillingPanel.tsx` |
| Migration 002 | `002_billing_fields.py` |
| Deploy prep | CORS env, rate limit, API + worker Dockerfiles |

---

## Full audit pipeline (unchanged)

```
Run Audit
  → Tier limit check (brands, queries/mo, site audits/mo)
  → Perplexity visibility batch
  → Site auditor (7 checks)
  → Ollama Cloud action plan (or template fallback)
  → Scorecard + ActionPlan in DB
  → UI: audit detail + PDF + billing settings
```

---

## Before first deploy

1. **Migration:** `make migrate` (runs 002)
2. **Stripe Dashboard:** create Pro ($19) + Team ($49) products → copy price IDs
3. **`.env`** (never commit):

```bash
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_ID_PRO=price_xxx
STRIPE_PRICE_ID_TEAM=price_xxx
WEB_URL=https://your-vercel-domain.vercel.app
CORS_ORIGINS=https://your-vercel-domain.vercel.app
OLLAMA_API_KEY=your-key
```

4. **Local webhook test:**

```bash
stripe listen --forward-to localhost:8000/api/v1/webhooks/stripe
```

---

## Deploy checklist

| Service | Config | Start command |
|---------|--------|---------------|
| Railway API | `apps/api/Dockerfile`, `infra/railway.toml` | uvicorn |
| Railway Worker | `apps/worker/Dockerfile`, `infra/railway.worker.toml` | celery worker |
| Railway Beat | same worker image | `celery beat` (separate service) |
| Vercel Web | `apps/web/` | auto |
| Stripe webhook | production API URL | `/api/v1/webhooks/stripe` |
| Supabase | production JWT secret | — |
| Upstash | Redis URL for Celery | — |

---

## Tests (verified before commit)

```bash
pytest tests/unit/        # 25 passed
cd apps/web && npm run build
```

---

## Next: finish Phase 6 deploy, then Phase 7

- [ ] Railway API + worker + beat live
- [ ] Vercel production domain
- [ ] Stripe webhook registered on production URL
- [ ] One successful Pro upgrade smoke test
- [ ] Recruit 10 beta users (5 EN + 5 ID)
- [ ] Product Hunt launch + case study

See [Plan.md](./Plan.md) Phase 6–7.
