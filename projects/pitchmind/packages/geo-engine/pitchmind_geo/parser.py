"""Brand mention, citation, and sentiment parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class MentionResult:
    brand_mentioned: bool
    competitors_mentioned: dict[str, bool]
    citations: list[str]


def _normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _domain_from_url(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
        return host.removeprefix("www.")
    except Exception:
        return ""


def _fuzzy_in_text(needle: str, haystack: str) -> bool:
    norm_needle = _normalize_name(needle)
    norm_hay = _normalize_name(haystack)
    if not norm_needle:
        return False
    return norm_needle in norm_hay


def extract_mentions(
    response: str,
    brand_name: str,
    brand_website: str,
    competitors: list[str],
    citations: list[str] | None = None,
) -> MentionResult:
    citations = citations or []
    brand_domain = _domain_from_url(brand_website)

    brand_in_text = _fuzzy_in_text(brand_name, response)
    brand_in_citations = any(brand_domain and brand_domain in _domain_from_url(c) for c in citations)
    brand_mentioned = brand_in_text or brand_in_citations

    competitors_mentioned: dict[str, bool] = {}
    for comp in competitors:
        comp_in_text = _fuzzy_in_text(comp, response)
        comp_in_citations = any(
            _fuzzy_in_text(comp, c) or _fuzzy_in_text(comp, _domain_from_url(c)) for c in citations
        )
        competitors_mentioned[comp] = comp_in_text or comp_in_citations

    return MentionResult(
        brand_mentioned=brand_mentioned,
        competitors_mentioned=competitors_mentioned,
        citations=citations,
    )


_POSITIVE = re.compile(
    r"\b(best|top|leading|recommended|excellent|great|strong|popular)\b", re.I
)
_NEGATIVE = re.compile(
    r"\b(worst|avoid|poor|bad|weak|overpriced|disappointing)\b", re.I
)


def classify_sentiment(response: str, brand_name: str) -> str:
    """Rule-based sentiment for brand context (MVP)."""
    sentences = re.split(r"[.!?]\s+", response)
    brand_sentences = [s for s in sentences if _fuzzy_in_text(brand_name, s)]
    if not brand_sentences:
        return "neutral"

    text = " ".join(brand_sentences)
    if _NEGATIVE.search(text):
        return "negative"
    if _POSITIVE.search(text):
        return "positive"
    return "neutral"
