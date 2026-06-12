# PitchMind — Handoff

> **Stop point:** Phase 5 complete — Action Plan + Email + PDF  
> **Date:** 2026-06-12  
> **Next:** Phase 6 — Billing + Production Deploy

---

## Phase 5 Delivered

| Feature | Location |
|---------|----------|
| Ollama Cloud client | `packages/geo-engine/pitchmind_geo/clients/ollama_cloud.py` |
| Action plan generator | `packages/geo-engine/pitchmind_geo/action_plan.py` |
| Worker integration | `apps/worker/tasks/audit.py` |
| Action plan UI | `apps/web/components/ActionPlanList.tsx` |
| PDF export | `GET /api/v1/audits/{id}/export/pdf` |
| Weekly email | `apps/worker/tasks/email.py` + `make beat` |

---

## Audit pipeline (full)

```
Run Audit
  → Perplexity visibility batch
  → Site auditor (7 checks)
  → Ollama Cloud action plan (or template fallback)
  → Scorecard + ActionPlan in DB
  → UI: audit detail with actions + PDF download
```

---

## Required setup

1. **Ollama Cloud** — add `OLLAMA_API_KEY` to `.env` (get from https://ollama.com/settings/keys)
2. **Resend** (optional) — `RESEND_API_KEY` for live weekly emails
3. **Docker + Supabase** — when ready for E2E

```bash
# .env (never commit)
OLLAMA_API_KEY=your-key
RESEND_API_KEY=re_xxx   # optional
```

---

## Next: Phase 6

- Stripe Checkout + webhooks
- Tier limit enforcement
- Railway (API + worker) + Vercel (web)
- Production secrets

See [Plan.md](./Plan.md) Phase 6.

---

## Tests

```bash
pytest tests/unit/        # 19 passed
cd apps/web && npm run build
```

---

## Security note

If an API key was shared in chat, rotate it at ollama.com/settings/keys and store only in local `.env`.
