"""Integration-style test: visibility batch → scorecard."""

from __future__ import annotations

import os
import sys
import uuid

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "geo-engine"))

from pitchmind_geo.clients.perplexity import PerplexityClient
from pitchmind_geo.hallucination import BrandFactsData
from pitchmind_geo.runner import GoldenQueryInput, run_visibility_batch
from pitchmind_geo.scorer import QueryResultData, compute_scorecard


@pytest.mark.asyncio
async def test_mock_audit_pipeline_end_to_end():
    queries = [
        GoldenQueryInput(id=uuid.uuid4(), text="Best GEO tools for SaaS?", lang="en"),
        GoldenQueryInput(id=uuid.uuid4(), text="Berapa harga PitchMind?", lang="id"),
    ]
    facts = BrandFactsData(pricing={"monthly": 19}, features=["GEO audit"], location="Jakarta")

    parsed = await run_visibility_batch(
        queries,
        brand_name="PitchMind",
        brand_website="https://pitchmind.example.com",
        competitors=["CompetitorX"],
        facts=facts,
        client=PerplexityClient(mock=True),
    )

    assert len(parsed) == 2
    scorecard_input = [
        QueryResultData(
            brand_mentioned=p.brand_mentioned,
            competitors_mentioned=p.competitors_mentioned,
            hallucination_flags=p.hallucination_flags,
            sentiment=p.sentiment,
        )
        for p in parsed
    ]
    card = compute_scorecard(scorecard_input, "PitchMind", ["CompetitorX"])
    assert "share_of_model" in card
    assert card["total_queries"] == 2
