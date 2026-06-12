# PitchMind — Product Requirements Document

> Version: 1.0  
> Last updated: 2026-06-11  
> Status: MVP ~95% — core product complete; deploy + beta pending  
> Owner: Full-stack AI SaaS Portfolio

---

## 1. Overview

| Field | Value |
|-------|-------|
| **Product name** | PitchMind |
| **Tagline** | Know if AI recommends you — before your customers ask |
| **Category** | Generative Engine Optimization (GEO) SaaS |
| **Target market** | Hybrid EN + ID (global marketers + Indonesia/SEA UMKM & agencies) |

### Problem Statement

Traditional SEO measures Google rankings, but an increasing share of discovery happens inside AI answer engines — ChatGPT, Perplexity, Gemini, Google AI Overviews. Brands have no visibility into:

- Whether AI mentions them for high-intent category queries
- Whether AI states **correct** facts (pricing, features, location)
- How they compare to competitors in AI-generated answers
- Whether their website is technically readable by AI crawlers (`llms.txt`, schema, bot access)

SEO tools do not solve this. Marketing teams fly blind while competitors capture "Share of Model."

### Solution

PitchMind is an end-to-end GEO audit platform that:

1. Runs a **golden query set** (English + Indonesian) against AI engines
2. Scores **citation rate**, **accuracy**, and **competitor gap**
3. Audits the brand website for **AI readiness** (technical GEO foundations)
4. Generates a **prioritized action plan** (Ollama Cloud LLM — managed inference, no local GPU)
5. Delivers **weekly email reports** for ongoing monitoring

### Why Now (2026)

- Deloitte Tech Trends 2026 lists GEO as an adjacent signal maturing into dominant force
- No native "AI Search Console" exists — tooling gap is wide open
- B2B SaaS and local businesses in ID/SEA are underserved by English-only GEO platforms
- Portfolio differentiation: niche, production-grade, bilingual, **Ollama Cloud** stack (no self-hosted GPU)

---

## 2. Goals & Non-Goals

### Goals (MVP)

| # | Goal |
|---|------|
| G1 | Measure brand visibility across Perplexity + spot-check ChatGPT/Gemini |
| G2 | Support golden query sets in **English and Indonesian** |
| G3 | Detect hallucinations vs user-defined brand facts |
| G4 | Audit site AI-readiness: `llms.txt`, JSON-LD, AI bot access |
| G5 | Generate actionable fix list without manual consultant |
| G6 | Ship as real SaaS: auth, billing, public URL, real users |
| G7 | Complete standard audit (25 queries) in under 5 minutes |

### Non-Goals (v1)

| # | Non-Goal | Reason |
|---|----------|--------|
| NG1 | Full content CMS / auto-publish | Scope creep; focus audit first |
| NG2 | Real-time SERP scraping at enterprise scale | Cost prohibitive for MVP |
| NG3 | Enterprise SSO / SAML | Post-PMF |
| NG4 | White-label agency portal | v2 feature |
| NG5 | Guaranteed ranking improvement | GEO is influence, not control |
| NG6 | Official ChatGPT API bulk audit | No public API; use Perplexity + manual spot-check |

---

## 3. Target Users

### Primary Personas

**Persona A — "Alex" (Global EN)**  
- Role: SaaS marketing manager / indie founder  
- Goal: Know if ChatGPT recommends their product vs competitors  
- Pain: Hears "I asked ChatGPT and it didn't mention us" from sales  
- Budget: $19-49/mo self-serve

**Persona B — "Sari" (Indonesia ID)**  
- Role: Marketing staff at UMKM or small agency  
- Goal: Simple report in Bahasa — "Apakah AI merekomendasikan brand kami?"  
- Pain: English-only tools, no local query templates  
- Budget: Sensitive; needs free tier to evaluate

**Persona C — "Agency Dev" (Hybrid)**  
- Role: Freelance digital marketer serving 5-10 clients  
- Goal: White-label-ready reports (future), multi-brand dashboard  
- Pain: Manual checking ChatGPT per client is tedious

### User Needs Summary

| Need | Priority |
|------|----------|
| Simple onboarding (brand URL + competitors) | P0 |
| Bilingual UI (EN/ID toggle) | P0 |
| Clear scorecard, not raw AI dumps | P0 |
| Actionable fixes, not jargon | P1 |
| Weekly monitoring without logging in daily | P1 |
| Export PDF for client/stakeholder | P2 |

---

## 4. Core Features (MVP)

### 4.1 Brand Workspace

- Create workspace with brand name, website URL, description (ground truth)
- Add up to 5 competitors (Pro) or 2 (Free)
- Define brand facts: pricing, key features, location, founding year (for hallucination check)
- Language preference: EN, ID, or both for query sets

### 4.2 Golden Query Builder

- Pre-built templates by category: SaaS, local service, e-commerce, personal brand
- 20-30 queries per audit covering: category discovery, comparison, pricing, "best X for Y"
- Custom query add/edit
- Bilingual: duplicate query set in EN + ID or run separate sets

**Example queries (EN):**
- "Best project management tools for remote teams"
- "How much does [Brand] cost?"
- "[Brand] vs [Competitor]"

**Example queries (ID):**
- "Software manajemen proyek terbaik untuk tim remote"
- "Berapa harga [Brand]?"
- "[Brand] vs [Competitor] mana lebih bagus?"

### 4.3 AI Visibility Scan

| Engine | MVP Approach |
|--------|--------------|
| **Perplexity** | Primary — API with citations |
| **ChatGPT** | Spot-check via manual golden-set UI or optional automation (Pro) |
| **Gemini** | Spot-check 5 queries per audit (Free: 2) |
| **Google AI Overviews** | Indirect via query simulation + future integration |

**Output per query:**
- Raw AI response
- Brand mentioned: yes/no
- Competitors mentioned
- Citation URLs (if available)
- Sentiment: positive / neutral / negative / not mentioned
- Accuracy flags vs ground truth

### 4.4 Scoring Engine

| Metric | Definition |
|--------|------------|
| **Share of Model (SoM)** | % of golden queries where brand is cited or recommended |
| **Citation Accuracy Score** | % of mentions where stated facts match ground truth |
| **Competitor Gap Index** | SoM(brand) - SoM(top competitor) |
| **Hallucination Risk Count** | Queries where AI states incorrect facts about brand |
| **AI Readiness Score** | 0-100 from site technical audit |

### 4.5 Site AI-Readiness Audit

Automated crawl checks:

| Check | Weight |
|-------|--------|
| `llms.txt` present and valid | 15% |
| `robots.txt` allows GPTBot, ClaudeBot, PerplexityBot | 15% |
| JSON-LD Organization / LocalBusiness schema | 20% |
| Homepage H1 + 40-word definition block | 15% |
| FAQ or Q&A structured content | 15% |
| Citable chunks (130-170 word segments) | 10% |
| HTTPS, mobile-friendly, page speed baseline | 10% |

### 4.6 Action Plan Generator

- Input: audit results + site findings
- Engine: **[Ollama Cloud](https://docs.ollama.com/cloud)** — managed LLM inference via `https://ollama.com/api`
- Default model: `gpt-oss:20b-cloud` (level 1-2, cost-efficient) or `qwen3.5:cloud`
- Auth: `OLLAMA_API_KEY` from [ollama.com/settings/keys](https://ollama.com/settings/keys)
- Same `ollama-python` SDK — only `host` changes to `https://ollama.com`
- No local GPU or Ollama daemon required on server
- Output: prioritized list (P0/P1/P2 fixes) with:
  - What to fix
  - Why it matters for GEO
  - Estimated effort (quick / medium / project)
  - Example copy suggestion (EN + ID where relevant)

### 4.7 Weekly Email Report

- Resend email digest every Monday
- Sections: SoM trend, new hallucinations, top 3 actions, competitor movement
- Link to full dashboard
- Unsubscribe / frequency settings

### 4.8 Billing & Tiers

| Tier | Price | Brands | Queries/mo | Site audits | Reports | Seats |
|------|-------|--------|------------|-------------|---------|-------|
| **Free** | $0 | 1 | 10 | 1 | Monthly | 1 |
| **Pro** | $19/mo | 5 | 200 | 4 | Weekly | 1 |
| **Team** | $49/mo | 20 | 1000 | 20 | Weekly | 3 |

Stripe Checkout + Customer Portal for self-serve upgrade.

---

## 5. User Stories

### P0 — Must Have

| ID | Story | Acceptance Criteria |
|----|-------|---------------------|
| US-01 | As a new user, I want to sign up with email/Google so I can start an audit in <3 min | Auth works; redirect to onboarding |
| US-02 | As a user, I want to enter my brand URL and 2 competitors so I can benchmark visibility | Brand + competitors saved; validation on URL |
| US-03 | As a user, I want to run a pre-filled golden query set in EN and ID so I cover both markets | 25 queries run; results tagged by language |
| US-04 | As a user, I want a scorecard showing SoM and accuracy so I understand performance at a glance | Dashboard shows 4 core metrics |
| US-05 | As a user, I want hallucination alerts when AI states wrong pricing so I can fix source content | Flag shown with diff vs ground truth |
| US-06 | As a free user, I want 1 brand and 10 queries/month so I can evaluate before paying | Limits enforced; upgrade prompt at cap |
| US-07 | As a user, I want the UI in English or Bahasa Indonesia so I can use my preferred language | i18n toggle; core flows translated |

### P1 — Should Have

| ID | Story | Acceptance Criteria |
|----|-------|---------------------|
| US-08 | As a user, I want a site audit report so I know technical GEO gaps | 7 checks scored; findings listed |
| US-09 | As a user, I want an AI-generated action plan so I know what to do next | 5-15 prioritized items from Ollama Cloud |
| US-10 | As a Pro user, I want weekly email reports so I monitor without daily login | Email sent; contains score delta |
| US-11 | As a user, I want to export PDF report for my client/boss | PDF download with logo + scores |

### P2 — Nice to Have (post-MVP)

| ID | Story |
|----|-------|
| US-12 | As an agency user, I want multiple workspaces under one account |
| US-13 | As a user, I want historical trend charts (SoM over 90 days) |
| US-14 | As a user, I want Slack notification when hallucination detected |

---

## 6. User Flows

### Flow 1: First Audit (Happy Path)

```
Sign up -> Onboarding (brand + competitors + facts) -> Select query template (EN/ID)
-> Run audit -> Wait (<5 min) -> Scorecard -> Site audit tab -> Action plan -> Upgrade CTA
```

### Flow 2: Weekly Monitoring (Pro)

```
Email received -> Click dashboard -> Review delta -> Mark action items done -> Re-run spot-check
```

### Flow 3: Hallucination Response

```
Alert on dashboard -> View incorrect AI statement -> See suggested source fix
-> Edit website/LinkedIn -> Re-run affected queries -> Confirm accuracy improved
```

---

## 7. Key Metrics

### Product Metrics

| Metric | Target (90 days post-launch) |
|--------|------------------------------|
| Registered users | 100 |
| Beta users (completed 1+ audit) | 10 |
| Paying users | 5 |
| Audit completion rate | >90% |
| Avg audit duration | <5 min (25 queries) |
| Weekly email open rate | >25% |
| Free -> Pro conversion | >5% |

### Technical Metrics

| Metric | Target |
|--------|--------|
| Citation detection precision | >80% |
| Hallucination flag recall | >70% |
| API cost per audit (25 queries + action plan) | <$0.60 |
| Uptime | >99% |
| P95 API response (non-audit) | <500ms |

---

## 8. Pricing Rationale

- **Free tier:** Acquisition + portfolio demo; strict limits prevent abuse
- **Pro $19:** Below Evertune/enterprise GEO tools ($100+); accessible for indie/SMB
- **Team $49:** Agency-lite; 3 seats covers small team
- Cost to serve Pro user: ~$5-12/mo (infra + Perplexity + Ollama Cloud quota) -> healthy margin at scale

---

## 9. Success Criteria (MVP Launch)

- [ ] Public URL deployed and stable
- [ ] Auth (Supabase) + Stripe billing live
- [ ] Full audit pipeline works EN + ID
- [ ] 10 beta users with real brands (not fake data)
- [ ] At least 1 paying Pro user within 30 days
- [ ] Case study documented with before/after SoM screenshot
- [ ] Portfolio README links to live demo

---

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Perplexity API cost at scale | High | Cache 7 days; batch queries; tier limits |
| Non-deterministic AI answers | Medium | 3 samples per query; report median; note variance |
| No ChatGPT bulk API | Medium | Perplexity primary; manual spot-check UI |
| Low ID market willingness to pay | Medium | Free tier generous; ID templates; local community GTM |
| Ollama Cloud quota exhausted | Medium | Use level 1-2 models; cache action plans; Pro account ($20/mo) for dev |
| Ollama Cloud model deprecation | Low | Pin model version; monitor [Ollama deprecations](https://docs.ollama.com/cloud) |
| Competitor platforms (Evertune, LLMClicks) | Low | Differentiate on price + bilingual + Ollama Cloud stack |
| Legal: scraping AI responses | Medium | Use official APIs where available; store only audit metadata |

---

## 11. Compliance & Privacy

- Store AI responses only for user's own audit history (not shared)
- GDPR-ready: data export + delete account
- No selling of audit data to third parties
- Terms: audit results are indicative, not guaranteed outcomes

---

## 12. Roadmap (Post-MVP)

| Version | Features |
|---------|----------|
| v1.1 | Historical trends, PDF white-label |
| v1.2 | Slack/webhook alerts, agency multi-workspace |
| v2.0 | Content optimizer (suggest citable chunks), MCP integration for site agents |
| v2.1 | API for agencies, bulk client import |

---

## 13. References

- [AI Portfolio Research 2026](../../docs/AI-Portfolio-Research-2026.md) — Project #4 PitchMind
- [GEO Playbook for SaaS](https://llmclicks.ai/blog/generative-engine-optimization-geo-saas/)
- [Top GEO Platforms 2026 — Evertune](https://www.evertune.ai/resources/insights-on-ai/top-15-generative-engine-optimization-geo-platforms-for-2026)
- [llms.txt, MCP, Schema — GEO 2026](https://predictadigital.com.au/blog/llms-txt-mcp-schema-geo-2026/)
- [Ollama Cloud Documentation](https://docs.ollama.com/cloud)
- [Ollama Cloud Models Blog](https://ollama.com/blog/cloud-models)
- [AI Citation Ranking — RAG Signal](https://ragsignal.com/ai-citation-ranking/)
- Deloitte Tech Trends 2026 — GEO as adjacent signal

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **GEO** | Generative Engine Optimization — optimizing for AI answer engines |
| **SoM** | Share of Model — % queries where brand appears in AI response |
| **Golden queries** | Curated high-intent questions representing buyer searches |
| **Hallucination (GEO context)** | AI states incorrect facts about brand |
| **AI Readiness** | Technical site preparedness for AI crawlers and citation |
| **Citable chunk** | 130-170 word self-contained content block AI can extract |
| **Ollama Cloud** | Managed LLM inference at ollama.com — cloud-hosted models via same Ollama API, no local GPU |
