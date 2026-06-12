# PitchMind — Project Memory

> Last updated: 2026-06-12 (Phase 5 complete)

---

## Project Identity

- **Name:** PitchMind — GEO audit SaaS
- **Repo:** https://github.com/DeryFerd/pitchmind
- **Local path:** `projects/pitchmind`

---

## Stack (locked)

| Layer | Choice |
|-------|--------|
| Frontend | Next.js 15, next-intl, Tailwind, Supabase Auth |
| API | FastAPI, JWT |
| Worker | Celery + Redis + Beat |
| Visibility | Perplexity API (mock if no key) |
| Action plan | **Ollama Cloud** — `https://ollama.com`, `gpt-oss:20b-cloud` |
| Email | Resend (optional) |
| PDF | reportlab |

---

## Completed Phases (0–5)

1. Foundation — monorepo, API, auth UI, onboarding
2. Geo engine — Perplexity, scorer, audit API
3. Site auditor — 7 checks, readiness score
4. Dashboard UI — brand/audit pages, polling, i18n switcher
5. Action plan — Ollama Cloud + template fallback, weekly email task, PDF export

---

## Key paths

```
packages/geo-engine/pitchmind_geo/
  clients/ollama_cloud.py
  action_plan.py
apps/worker/tasks/audit.py      # chains visibility → site → action plan
apps/worker/tasks/email.py      # weekly digest
apps/api/services/pdf_export.py
apps/web/components/ActionPlanList.tsx
apps/web/components/ExportPdfButton.tsx
```

---

## Env vars (server-side only — never commit)

```
OLLAMA_API_KEY=
OLLAMA_CLOUD_HOST=https://ollama.com
OLLAMA_ACTION_PLAN_MODEL=gpt-oss:20b-cloud
RESEND_API_KEY=
RESEND_FROM=PitchMind <onboarding@resend.dev>
```

---

## Dev commands

```bash
make api && make worker && make beat && make web
pytest tests/unit/   # 19 tests
```

Action plan uses Ollama Cloud when `OLLAMA_API_KEY` is set; otherwise template fallback.

---

## Conventions

- Do NOT commit API keys or add local Ollama daemon
- Action item schema: `{ priority, title, description, effort, locale }`
- Strings via `messages/en.json` + `id.json`

---

## Next: Phase 6

Stripe billing, production deploy (Railway + Vercel), tier enforcement.
