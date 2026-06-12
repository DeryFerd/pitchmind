import os
import sys
import uuid

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "geo-engine"))

from pitchmind_geo.clients.perplexity import PerplexityClient
from pitchmind_geo.runner import GoldenQueryInput, run_visibility_batch


@pytest.mark.asyncio
async def test_run_visibility_batch_mock():
    client = PerplexityClient(mock=True)
    queries = [
        GoldenQueryInput(id=uuid.uuid4(), text="Best GEO tools?", lang="en"),
        GoldenQueryInput(id=uuid.uuid4(), text="Alat GEO terbaik?", lang="id"),
    ]
    results = await run_visibility_batch(
        queries,
        brand_name="PitchMind",
        brand_website="https://pitchmind.io",
        competitors=["CompetitorX"],
        client=client,
    )
    assert len(results) == 2
    assert all(r.engine == "perplexity" for r in results)
    assert all(r.brand_mentioned for r in results)
