# PitchMind — Progress Tracker

> Last updated: 2026-06-12  
> Current phase: **Phase 4 — Dashboard UI (in progress)**  
> Overall progress: **~70%**

---

## Quick Status

| Item | Status |
|------|--------|
| PRD | DONE |
| System Design | DONE |
| Plan | DONE |
| GitHub repo | DONE — https://github.com/DeryFerd/pitchmind |
| Phase 1 — Foundation | DONE |
| Phase 2 — Geo engine | DONE |
| Phase 3 — Site auditor | DONE |
| Phase 4 — Dashboard UI | **in_progress** |
| Supabase / Docker / deploy | DEFERRED |

---

## Phase Status

| Phase | Name | Status | Started | Completed | Notes |
|-------|------|--------|---------|-----------|-------|
| 0 | Documentation | **DONE** | 2026-06-11 | 2026-06-11 | |
| 1 | Foundation | **DONE** | 2026-06-11 | 2026-06-12 | infra deferred |
| 2 | Geo Engine | **DONE** | 2026-06-12 | 2026-06-12 | |
| 3 | Site Auditor | **DONE** | 2026-06-12 | 2026-06-12 | 17 unit tests |
| 4 | Dashboard UI | **in_progress** | 2026-06-12 | — | |
| 5 | Action Plan + Email | not_started | — | — | |
| 6 | Billing + Deploy | not_started | — | — | |
| 7 | Beta + Launch | not_started | — | — | |

---

## Phase 3 Checklist — DONE

- [x] Crawler (homepage, llms.txt, robots.txt)
- [x] 7 checks + weighted readiness score
- [x] Worker integration + DB persist
- [x] Scorecard merge + API fields
- [x] Unit tests (6 site auditor tests)

---

## Phase 4 Checklist

### 4.1 i18n

- [x] DONE — next-intl en/id (existing)
- [ ] IN PROGRESS — Dashboard + audit labels
- [ ] IN PROGRESS — Language switcher in header

### 4.2 Dashboard Pages

- [ ] IN PROGRESS — `/dashboard` — brand cards + SoM summary
- [ ] NOT STARTED — `/dashboard/brands/[id]` — scorecard overview
- [ ] NOT STARTED — `/dashboard/brands/[id]/audits/[auditId]` — audit detail
- [ ] NOT STARTED — Query results table
- [ ] NOT STARTED — Site findings checklist UI
- [ ] NOT STARTED — Competitor comparison bars

### 4.3 Audit UX

- [x] DONE — Run audit button + loading state
- [ ] NOT STARTED — Poll progress + redirect to audit page
- [ ] NOT STARTED — Empty/error states on audit pages

### 4.4 Settings

- [ ] NOT STARTED — Brand facts, competitors, queries editor

---

## Blockers (deferred)

| Blocker | Resolution |
|---------|------------|
| Docker Desktop | `make dev-up` + `make migrate` when ready |
| Supabase keys | `.env` + `apps/web/.env.local` when ready |

---

## Changelog

### 2026-06-12 — Phase 3 site auditor (DONE)

- Full `packages/site-auditor/` implementation
- Worker chains site audit; scorecard includes readiness_score
- 17 unit tests passing

### 2026-06-12 — Phase 2 geo engine (DONE)

- Geo-engine, audit API, RunAuditButton

### 2026-06-12 — Phase 1 API integration (DONE)

- Onboarding → API, protected routes, dashboard

---

## Links

- [PRD](./PRD.md) | [System Design](./system-design.md) | [Plan](./Plan.md)
- [handoff.md](./handoff.md) | [memory.md](./memory.md)
