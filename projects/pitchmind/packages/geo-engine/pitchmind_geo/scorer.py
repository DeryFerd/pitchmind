"""Aggregate visibility scorecard from query results."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class QueryResultData:
    brand_mentioned: bool
    competitors_mentioned: dict[str, bool]
    hallucination_flags: list[dict] | None = None
    sentiment: str | None = None


def compute_scorecard(
    results: list[QueryResultData],
    brand_name: str,
    competitors: list[str],
) -> dict:
    total = len(results)
    if total == 0:
        return {
            "share_of_model": 0.0,
            "citation_accuracy": None,
            "competitor_gap": {},
            "total_queries": 0,
            "mentions_count": 0,
            "sentiment_breakdown": {"positive": 0, "neutral": 0, "negative": 0},
        }

    mentions = sum(1 for r in results if r.brand_mentioned)
    share_of_model = round((mentions / total) * 100, 1)

    competitor_som: dict[str, float] = {}
    for comp in competitors:
        comp_mentions = sum(1 for r in results if r.competitors_mentioned.get(comp, False))
        competitor_som[comp] = round((comp_mentions / total) * 100, 1)

    max_competitor_som = max(competitor_som.values()) if competitor_som else 0.0
    competitor_gap = {
        comp: round(share_of_model - som, 1) for comp, som in competitor_som.items()
    }
    competitor_gap["_max_gap"] = round(share_of_model - max_competitor_som, 1)

    hallucination_count = sum(len(r.hallucination_flags or []) for r in results if r.brand_mentioned)
    correct_mentions = mentions - min(hallucination_count, mentions)
    citation_accuracy = round((correct_mentions / mentions) * 100, 1) if mentions > 0 else None

    sentiment_breakdown = {"positive": 0, "neutral": 0, "negative": 0}
    for r in results:
        if r.brand_mentioned and r.sentiment:
            key = r.sentiment if r.sentiment in sentiment_breakdown else "neutral"
            sentiment_breakdown[key] += 1

    return {
        "share_of_model": share_of_model,
        "citation_accuracy": citation_accuracy,
        "competitor_gap": competitor_gap,
        "competitor_som": competitor_som,
        "total_queries": total,
        "mentions_count": mentions,
        "hallucination_count": hallucination_count,
        "sentiment_breakdown": sentiment_breakdown,
        "brand_name": brand_name,
    }
