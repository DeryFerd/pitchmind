# PitchMind — Progress Tracker

> Last updated: 2026-06-12  
> Current phase: **Phase 6 — Billing + Deploy (code DONE, deploy pending)**  
> Overall progress: **~92%**

---

## Quick Status

| Item | Status |
|------|--------|
| Phase 1 — Foundation | DONE |
| Phase 2 — Geo engine | DONE |
| Phase 3 — Site auditor | DONE |
| Phase 4 — Dashboard UI | DONE |
| Phase 5 — Action Plan + Email | DONE |
| Phase 6 — Billing (code) | **DONE** |
| Phase 6 — Production deploy | not_started |
| Phase 7 — Beta + Launch | not_started |

---

## Phase Status

| Phase | Name | Status | Completed |
|-------|------|--------|-----------|
| 0–5 | Docs → Action Plan + Email | **DONE** | 2026-06-12 |
| 6 | Billing + Deploy | **code DONE / deploy pending** | 2026-06-12 |
| 7 | Beta + Launch | not_started | — |

---

## Phase 6 Checklist

### 6.1 Stripe — DONE

- [x] Tier limits module (`apps/api/services/billing.py`)
- [x] Checkout session (`POST /api/v1/billing/checkout`)
- [x] Customer portal (`POST /api/v1/billing/portal`)
- [x] Webhook handler (`POST /api/v1/webhooks/stripe`) with signature verify
- [x] Enforce brand / query / site-audit limits per tier
- [x] Usage counter + monthly reset Celery beat task
- [x] Migration 002: `stripe_subscription_id`, `site_audits_used_this_period`
- [x] Billing settings UI (`/dashboard/settings`)
- [x] 6 billing unit tests (25 total passing)
- [ ] Live Stripe products + price IDs in production
- [ ] End-to-end upgrade smoke test on staging

### 6.2 Production Deploy — pending

- [x] CORS from `CORS_ORIGINS` env
- [x] Rate limiting middleware (100 req/min)
- [x] API Dockerfile updated (stripe, reportlab)
- [x] Worker Dockerfile + `infra/railway.worker.toml`
- [ ] Railway API + worker live
- [ ] Vercel production domain
- [ ] Supabase production + Upstash Redis

### 6.3 Observability — pending

- [ ] Sentry DSN both apps
- [ ] Langfuse for Ollama Cloud traces

### 6.4 Security — partial

- [x] Stripe webhook signature verify
- [x] Rate limiting middleware
- [x] CORS configurable for production domain
- [ ] RLS policies tested on Supabase

---

## Phase 6 Exit Criteria

- [ ] Production URL live
- [x] Free tier limits enforced in API
- [ ] Upgrade to Pro works end-to-end (needs Stripe keys + deploy)
- [ ] No critical errors in 48h smoke test

---

## Changelog

### 2026-06-12 — Phase 6 billing + deploy prep (committed)

- Stripe Checkout + Customer Portal + webhook handler
- Tier enforcement: brands, queries/month, queries/audit, site audits/month
- Billing settings page (`/dashboard/settings`) with usage meters + upgrade buttons
- Migration 002, worker monthly reset task, rate limit + CORS config
- Worker Dockerfile, `railway.worker.toml`, CI stripe dep
- 25 unit tests passing; web build OK

### 2026-06-12 — Phase 5 action plan + email + PDF

- Ollama Cloud client + action plan generator with template fallback
- ActionPlanList UI, ExportPdfButton, weekly digest, PDF export

---

## Links

- [PRD](./PRD.md) | [Plan](./Plan.md) | [handoff.md](./handoff.md) | [memory.md](./memory.md)
