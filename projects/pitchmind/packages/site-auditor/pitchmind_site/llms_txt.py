"""llms.txt presence and structure checks."""

from __future__ import annotations

import re

from pitchmind_site.types import CheckResult

_LINK_PATTERN = re.compile(r"\[.+?\]\(.+?\)")
_HEADING_PATTERN = re.compile(r"^#+\s+", re.MULTILINE)


def check_llms_txt(content: str, *, fetched_ok: bool) -> CheckResult:
    if not fetched_ok or not content.strip():
        return CheckResult(
            check_type="llms_txt",
            severity="fail",
            score=0,
            message="llms.txt not found or unreachable",
            recommendation="Add /llms.txt with markdown links to key pages for AI crawlers.",
        )

    has_links = bool(_LINK_PATTERN.search(content))
    has_headings = bool(_HEADING_PATTERN.search(content))
    if has_links and has_headings:
        return CheckResult(
            check_type="llms_txt",
            severity="pass",
            score=100,
            message="llms.txt present with headings and markdown links",
            recommendation=None,
        )
    if has_links or has_headings:
        return CheckResult(
            check_type="llms_txt",
            severity="partial",
            score=50,
            message="llms.txt found but structure is incomplete",
            recommendation="Include # headings and [title](url) links per llms.txt spec.",
        )
    return CheckResult(
        check_type="llms_txt",
        severity="fail",
        score=0,
        message="llms.txt exists but lacks valid markdown structure",
        recommendation="Format llms.txt with headings and markdown links to important pages.",
    )
