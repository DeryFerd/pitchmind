#!/usr/bin/env python3
"""Generate AI-Portfolio-Research-2026.pdf from structured content."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
OUTPUT = DOCS / "AI-Portfolio-Research-2026.pdf"

NAVY = colors.HexColor("#1a365d")
GRAY = colors.HexColor("#4a5568")
LIGHT = colors.HexColor("#f7fafc")
BORDER = colors.HexColor("#e2e8f0")

PAGE_W, PAGE_H = A4
MARGIN = 2.5 * cm


def build_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=13,
            leading=18,
            textColor=GRAY,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=NAVY,
            spaceBefore=18,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=NAVY,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=GRAY,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=GRAY,
            leftIndent=14,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=GRAY,
        ),
        "toc": ParagraphStyle(
            "TOC",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=16,
            textColor=GRAY,
            leftIndent=10,
        ),
    }


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def p(styles, kind: str, text: str):
    return Paragraph(esc(text), styles[kind])


def bullets(styles, items: list[str]):
    return [p(styles, "bullet", f"&#8226; {item}") for item in items]


def table(data: list[list[str]], col_widths=None, header=True):
    cell_style = ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=11, textColor=GRAY)
    wrapped = [[Paragraph(esc(c), cell_style) for c in row] for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(style))
    return t


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    if doc.page > 1:
        canvas.drawString(MARGIN, PAGE_H - 1.2 * cm, "AI Portfolio Research 2026")
        canvas.drawRightString(PAGE_W - MARGIN, 1.0 * cm, f"Page {doc.page}")
    canvas.restoreState()


def cover_page(styles):
    story = [
        Spacer(1, 4 * cm),
        p(styles, "cover_title", "AI/ML/DL Trends &amp;<br/>Portfolio Plan 2026"),
        Spacer(1, 0.5 * cm),
        p(styles, "cover_sub", "Full-stack AI SaaS Founder | Low-cost SLM/Edge Stack"),
        Spacer(1, 1.2 * cm),
        table(
            [
                ["Field", "Value"],
                ["Date", str(date.today())],
                ["Version", "1.0"],
                ["Target Role", "Full-stack AI SaaS Founder"],
                ["Constraint", "Low-cost (SLM / edge / open-source)"],
                ["Sources", "30+"],
                ["Confidence", "High"],
            ],
            col_widths=[5.5 * cm, 10 * cm],
        ),
        Spacer(1, 1.5 * cm),
        p(styles, "cover_sub", "Research: deep-research + brainstorming-research-ideas skills"),
        PageBreak(),
    ]
    return story


def executive_summary(styles):
    story = [p(styles, "h1", "Executive Summary")]
    story += bullets(
        styles,
        [
            "Paradigm shift 2026: dari demo chatbot ke production agent harness.",
            "Tren mainstream: multi-agent systems, DSLMs, SLM+edge, trajectory eval, MCP/A2A, physical AI.",
            "Niche diferensiasi: hybrid SLM router, agent harness, confidence scoring, GEO.",
            "Job market: recruiter cari end-to-end production (deploy, monitor, eval, cost).",
            "3 flagship projects: DocFlow, AgentOps Lite, LogSentry AI.",
            "Timeline: 12-16 minggu hingga 2-3 live SaaS dengan real users.",
        ],
    )
    return story


def toc(styles):
    story = [p(styles, "h1", "Table of Contents")]
    for item in [
        "1. Metodologi Riset",
        "2. Tren HOT 2026 (Mainstream)",
        "3. Niche &amp; Underdiscussed Topics",
        "4. Job Requirements ML/AI/LLM Engineer 2026",
        "5. Portfolio Projects (Tier 1-3)",
        "6. Roadmap Implementasi",
        "7. Architecture Template",
        "8. Perbandingan vs Tutorial Biasa",
        "Appendix A: Sources &amp; Citations",
        "Appendix B: Tech Stack Reference",
        "Appendix C: Cost Estimation",
    ]:
        story.append(p(styles, "toc", item))
    story.append(PageBreak())
    return story


def section_methodology(styles):
    return [
        p(styles, "h1", "1. Metodologi Riset"),
        p(
            styles,
            "body",
            "Framework dari skills di GLOBAL SKILLS AI AGENTS/RESEARCH: deep-research (multi-source synthesis), "
            "brainstorming-research-ideas (tension hunting, What Changed?), research router (classification + fallback).",
        ),
        table(
            [
                ["Skill", "Fungsi"],
                ["deep-research", "Multi-source synthesis, citations"],
                ["brainstorming-research-ideas", "Tension hunting, niche discovery"],
                ["research router", "Classification + fallback workflow"],
            ],
            col_widths=[5 * cm, 10.5 * cm],
        ),
        Spacer(1, 0.2 * cm),
        p(styles, "body", "Sumber primer: Gartner, Forrester, Deloitte 2026; job templates KORE1, BirJob; arXiv agent papers; SLM production guides."),
    ]


def section_hot_trends(styles):
    return [
        PageBreak(),
        p(styles, "h1", "2. Tren HOT 2026 (Mainstream)"),
        p(styles, "h2", "Paradigm Shift"),
        p(styles, "body", "DEMO CHATBOT --> PRODUCTION AGENT HARNESS (memory + guardrails + eval + deploy)"),
        p(styles, "h2", "Tren Utama"),
        table(
            [
                ["#", "Tren", "Kenapa Hot"],
                ["1", "Multi-Agent Systems", "Workflow bisnis kompleks via agent spesialis"],
                ["2", "Agent Harness", "Runtime: auth, memory, budget, HITL, observability"],
                ["3", "DSLMs", "Akurasi + compliance per industri"],
                ["4", "SLM + Edge AI", "10-30x lebih murah, latency &lt;50ms"],
                ["5", "Trajectory Evals", "Eval tool-call path, bukan final answer saja"],
                ["6", "MCP + A2A", "Standard tool integration antar agent"],
                ["7", "Physical AI", "Robot, drone, smart equipment"],
                ["8", "AI Security Platforms", "Visibility + control untuk AI apps"],
                ["9", "Hybrid Inference", "SLM 90% lokal, cloud 10% edge case"],
                ["10", "AI-Native Dev", "Tim kecil build software dengan GenAI"],
            ],
            col_widths=[1 * cm, 4.5 * cm, 10 * cm],
        ),
        Spacer(1, 0.2 * cm),
        p(styles, "h3", "Sinyal Adjacent"),
        p(styles, "body", "Synthetic data, neuromorphic computing, GEO, AI wearables, confidential computing, continual learning, world models."),
    ]


def section_niche(styles):
    return [
        PageBreak(),
        p(styles, "h1", "3. Niche &amp; Underdiscussed Topics"),
        table(
            [
                ["Niche", "Tension", "Peluang Portfolio"],
                ["Agent Harness Eng.", "Reliability vs autonomy", "Circuit breaker, budget cap"],
                ["Trajectory Eval", "Quality vs deploy speed", "Golden dataset dari traces"],
                ["Hybrid SLM Router", "Cost vs capability", "Qwen3-4B lokal, escalate 10%"],
                ["Mech. Interpretability", "Trust vs black-box", "Uncertainty probe classifier"],
                ["World Models", "Data scarcity vs quality", "Synthetic scenario generator"],
                ["Continual Learning", "Static vs evolving", "User correction -> LoRA batch"],
                ["Digital Provenance", "AI content vs trust", "Audit log per action"],
                ["DeepConf Scoring", "Know when unsure", "Auto-escalate ke human"],
                ["GEO", "SEO vs AI search", "Brand visibility audit tool"],
                ["Confidential Computing", "Privacy vs cloud", "On-device + encrypted embed"],
            ],
            col_widths=[3.8 * cm, 4.2 * cm, 7 * cm],
        ),
        Spacer(1, 0.2 * cm),
        p(styles, "h3", "Rekomendasi Triple Niche"),
        *bullets(styles, ["Hybrid SLM Router", "Agent Harness", "Trajectory Eval"]),
    ]


def section_jobs(styles):
    return [
        PageBreak(),
        p(styles, "h1", "4. Job Requirements ML/AI/LLM Engineer 2026"),
        p(styles, "h2", "Hard Skills - Semua Role"),
        *bullets(styles, ["Python (typing, async)", "Docker + CI/CD", "SQL + pipelines", "Cloud (AWS/GCP/Azure)", "Monitoring drift/latency/cost"]),
        p(styles, "h2", "ML Engineer"),
        *bullets(styles, ["PyTorch/TF end-to-end", "Model serving (Triton)", "MLOps (MLflow, W&B)", "Classical ML (XGBoost)", "LoRA fine-tuning"]),
        p(styles, "h2", "LLM Engineer"),
        *bullets(styles, ["RAG + pgvector", "LangGraph agents", "RAGAS + trajectory eval", "Langfuse/OTel", "Cost routing"]),
        p(styles, "h2", "Full-stack AI SaaS"),
        *bullets(styles, ["Supabase Auth + RBAC", "Stripe billing + metering", "Product metrics", "Domain knowledge"]),
        p(styles, "h2", "Soft Signals"),
        *bullets(styles, ["Live demo + real users", "Documented trade-offs", "Eval numbers published", "Architecture diagram", "Open-source harness component"]),
        table(
            [
                ["Role", "US Total Comp 2026"],
                ["LLM Engineer", "$170K - $420K"],
                ["ML Engineer", "$160K - $380K"],
                ["AI Engineer", "~$149K"],
            ],
            col_widths=[6 * cm, 9.5 * cm],
        ),
    ]


def section_projects(styles):
    story = [
        PageBreak(),
        p(styles, "h1", "5. Portfolio Projects"),
        p(styles, "h2", "Kriteria Wajib (Bukan Demo)"),
        *bullets(styles, ["Auth + free/paid tier", "Public URL deployed", "Real user acquisition", "Monitoring + error tracking", "Eval + cost docs"]),
        p(styles, "h2", "Tier 1 - Build First"),
    ]
    for title, detail in [
        ("DocFlow - Hybrid RAG UMKM", "OCR -> RAG -> hybrid router 90% lokal. Target: accountant, UMKM. Cost: $10-25/bulan."),
        ("AgentOps Lite - Harness + Eval SaaS", "SDK harness, trace viewer, CI eval gate. Target: indie devs. Cost: $15-30/bulan."),
        ("LogSentry AI - Hybrid Log Classifier", "XGBoost 95% + SLM explain + cloud P1. Target: solo devops. Cost: $10-20/bulan."),
    ]:
        story.append(p(styles, "h3", title))
        story.append(p(styles, "body", detail))
    story += [
        p(styles, "h2", "Tier 2"),
        *bullets(styles, ["PitchMind - GEO content audit", "VoiceBridge ID - voice agent Indonesia", "ModelRegistry Hub - MLOps solo engineers"]),
        p(styles, "h2", "Tier 3"),
        *bullets(styles, ["ContinualLearn Feed - batch LoRA adaptation", "SynthForge - synthetic data generator"]),
    ]
    return story


def section_roadmap(styles):
    return [
        PageBreak(),
        p(styles, "h1", "6. Roadmap Implementasi (12-16 minggu)"),
        table(
            [
                ["Minggu", "Milestone"],
                ["1-2", "Monorepo, Supabase, Stripe, Ollama, CI/CD"],
                ["3-6", "DocFlow MVP + 5 beta users"],
                ["7-10", "AgentOps Lite + Product Hunt launch"],
                ["11-14", "LogSentry AI"],
                ["15-16", "Case studies + demo video"],
            ],
            col_widths=[3 * cm, 12.5 * cm],
        ),
    ]


def section_architecture(styles):
    diagram = """
Next.js App
    |
FastAPI Gateway --> Supabase Auth + Stripe
    |
Hybrid SLM Router
  |-- Ollama Qwen3-4B (90%)
  |-- Cloud LLM API (10%)
    |
Agent Harness --> PostgreSQL + pgvector
    |
Langfuse + Sentry + Prometheus
"""
    return [
        PageBreak(),
        p(styles, "h1", "7. Architecture Template"),
        *[p(styles, "body", line) for line in diagram.strip().split("\n")],
    ]


def section_comparison(styles):
    return [
        p(styles, "h1", "8. Perbandingan vs Tutorial Biasa"),
        table(
            [
                ["Tutorial", "Portfolio Anda"],
                ["Jupyter notebook", "Deployed SaaS + billing"],
                ["Chat with PDF demo", "Hybrid router + cost metrics"],
                ["LangChain hello world", "Harness + circuit breaker"],
                ["Akurasi tanpa konteks", "Trajectory eval + replay"],
                ["GPT-4 only", "SLM-first documented"],
                ["No users", "5-20 beta users"],
            ],
            col_widths=[6.5 * cm, 9 * cm],
        ),
    ]


def appendix_sources(styles):
    sources = [
        "Gartner Top Strategic Technology Trends 2026",
        "Forrester Top 10 Emerging Technologies 2026",
        "Deloitte Tech Trends 2026",
        "Agentic Lexicon Jan-Feb 2026",
        "VoltAgent Awesome AI Agent Papers 2026",
        "Zylos SLM Production & Edge AI 2026",
        "Dell Edge AI Predictions 2026",
        "CODERCOPS SLM Edge Deployment",
        "LLM Observability & Evals 2026",
        "HarnessAudit (UCSB)",
        "Production Agent Harness (DEV Community)",
        "Agent Harness Observability (Rahul Kashyap)",
        "Mechanistic Interpretability 2026 (Towards AI)",
        "AgenticCareers LLM Engineer Guide 2026",
        "Howdy AI vs ML Engineer 2026",
        "KORE1 ML Engineer JD 2026",
        "BirJob ML Engineer Roadmap 2026",
        "Codebasics Production AI Projects 2026",
        "InfraSketch ML System Design Patterns",
        "GigaWorld-0 World Models (arXiv)",
        "ARROW Continual RL (arXiv)",
    ]
    story = [PageBreak(), p(styles, "h1", "Appendix A: Sources")]
    story += [p(styles, "small", f"{i}. {s}") for i, s in enumerate(sources, 1)]
    return story


def appendix_tech_cost(styles):
    return [
        PageBreak(),
        p(styles, "h1", "Appendix B: Tech Stack"),
        table(
            [
                ["Category", "Primary", "Alternative"],
                ["SLM Runtime", "Ollama", "llama.cpp"],
                ["SLM Models", "Qwen3-4B, Phi-4-mini", "Gemma 3"],
                ["Vector DB", "pgvector", "ChromaDB"],
                ["Agents", "LangGraph", "CrewAI"],
                ["Eval", "RAGAS + custom", "Braintrust"],
                ["Tracing", "Langfuse", "LangSmith"],
                ["Auth", "Supabase", "Clerk"],
                ["Billing", "Stripe", "LemonSqueezy"],
                ["Deploy", "Railway", "Fly.io"],
            ],
            col_widths=[4 * cm, 5 * cm, 5.5 * cm],
        ),
        Spacer(1, 0.4 * cm),
        p(styles, "h1", "Appendix C: Cost Estimation"),
        table(
            [
                ["Project", "Infra/mo", "API/mo", "Total/mo"],
                ["DocFlow", "$10-15", "$0-5", "$10-25"],
                ["AgentOps Lite", "$15-20", "$0", "$15-30"],
                ["LogSentry AI", "$10-15", "$0-5", "$10-20"],
                ["PitchMind", "$10", "$10-20", "$20-30"],
                ["VoiceBridge ID", "$20-30", "$10-30", "$30-60"],
            ],
            col_widths=[4 * cm, 3 * cm, 3 * cm, 3.5 * cm],
        ),
        Spacer(1, 0.5 * cm),
        p(styles, "small", "Document version 1.0 - Generated from AI-Portfolio-Research-2026.md"),
    ]


def generate():
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="AI Portfolio Research 2026",
        author="Portfolio Research",
    )
    story = []
    story += cover_page(styles)
    story += executive_summary(styles)
    story.append(PageBreak())
    story += toc(styles)
    story += section_methodology(styles)
    story += section_hot_trends(styles)
    story += section_niche(styles)
    story += section_jobs(styles)
    story += section_projects(styles)
    story += section_roadmap(styles)
    story += section_architecture(styles)
    story += section_comparison(styles)
    story += appendix_sources(styles)
    story += appendix_tech_cost(styles)
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"PDF generated: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    generate()
