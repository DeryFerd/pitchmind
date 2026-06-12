# PitchMind — Progress Tracker

> Last updated: 2026-06-11  
> Current phase: **Phase 0 — Documentation**  
> Overall progress: **~20%** (docs complete + Ollama Cloud stack decision)

---

## Quick Status

| Item | Status |
|------|--------|
| PRD | Done |
| System Design | Done |
| Plan | Done |
| memory.md | Empty (by design) |
| handoff.md | Empty (by design) |
| Monorepo scaffold | Not started |
| Production URL | Not deployed |

---

## Phase Status

| Phase | Name | Status | Started | Completed | Notes |
|-------|------|--------|---------|-----------|-------|
| 0 | Documentation | **done** | 2026-06-11 | 2026-06-11 | All 6 doc files created |
| 1 | Foundation | not_started | — | — | Next: monorepo + auth |
| 2 | Geo Engine | not_started | — | — | |
| 3 | Site Auditor | not_started | — | — | |
| 4 | Dashboard UI | not_started | — | — | |
| 5 | Action Plan + Email | not_started | — | — | |
| 6 | Billing + Deploy | not_started | — | — | |
| 7 | Beta + Launch | not_started | — | — | |

---

## Current Sprint (Phase 0 -> 1 transition)

### Done

- [x] Select PitchMind (GEO) from portfolio research Tier 2
- [x] Confirm target market: hybrid EN + ID
- [x] Write PRD.md
- [x] Write system-design.md
- [x] Write Plan.md
- [x] Write progress.md (this file)
- [x] Create memory.md (empty placeholder)
- [x] Create handoff.md (empty placeholder)

### Up Next

- [ ] Self-review PRD + system-design
- [ ] Initialize monorepo (`apps/web`, `apps/api`, `apps/worker`)
- [ ] Create Supabase project
- [ ] First Alembic migration
- [ ] Landing page + auth flow

---

## Blockers

| Blocker | Owner | Since | Resolution |
|---------|-------|-------|------------|
| None | — | — | — |

---

## Metrics (post-launch targets)

| Metric | Target | Current |
|--------|--------|---------|
| Registered users | 100 | 0 |
| Beta users (1+ audit) | 10 | 0 |
| Paying Pro users | 5 | 0 |
| Audit completion rate | >90% | — |
| Avg audit duration | <5 min | — |
| Citation detection precision | >80% | — |
| Free -> Pro conversion | >5% | — |
| Monthly infra cost | <$45 | $0 |

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-11 | Project: PitchMind GEO (#4 from research) | Niche 2026, portfolio differentiation, hybrid EN+ID market gap |
| 2026-06-11 | Perplexity as primary AI engine | Has citations API; ChatGPT no bulk API |
| 2026-06-11 | **Ollama Cloud** for action plans (not local SLM) | No GPU on Railway; same ollama-python SDK; Pro $20/mo quota; models `gpt-oss:20b-cloud`, `qwen3.5:cloud` |
| 2026-06-11 | Supabase + Stripe + Railway stack | Matches portfolio research default stack |
| 2026-06-11 | memory.md + handoff.md left empty until dev starts | Per project setup request |

---

## Changelog

### 2026-06-11 (update)

- **Stack change:** Local Ollama SLM -> **Ollama Cloud** managed inference
  - API: `https://ollama.com` + `OLLAMA_API_KEY`
  - Models: `gpt-oss:20b-cloud` (action plan), `qwen3.5:cloud` (deep analysis)
  - Removed: Railway Ollama sidecar / local GPU requirement
  - Added: Ollama Cloud Pro ($20/mo) for production quota
- Updated: PRD.md, system-design.md, Plan.md, progress.md

### 2026-06-11

- Project kickoff from [AI Portfolio Research 2026](../../docs/AI-Portfolio-Research-2026.md)
- Created pre-development documentation set in `projects/pitchmind/`:
  - PRD.md
  - system-design.md
  - Plan.md
  - progress.md
  - memory.md (empty)
  - handoff.md (empty)
- Phase 0 marked complete; ready for Phase 1 (Foundation)

---

## Links

- [PRD](./PRD.md)
- [System Design](./system-design.md)
- [Plan](./Plan.md)
- [Portfolio Research](../../docs/AI-Portfolio-Research-2026.md)
