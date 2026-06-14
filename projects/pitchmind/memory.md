# PitchMind — Project Memory

> Last updated: 2026-06-13 (ROAST_REVIEW round 2)

---

## Project Identity

- **Name:** PitchMind — GEO audit SaaS
- **Repo:** https://github.com/DeryFerd/pitchmind
- **Local path:** `projects/pitchmind`
- **Status:** MVP hardened ~97% — deploy + beta blocked on credentials only
- **Architecture map:** [STRUCTURE.md](../../STRUCTURE.md)
- **Portfolio README:** [README.md](../../README.md)

---

## Stack (locked)

| Layer | Choice |
|-------|--------|
| Frontend | Next.js 15, next-intl, Tailwind, Supabase Auth |
| API | FastAPI, JWT, tier limits (Stripe code present, live skipped) |
| Worker | Celery + Redis + Beat |
| Visibility | Perplexity API (mock if no key, 7-day Redis cache) |
| ML inference | sentence-transformers `all-MiniLM-L6-v2` — sentiment + hallucination |
| Action plan | Ollama Cloud — `gpt-oss:20b-cloud` |
| Agent harness | Budget cap, circuit breaker, retry (Perplexity live) |
| SSE progress | Redis pub/sub `audit:progress:{id}` |
| Email | Resend — Pro/Team weekly digest only |
| PDF | reportlab |

---

## Key paths (latest)

```
packages/db/pitchmind_db/audit_progress.py          # Redis pub/sub for SSE
apps/api/services/audit_stream.py                   # SSE generator (pub/sub + fallback)
tests/eval/fixtures/ml_eval_dataset.json          # 30-item labeled ML eval set
tests/eval/test_ml_eval.py                          # precision/recall/F1 CI gate
tests/unit/test_api_routes.py                       # FastAPI route tests
tests/conftest.py                                   # PYTHONPATH bootstrap + fake encoder
Makefile                                            # unified PYTHONPATH for api/worker/test
```

---

## Dev commands

```bash
make migrate && make api && make worker && make web
make test             # 41 tests
make lint
```

`PYTHONPATH=packages/db;packages/geo-engine;packages/site-auditor;packages/harness;.`

---

## Next session (credential-gated)

1. Deploy Vercel + Railway + Supabase + Upstash
2. Supabase RLS + production secrets
3. Langfuse + Sentry (optional keys in `.env.example`)
4. Phase 7: 10 beta users, case study, Product Hunt

New contributors: **STRUCTURE.md** → `handoff.md` → `make test`.
