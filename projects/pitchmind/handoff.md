# PitchMind — Handoff

> **Stop point:** Phase 3 Site Auditor complete (code); Phase 4 Dashboard UI next  
> **Date:** 2026-06-12  
> **Repo:** https://github.com/DeryFerd/pitchmind

---

## Where We Stopped

Full audit pipeline: **visibility (Phase 2) + site readiness (Phase 3)** in one Celery task. Unit tests pass without Docker/Supabase. Infra still deferred.

---

## Deferred (OK later)

Docker, Supabase, Perplexity API key, deploy — same as before.

---

## Next: Phase 4 — Dashboard UI

- `/dashboard/brands/[id]` — scorecard + readiness score
- Audit detail page with query results + site findings
- Poll audit status after "Run audit"
- Language switcher

See [Plan.md](./Plan.md) Phase 4 section.

---

## Phase 3 Delivered

| Module | Path |
|--------|------|
| Crawler | `packages/site-auditor/pitchmind_site/crawler.py` |
| llms.txt check | `llms_txt.py` |
| robots.txt AI bots | `robots.py` |
| JSON-LD schema | `schema.py` |
| Content (H1, FAQ, chunks) | `content.py` |
| Technical baseline | `technical.py` |
| Readiness scorer | `readiness_score.py` |
| Orchestrator | `auditor.py` |
| Worker integration | `apps/worker/tasks/audit.py` |

### Audit flow

```
POST /audits (include_site_audit: true)
  → visibility batch (Perplexity mock/real)
  → site crawl + 7 checks
  → scorecard { share_of_model, readiness_score, site_findings[] }
```

### Tests

```bash
pytest tests/unit/   # 17 passed
```

---

## Key Files

- [progress.md](./progress.md) — live status
- [memory.md](./memory.md) — conventions
- `packages/site-auditor/pitchmind_site/auditor.py`
