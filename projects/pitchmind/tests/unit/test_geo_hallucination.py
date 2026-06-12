import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "geo-engine"))

from pitchmind_geo.hallucination import BrandFactsData, check_hallucinations


def test_pricing_mismatch_detected():
    facts = BrandFactsData(pricing={"monthly": 19})
    flags = check_hallucinations(
        "PitchMind costs $99 per month for the pro plan.",
        "PitchMind",
        facts,
    )
    assert any(f["type"] == "pricing_mismatch" for f in flags)


def test_no_flags_without_brand_reference():
    facts = BrandFactsData(pricing={"monthly": 19})
    flags = check_hallucinations("CompetitorX costs $99 per month.", "PitchMind", facts)
    assert flags == []
