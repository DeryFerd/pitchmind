# PitchMind — Project Memory

> Last updated: 2026-06-12 (Phase 4 complete)

---

## Project Identity

- **Name:** PitchMind — GEO audit SaaS
- **Repo:** https://github.com/DeryFerd/pitchmind
- **Local path:** `projects/pitchmind`

---

## Stack (locked)

Next.js 15 + next-intl | FastAPI | Celery + Redis | PostgreSQL | Perplexity (mock ok) | Ollama Cloud (Phase 5)

---

## Completed

| Phase | Key deliverables |
|-------|------------------|
| 1 | Monorepo, auth UI, onboarding→API, CI |
| 2 | geo-engine, audit API, Celery visibility task |
| 3 | site-auditor, readiness score, worker chain |
| 4 | Dashboard UI: brand page, audit detail, polling, i18n switcher |

---

## Web routes

```
/[locale]/dashboard
/[locale]/dashboard/brands/[id]
/[locale]/dashboard/brands/[id]/audits/[auditId]
```

Components: `DashboardHeader`, `LanguageSwitcher`, `ScorecardCards`, `CompetitorGapChart`, `QueryResultsTable`, `SiteFindingsList`, `RunAuditButton`

---

## Deferred

- Docker + Supabase (E2E auth/DB)
- Phase 5: Ollama Cloud action plan
- Phase 6: Stripe, deploy
- Settings pages (brand facts editor)

---

## Dev

```bash
make dev-up && make migrate && make api && make worker && make web
pytest tests/unit/   # 17 tests, no infra
```

---

## Conventions

- Strings: `messages/en.json` + `id.json`
- i18n navigation: `@/i18n/routing` (Link, useRouter, usePathname)
- API prefix: `/api/v1`
