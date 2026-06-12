"""JSON-LD structured data checks."""

from __future__ import annotations

import json
import re

from pitchmind_site.types import CheckResult

_JSON_LD_PATTERN = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)


def _extract_types(blocks: list[dict]) -> set[str]:
    types: set[str] = set()
    for block in blocks:
        t = block.get("@type")
        if isinstance(t, list):
            types.update(str(x) for x in t)
        elif t:
            types.add(str(t))
        if "@graph" in block:
            for node in block["@graph"]:
                if isinstance(node, dict) and "@type" in node:
                    nt = node["@type"]
                    if isinstance(nt, list):
                        types.update(str(x) for x in nt)
                    else:
                        types.add(str(nt))
    return types


def _parse_json_ld(html: str) -> list[dict]:
    blocks: list[dict] = []
    for match in _JSON_LD_PATTERN.finditer(html):
        raw = match.group(1).strip()
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                blocks.extend(item for item in data if isinstance(item, dict))
            elif isinstance(data, dict):
                blocks.append(data)
        except json.JSONDecodeError:
            continue
    return blocks


def check_schema(html: str) -> CheckResult:
    blocks = _parse_json_ld(html)
    if not blocks:
        return CheckResult(
            check_type="schema",
            severity="fail",
            score=0,
            message="No JSON-LD structured data found",
            recommendation="Add Organization or LocalBusiness schema via application/ld+json.",
        )

    types = _extract_types(blocks)
    has_org = any(t in ("Organization", "LocalBusiness", "Corporation") for t in types)
    has_faq = "FAQPage" in types

    if has_org and has_faq:
        return CheckResult(
            check_type="schema",
            severity="pass",
            score=100,
            message="JSON-LD includes Organization/LocalBusiness and FAQPage",
            recommendation=None,
        )
    if has_org:
        return CheckResult(
            check_type="schema",
            severity="partial",
            score=75,
            message="Organization/LocalBusiness schema found; FAQPage missing",
            recommendation="Add FAQPage JSON-LD for common buyer questions.",
        )
    return CheckResult(
        check_type="schema",
        severity="partial",
        score=50,
        message=f"JSON-LD found but missing Organization schema (types: {', '.join(sorted(types))})",
        recommendation="Add Organization schema with name, url, and logo.",
    )
