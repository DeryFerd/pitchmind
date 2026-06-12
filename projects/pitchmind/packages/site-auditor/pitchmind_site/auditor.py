"""Orchestrate full site AI-readiness audit."""

from __future__ import annotations

import httpx

from pitchmind_site.content import check_citable_chunks, check_faq_content, check_h1_and_definition
from pitchmind_site.crawler import fetch_site_pages, normalize_base_url
from pitchmind_site.llms_txt import check_llms_txt
from pitchmind_site.readiness_score import compute_readiness_score
from pitchmind_site.robots import check_robots, is_pitchmind_blocked
from pitchmind_site.schema import check_schema
from pitchmind_site.technical import check_technical
from pitchmind_site.types import CheckResult, SiteAuditResult


def run_site_audit(
    website_url: str,
    *,
    html_override: str | None = None,
    llms_override: str | None = None,
    robots_override: str | None = None,
) -> SiteAuditResult:
    """
    Run all site checks for a public HTTPS URL.

    Override params allow unit tests without network access.
    """
    base = normalize_base_url(website_url)

    if html_override is not None:
        homepage_html = html_override
        llms_content = llms_override or ""
        robots_content = robots_override or ""
        homepage_ok = True
        llms_ok = bool(llms_override)
        robots_ok = bool(robots_override)
        blocked = is_pitchmind_blocked(robots_content) if robots_content else False
    else:
        with httpx.Client(timeout=15.0, follow_redirects=True, trust_env=False) as client:
            pages = fetch_site_pages(base, client)
        homepage = pages["homepage"]
        llms = pages["llms_txt"]
        robots = pages["robots_txt"]

        if not homepage.ok:
            return SiteAuditResult(
                readiness_score=0,
                findings=[
                    CheckResult(
                        check_type="technical",
                        severity="fail",
                        score=0,
                        message=f"Homepage unreachable: {homepage.error or homepage.status_code}",
                        recommendation="Ensure the website URL is public and returns HTTP 200.",
                    )
                ],
            )

        homepage_html = homepage.text
        llms_content = llms.text if llms.ok else ""
        robots_content = robots.text if robots.ok else ""
        homepage_ok = homepage.ok
        llms_ok = llms.ok
        robots_ok = robots.ok
        blocked = is_pitchmind_blocked(robots_content) if robots_ok else False

    findings: list[CheckResult] = [
        check_llms_txt(llms_content, fetched_ok=llms_ok),
        check_robots(robots_content, fetched_ok=robots_ok),
        check_schema(homepage_html),
        check_h1_and_definition(homepage_html),
        check_faq_content(homepage_html),
        check_citable_chunks(homepage_html),
        check_technical(homepage_html, base),
    ]

    score = compute_readiness_score(findings)
    return SiteAuditResult(readiness_score=score, findings=findings, blocked_by_robots=blocked)
