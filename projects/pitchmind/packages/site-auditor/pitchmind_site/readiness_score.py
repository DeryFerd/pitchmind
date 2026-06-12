"""Weighted AI readiness score (0-100)."""

from __future__ import annotations

from pitchmind_site.types import CheckResult, SiteAuditResult

# PRD section 4.5 weights
WEIGHTS: dict[str, float] = {
    "llms_txt": 0.15,
    "robots": 0.15,
    "schema": 0.20,
    "content_h1": 0.15,
    "faq": 0.15,
    "chunks": 0.10,
    "technical": 0.10,
}


def compute_readiness_score(results: list[CheckResult]) -> int:
    by_type = {r.check_type: r.score for r in results}
    total = 0.0
    for check_type, weight in WEIGHTS.items():
        total += by_type.get(check_type, 0) * weight
    return round(total)


def merge_into_scorecard(scorecard: dict, site_result: SiteAuditResult) -> dict:
    merged = dict(scorecard)
    merged["readiness_score"] = site_result.readiness_score
    merged["site_findings"] = [
        {
            "check_type": f.check_type,
            "severity": f.severity,
            "message": f.message,
            "recommendation": f.recommendation,
        }
        for f in site_result.findings
    ]
    return merged
