"""Compare AI claims against BrandFacts ground truth."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BrandFactsData:
    pricing: dict | None = None
    features: list[str] | None = None
    location: str | None = None
    founded_year: int | None = None


def _facts_to_strings(facts: BrandFactsData) -> list[str]:
    strings: list[str] = []
    if facts.pricing:
        monthly = facts.pricing.get("monthly") or facts.pricing.get("price")
        if monthly is not None:
            strings.append(f"Pricing is ${monthly} per month")
    if facts.features:
        strings.extend(f"Feature: {feature}" for feature in facts.features)
    if facts.location:
        strings.append(f"Located in {facts.location}")
    if facts.founded_year:
        strings.append(f"Founded in {facts.founded_year}")
    return strings


def _extract_prices(text: str) -> list[float]:
    matches = re.findall(r"\$\s*(\d+(?:\.\d+)?)", text)
    return [float(m) for m in matches]


def check_hallucinations(
    response: str,
    brand_name: str,
    facts: BrandFactsData | None,
) -> list[dict]:
    if not facts or not _brand_referenced(response, brand_name):
        return []

    flags: list[dict] = []

    if facts.pricing:
        ground_price = facts.pricing.get("monthly") or facts.pricing.get("price")
        if ground_price is not None:
            stated = _extract_prices(response)
            ground = float(ground_price)
            for price in stated:
                if ground > 0 and abs(price - ground) / ground > 0.10:
                    flags.append({
                        "type": "pricing_mismatch",
                        "stated": price,
                        "expected": ground,
                        "severity": "high",
                    })

    if facts.features:
        for feature in facts.features:
            if feature.lower() not in response.lower():
                continue
            # Feature mentioned — check if other invented features appear
        invented = _find_invented_features(response, facts.features)
        for feat in invented:
            flags.append({
                "type": "feature_hallucination",
                "stated": feat,
                "severity": "medium",
            })

    if facts.location:
        loc_lower = facts.location.lower()
        loc_pattern = re.compile(re.escape(loc_lower), re.I)
        location_claims = re.findall(
            r"(?:based in|located in|headquartered in)\s+([A-Za-z\s,]+)",
            response,
            re.I,
        )
        for claim in location_claims:
            if loc_lower not in claim.lower():
                flags.append({
                    "type": "location_mismatch",
                    "stated": claim.strip(),
                    "expected": facts.location,
                    "severity": "medium",
                })
        if location_claims and not loc_pattern.search(response):
            pass  # claims exist but don't match — already flagged above

    if facts.founded_year:
        years = [int(y) for y in re.findall(r"\b(19\d{2}|20\d{2})\b", response)]
        for year in years:
            if year != facts.founded_year and abs(year - facts.founded_year) > 1:
                flags.append({
                    "type": "founded_year_mismatch",
                    "stated": year,
                    "expected": facts.founded_year,
                    "severity": "low",
                })

    fact_strings = _facts_to_strings(facts)
    if fact_strings:
        try:
            from pitchmind_geo.semantic import detect_semantic_hallucinations

            flags.extend(detect_semantic_hallucinations(response, brand_name, fact_strings))
        except Exception as exc:
            logger.debug("Semantic hallucination check skipped: %s", exc)

    return flags


def _brand_referenced(response: str, brand_name: str) -> bool:
    return brand_name.lower() in response.lower()


_INVENTED_PATTERNS = [
    "unlimited api calls",
    "free forever",
    "enterprise-only",
    "blockchain-powered",
]


def _find_invented_features(response: str, known_features: list[str]) -> list[str]:
    known_lower = {f.lower() for f in known_features}
    invented = []
    for pattern in _INVENTED_PATTERNS:
        if pattern in response.lower() and pattern not in known_lower:
            invented.append(pattern)
    return invented
