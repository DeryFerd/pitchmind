import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "geo-engine"))

from pitchmind_geo.scorer import QueryResultData, compute_scorecard


def test_compute_scorecard_basic():
    results = [
        QueryResultData(brand_mentioned=True, competitors_mentioned={"CompX": False}, sentiment="positive"),
        QueryResultData(brand_mentioned=False, competitors_mentioned={"CompX": True}, sentiment="neutral"),
        QueryResultData(brand_mentioned=True, competitors_mentioned={"CompX": False}, sentiment="positive"),
        QueryResultData(brand_mentioned=False, competitors_mentioned={"CompX": False}, sentiment="neutral"),
    ]
    card = compute_scorecard(results, "PitchMind", ["CompX"])
    assert card["share_of_model"] == 50.0
    assert card["mentions_count"] == 2
    assert card["competitor_som"]["CompX"] == 25.0
    assert card["competitor_gap"]["_max_gap"] == 25.0


def test_compute_scorecard_empty():
    card = compute_scorecard([], "PitchMind", [])
    assert card["share_of_model"] == 0.0
    assert card["citation_accuracy"] is None
