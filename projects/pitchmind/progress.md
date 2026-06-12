# PitchMind — Progress Tracker

> Last updated: 2026-06-12  
> Current phase: **Phase 5 — Action Plan + Email (DONE)**  
> Overall progress: **~85%**

---

## Quick Status

| Item | Status |
|------|--------|
| Phase 1 — Foundation | DONE |
| Phase 2 — Geo engine | DONE |
| Phase 3 — Site auditor | DONE |
| Phase 4 — Dashboard UI | DONE |
| Phase 5 — Action Plan + Email | DONE |
| Phase 6 — Billing + Deploy | not_started |
| Supabase / Docker / deploy | DEFERRED |

---

## Phase Status

| Phase | Name | Status | Completed |
|-------|------|--------|-----------|
| 0–4 | Docs → Dashboard UI | **DONE** | 2026-06-12 |
| 5 | Action Plan + Email | **DONE** | 2026-06-12 |
| 6 | Billing + Deploy | not_started | — |
| 7 | Beta + Launch | not_started | — |

---

## Phase 5 Checklist — DONE

### 5.1 Ollama Cloud Action Plan

- [x] `clients/ollama_cloud.py` — Bearer auth, host `https://ollama.com`
- [x] `action_plan.py` — prompt → JSON items + template fallback
- [x] Worker generates ActionPlan after audit completes
- [x] Default model: `gpt-oss:20b-cloud` via `OLLAMA_ACTION_PLAN_MODEL`

### 5.2 Action Plan UI

- [x] Action plan section on audit detail page
- [x] Checkbox mark-as-done (localStorage)
- [x] Copy suggestion buttons

### 5.3 Weekly Email

- [x] Resend integration (`email.send_weekly_digest` task)
- [x] HTML digest template EN
- [x] Celery beat: Monday 09:00 UTC (`make beat`)
- [x] Skips gracefully when `RESEND_API_KEY` unset

### 5.4 PDF Export

- [x] `GET /api/v1/audits/{id}/export/pdf` (reportlab)
- [x] Download button on audit detail page

---

## Phase 5 Exit Criteria

- [x] Action plan generated for every completed audit (Ollama Cloud or template fallback)
- [x] Weekly email task + beat schedule ready (needs Resend key for live send)
- [x] PDF export works

---

## Setup (Ollama Cloud)

Add to `projects/pitchmind/.env` (never commit):

```
OLLAMA_API_KEY=your-key-from-ollama.com/settings/keys
OLLAMA_CLOUD_HOST=https://ollama.com
OLLAMA_ACTION_PLAN_MODEL=gpt-oss:20b-cloud
```

---

## Changelog

### 2026-06-12 — Phase 5 action plan + email + PDF

- Ollama Cloud client + action plan generator with template fallback
- Worker persists ActionPlan; audit detail API returns action_plan
- ActionPlanList UI (checkbox, copy), ExportPdfButton
- Weekly digest Celery task + beat schedule
- PDF export endpoint
- 19 unit tests passing

### 2026-06-12 — Phase 4 dashboard UI (DONE)

### 2026-06-12 — Phases 1–3 (DONE)

---

## Links

- [PRD](./PRD.md) | [Plan](./Plan.md) | [handoff.md](./handoff.md) | [memory.md](./memory.md)
