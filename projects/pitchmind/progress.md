# PitchMind — Progress Tracker

> Last updated: 2026-06-12  
> Current phase: **MVP product complete — deploy + beta pending**  
> Overall progress: **~95%**

---

## Quick Status

| Item | Status |
|------|--------|
| Phases 1–5 (core product) | DONE |
| Phase 6 billing (code) | DONE (Stripe live skipped) |
| MVP gap fill (settings, facts, email, SSE) | **DONE** |
| Production deploy | not_started |
| Phase 7 beta + launch | not_started |

---

## Latest: MVP gap fill (2026-06-12)

### Product polish — DONE

- [x] Brand facts in onboarding (pricing, features, location)
- [x] Query template picker (saas / local / ecom)
- [x] 25 golden queries per template (13 EN + 12 ID)
- [x] Brand settings page (`/dashboard/brands/[id]/settings`)
- [x] Competitor + custom query management
- [x] Competitor limit per tier (2 free / 5 pro+)
- [x] Hallucination diff UI (expandable stated vs expected)
- [x] Google signup
- [x] Weekly email: Pro/Team only, EN+ID, SoM delta, top actions, unsubscribe
- [x] Email preferences in account settings
- [x] SSE audit progress (`GET /audits/{id}/stream`)
- [x] Perplexity 7-day Redis cache
- [x] API cost estimate in scorecard
- [x] Harness retry helper
- [x] Integration test (mock audit pipeline)
- [x] Migration 003 (`email_digest_enabled`)
- [x] PRD / Plan / system-design status synced

### Still pending

- [ ] Production deploy (Vercel + Railway + Supabase)
- [ ] Stripe live (skipped by choice)
- [ ] Sentry + Langfuse
- [ ] Supabase RLS policies
- [ ] ChatGPT/Gemini multi-engine (PRD stretch)
- [ ] Phase 7 beta users + case study

---

## Tests

```bash
pytest tests/           # 26 passed (25 unit + 1 integration)
cd apps/web && npm run build
```

---

## Links

- [PRD](./PRD.md) | [Plan](./Plan.md) | [handoff.md](./handoff.md) | [memory.md](./memory.md)
