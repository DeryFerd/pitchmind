# PitchMind — Project Memory

> Last updated: 2026-06-13 (ROAST_REVIEW upgrades)

---

## Project Identity

- **Name:** PitchMind — GEO audit SaaS
- **Repo:** https://github.com/DeryFerd/pitchmind
- **Local path:** `projects/pitchmind`
- **Status:** MVP + ML upgrades ~96% — deploy + beta next
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
| **ML inference** | **sentence-transformers `all-MiniLM-L6-v2` — sentiment + hallucination** |
| Action plan | Ollama Cloud — `gpt-oss:20b-cloud` |
| Agent harness | Budget cap, circuit breaker, retry (Perplexity live) |
| Email | Resend — Pro/Team weekly digest only |
| PDF | reportlab |

---

## Key paths (latest)

```
packages/geo-engine/pitchmind_geo/semantic.py           # ML: embeddings, sentiment, hallucination
packages/harness/pitchmind_harness/__init__.py        # AgentHarness (budget + circuit breaker)
packages/geo-engine/pitchmind_geo/clients/perplexity.py # Realistic mocks + harness integration
apps/api/deps.py                                      # get_owned_brand() shared dependency
tests/conftest.py                                     # Fake encoder for offline unit tests
.github/workflows/ci.yml                              # pytest + ruff (no || true)
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
- **Brand facts required for good hallucination checks** — rule-based + semantic similarity
- **Perplexity only** for visibility MVP; ChatGPT/Gemini deferred to v1.1
- **ROAST_REVIEW addressed** — ML component, CI, harness, realistic mocks (2026-06-13)

---

## Dev commands

```bash
make migrate          # runs through 003
make api && make worker && make beat && make web
pytest tests/         # 35 tests
ruff check apps/ packages/
```

---

## Next session

1. Deploy Vercel (web) + Railway (API/worker) — free tiers OK
2. Supabase production + env secrets + RLS
3. Langfuse traces + Sentry error tracking
4. Run full E2E audit with real Perplexity + Ollama keys
5. Phase 7: 10 beta users, case study, Product Hunt

New contributors: start with **STRUCTURE.md** for layer map, then `handoff.md` for run commands.
