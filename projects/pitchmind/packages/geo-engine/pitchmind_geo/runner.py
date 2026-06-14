"""Batch visibility audit runner."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from uuid import UUID

from pitchmind_geo.clients.perplexity import PerplexityClient
from pitchmind_geo.hallucination import BrandFactsData, check_hallucinations
from pitchmind_geo.parser import classify_sentiment, extract_mentions

OnQueryComplete = Callable[[int], None]


@dataclass
class GoldenQueryInput:
    id: UUID
    text: str
    lang: str


@dataclass
class ParsedQueryResult:
    query_id: UUID
    engine: str
    response: str
    brand_mentioned: bool
    competitors_mentioned: dict[str, bool]
    citations: list[str]
    sentiment: str
    hallucination_flags: list[dict]


async def run_visibility_batch(
    queries: list[GoldenQueryInput],
    *,
    brand_name: str,
    brand_website: str,
    competitors: list[str],
    facts: BrandFactsData | None = None,
    client: PerplexityClient | None = None,
    concurrency: int = 3,
    on_query_complete: OnQueryComplete | None = None,
) -> list[ParsedQueryResult]:
    perplexity = client or PerplexityClient(
        mock_brand=brand_name,
        mock_competitors=competitors,
    )
    semaphore = asyncio.Semaphore(concurrency)
    results: list[ParsedQueryResult] = []
    completed_count = 0
    count_lock = asyncio.Lock()

    async def _notify_progress() -> None:
        nonlocal completed_count
        async with count_lock:
            completed_count += 1
            current = completed_count
        if on_query_complete:
            on_query_complete(current)

    async def _run_one(query: GoldenQueryInput) -> ParsedQueryResult | None:
        async with semaphore:
            try:
                api_res = await perplexity.query(query.text)
                mentions = extract_mentions(
                    api_res.text,
                    brand_name,
                    brand_website,
                    competitors,
                    api_res.citations,
                )
                flags = check_hallucinations(api_res.text, brand_name, facts)
                sentiment = classify_sentiment(api_res.text, brand_name)
                await _notify_progress()
                return ParsedQueryResult(
                    query_id=query.id,
                    engine="perplexity",
                    response=api_res.text,
                    brand_mentioned=mentions.brand_mentioned,
                    competitors_mentioned=mentions.competitors_mentioned,
                    citations=mentions.citations,
                    sentiment=sentiment,
                    hallucination_flags=flags,
                )
            except Exception:
                return None

    tasks = [_run_one(q) for q in queries]
    completed = await asyncio.gather(*tasks)

    for item in completed:
        if item is not None:
            results.append(item)

    if client is None and perplexity.mock is False:
        await perplexity.close()

    return results
