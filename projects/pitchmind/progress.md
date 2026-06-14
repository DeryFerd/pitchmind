# PitchMind — Progress Tracker

> Last updated: 2026-06-13  
> Current phase: **MVP hardened — deploy + beta pending (credential-gated)**  
> Overall progress: **~97%**

---

## Quick Status

| Item | Status |
|------|--------|
| Phases 1–5 (core product) | DONE |
| Phase 6 billing (code) | DONE (Stripe live skipped) |
| ROAST_REVIEW P1–P4 (ML, CI, harness, mocks) | **DONE** |
| ROAST_REVIEW round 2 (no credentials) | **DONE** |
| Production deploy | skipped — needs credentials |
| Phase 7 beta + launch | skipped — needs deploy + users |

---

## Latest: ROAST_REVIEW round 2 (2026-06-13)

### Code quality — DONE

- [x] Removed `sys.path.insert` from apps/tests — `PYTHONPATH` in Makefile + `tests/conftest.py`
- [x] SSE audit progress via **Redis pub/sub** (`audit:progress:{id}`); DB fallback poll 5s
- [x] Worker publishes progress per query + terminal status

### Testing — DONE

- [x] **API route tests** (`TestClient` + dependency overrides)
- [x] **ML eval pipeline** — 30-item labeled dataset + precision/recall/F1 CI gate
- [x] Audit progress unit tests
- [x] **41 tests** passing (was 35)
- [x] CI: `.env` tracked-file guard

### Skipped (credential / external)

- [ ] Production deploy (Vercel + Railway + Supabase)
- [ ] Langfuse + Sentry
- [ ] Supabase RLS live apply
- [ ] Stripe live
- [ ] Phase 7 beta users

---

## Tests

```bash
make test               # pytest via Makefile PYTHONPATH
pytest tests/           # 41 passed
ruff check apps/ packages/
```

---

## Links

- [STRUCTURE.md](../../STRUCTURE.md) | [README.md](../../README.md)
- [PRD](./PRD.md) | [Plan](./Plan.md) | [handoff.md](./handoff.md) | [memory.md](./memory.md)
