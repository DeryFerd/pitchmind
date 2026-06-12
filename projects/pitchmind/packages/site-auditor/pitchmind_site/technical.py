"""Technical baseline checks (HTTPS, mobile meta)."""

from __future__ import annotations

import re

from pitchmind_site.types import CheckResult


def check_technical(html: str, base_url: str) -> CheckResult:
    score = 0
    notes: list[str] = []

    if base_url.startswith("https://"):
        score += 40
        notes.append("HTTPS")
    else:
        notes.append("not HTTPS")

    if re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.I):
        score += 30
        notes.append("viewport meta")
    else:
        notes.append("no viewport meta")

    if re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'].{20,}', html, re.I):
        score += 30
        notes.append("meta description")
    else:
        notes.append("weak meta description")

    if score >= 90:
        severity, recommendation = "pass", None
    elif score >= 50:
        severity = "partial"
        recommendation = "Ensure HTTPS, mobile viewport meta, and a descriptive meta tag."
    else:
        severity = "fail"
        recommendation = "Fix HTTPS, add viewport meta, and write a 20+ char meta description."

    return CheckResult(
        check_type="technical",
        severity=severity,
        score=min(score, 100),
        message=f"Technical baseline: {', '.join(notes)}",
        recommendation=recommendation,
    )
