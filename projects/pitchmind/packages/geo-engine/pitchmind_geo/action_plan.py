"""Generate prioritized GEO action plans from audit results."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from pitchmind_geo.clients.ollama_cloud import OllamaCloudClient

logger = logging.getLogger(__name__)

ACTION_PLAN_SYSTEM = """You are a GEO (Generative Engine Optimization) consultant.
Return ONLY a valid JSON array of action items. No markdown, no explanation.
Each item must have: priority (P0|P1|P2), title, description, effort (quick|medium|project), locale (en|id).
Provide 4-8 items covering visibility gaps, hallucinations, and site readiness fixes.
Include at least one item in Indonesian (locale: id) and one in English (locale: en)."""


def _parse_json_array(text: str) -> list[dict[str, Any]]:
    text = text.strip()
    match = re.search(r"\[[\s\S]*\]", text)
    if not match:
        raise ValueError("No JSON array in response")
    data = json.loads(match.group())
    if not isinstance(data, list):
        raise ValueError("Expected JSON array")
    return _normalize_items(data)


def _normalize_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append({
            "priority": str(item.get("priority", "P1"))[:2],
            "title": str(item.get("title", "GEO improvement"))[:200],
            "description": str(item.get("description", ""))[:1000],
            "effort": str(item.get("effort", "medium")),
            "locale": str(item.get("locale", "en"))[:2],
        })
    return normalized[:10]


def template_action_plan(
    brand_name: str,
    scorecard: dict | None,
    site_findings: list[dict] | None,
) -> list[dict[str, Any]]:
    """Fallback plan when Ollama Cloud is unavailable."""
    items: list[dict[str, Any]] = []
    sc = scorecard or {}

    som = sc.get("share_of_model", 0)
    if som < 50:
        items.append({
            "priority": "P0",
            "title": "Improve AI visibility (Share of Model)",
            "description": (
                f"{brand_name} appears in only {som}% of golden queries. "
                "Publish citable FAQ content and ensure brand facts match across your site."
            ),
            "effort": "medium",
            "locale": "en",
        })
        items.append({
            "priority": "P0",
            "title": "Tingkatkan visibilitas AI (Share of Model)",
            "description": (
                f"{brand_name} hanya muncul di {som}% query emas. "
                "Terbitkan konten FAQ yang mudah dikutip dan selaraskan fakta brand di situs."
            ),
            "effort": "medium",
            "locale": "id",
        })

    readiness = sc.get("readiness_score")
    if readiness is not None and readiness < 70:
        items.append({
            "priority": "P1",
            "title": "Fix site AI readiness gaps",
            "description": f"Readiness score is {readiness}/100. Address llms.txt, schema markup, and AI bot access.",
            "effort": "quick",
            "locale": "en",
        })

    for finding in (site_findings or []):
        if finding.get("severity") in ("fail", "partial") and finding.get("recommendation"):
            items.append({
                "priority": "P1" if finding.get("severity") == "fail" else "P2",
                "title": f"Fix: {finding.get('check_type', 'site check')}",
                "description": finding["recommendation"],
                "effort": "quick",
                "locale": "en",
            })

    if sc.get("hallucination_count", 0) > 0:
        items.append({
            "priority": "P0",
            "title": "Correct AI hallucinations about your brand",
            "description": "Update pricing, features, and facts pages so AI crawlers index accurate information.",
            "effort": "medium",
            "locale": "en",
        })

    if not items:
        items.append({
            "priority": "P2",
            "title": "Maintain GEO momentum",
            "description": f"Continue monitoring {brand_name} visibility and refresh golden queries monthly.",
            "effort": "quick",
            "locale": "en",
        })

    return items[:8]


def build_action_plan_prompt(
    brand_name: str,
    scorecard: dict | None,
    site_findings: list[dict] | None,
) -> str:
    sc = scorecard or {}
    findings_text = json.dumps(site_findings or [], indent=2)[:2000]
    return f"""Brand: {brand_name}

Audit scorecard:
- Share of Model: {sc.get('share_of_model', 'N/A')}%
- Citation accuracy: {sc.get('citation_accuracy', 'N/A')}
- AI Readiness: {sc.get('readiness_score', 'N/A')}/100
- Hallucination flags: {sc.get('hallucination_count', 0)}
- Competitor SoM: {json.dumps(sc.get('competitor_som', {}))}

Site findings (fail/partial):
{findings_text}

Generate a prioritized GEO action plan as JSON array."""


def generate_action_plan(
    brand_name: str,
    scorecard: dict | None,
    site_findings: list[dict] | None,
    *,
    client: OllamaCloudClient | None = None,
) -> tuple[list[dict[str, Any]], str]:
    """
    Returns (items, source) where source is 'ollama_cloud' or 'template'.
    """
    ollama = client or OllamaCloudClient()
    site = site_findings or (scorecard or {}).get("site_findings")

    if ollama.available:
        try:
            raw = ollama.chat(
                build_action_plan_prompt(brand_name, scorecard, site),
                system=ACTION_PLAN_SYSTEM,
            )
            items = _parse_json_array(raw)
            if items:
                return items, "ollama_cloud"
        except Exception as exc:
            logger.warning("Ollama Cloud action plan failed, using template: %s", exc)

    return template_action_plan(brand_name, scorecard, site), "template"
