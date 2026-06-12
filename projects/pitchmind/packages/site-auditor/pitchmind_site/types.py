"""Shared types for site audit findings."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CheckResult:
    check_type: str
    severity: str  # pass | partial | fail
    score: int  # 0, 50, 100
    message: str
    recommendation: str | None = None


@dataclass
class SiteAuditResult:
    readiness_score: int
    findings: list[CheckResult]
    blocked_by_robots: bool = False
