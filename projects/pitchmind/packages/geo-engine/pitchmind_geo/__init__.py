"""GEO engine: query runner, citation parser, scorer."""

from pitchmind_geo.hallucination import BrandFactsData, check_hallucinations
from pitchmind_geo.parser import MentionResult, classify_sentiment, extract_mentions
from pitchmind_geo.runner import GoldenQueryInput, ParsedQueryResult, run_visibility_batch
from pitchmind_geo.scorer import QueryResultData, compute_scorecard

__all__ = [
    "BrandFactsData",
    "GoldenQueryInput",
    "MentionResult",
    "ParsedQueryResult",
    "QueryResultData",
    "check_hallucinations",
    "classify_sentiment",
    "compute_scorecard",
    "extract_mentions",
    "run_visibility_batch",
]
