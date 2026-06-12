"""Site auditor: llms.txt, schema, bot checker."""

from pitchmind_site.auditor import run_site_audit
from pitchmind_site.readiness_score import compute_readiness_score, merge_into_scorecard
from pitchmind_site.types import CheckResult, SiteAuditResult

__all__ = [
    "CheckResult",
    "SiteAuditResult",
    "compute_readiness_score",
    "merge_into_scorecard",
    "run_site_audit",
]
