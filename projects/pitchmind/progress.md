# PitchMind — Progress Tracker

> Last updated: 2026-06-13  
> Current phase: **MVP + ROAST_REVIEW upgrades — deploy + beta pending**  
> Overall progress: **~96%**

---

## Quick Status

| Item | Status |
|------|--------|
| Phases 1–5 (core product) | DONE |
| Phase 6 billing (code) | DONE (Stripe live skipped) |
| MVP gap fill (settings, facts, email, SSE) | **DONE** |
| ROAST_REVIEW P1–P4 (ML, CI, harness, mocks) | **DONE** |
| Repo docs (README + STRUCTURE.md) | **DONE** |
| Production deploy | not_started |
| Phase 7 beta + launch | not_started |

---

## Latest: ROAST_REVIEW implementation (2026-06-13)

### P1 — Semantic ML component — DONE

- [x] `packages/geo-engine/pitchmind_geo/semantic.py` — `all-MiniLM-L6-v2` CPU inference
- [x] Embedding-based sentiment (regex fallback)
- [x] Semantic hallucination detection vs brand facts
- [x] `sentence-transformers` + `numpy` in dependencies + Dockerfiles

### P2 — CI fix — DONE

- [x] `pytest tests/` in GitHub Actions (was skipped)
- [x] `ruff check` without `|| true`
- [x] HuggingFace model cache in CI
- [x] **35 tests** passing (was 26)

### P3 — AgentHarness — DONE

- [x] Budget cap (`BudgetExhausted`)
- [x] Circuit breaker (`CircuitOpen`)
- [x] Retry with exponential backoff
- [x] Wired into `PerplexityClient` (live mode)

### P4 — Realistic mock responses — DONE

- [x] 4 mock templates: brand positive, competitor leads, hallucination, mixed
- [x] Hash-based variant selection (no longer always SoM 100%)

### Code quality — DONE

- [x] `get_owned_brand()` consolidated in `apps/api/deps.py`
- [x] Ruff per-file ignores for legacy migration/site-auditor noise

### Still pending (ROAST_REVIEW P0/P5)

- [ ] Production deploy (Vercel + Railway + Supabase)
- [ ] Langfuse + Sentry observability
- [ ] Eval pipeline (50-item labeled dataset + CI gate)
- [ ] Supabase RLS policies
- [ ] Stripe live (skipped by choice)
- [ ] Phase 7 beta users + case study

---

## Tests

```bash
pytest tests/           # 35 passed (32 unit + 1 integration + 2 harness)
cd apps/web && npm run build
ruff check apps/ packages/
```

---

## Links

- [ROAST_REVIEW.md](./ROAST_REVIEW.md) | [STRUCTURE.md](../../STRUCTURE.md) | [README.md](../../README.md)
- [PRD](./PRD.md) | [Plan](./Plan.md) | [handoff.md](./handoff.md) | [memory.md](./memory.md)
