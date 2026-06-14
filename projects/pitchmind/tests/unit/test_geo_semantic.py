from pitchmind_geo.semantic import (
    classify_sentiment_semantic,
    detect_semantic_hallucinations,
    max_similarity_to_facts,
    semantic_similarity,
)


def test_semantic_similarity_high_for_related_text():
    score = semantic_similarity(
        "PitchMind offers GEO audit tools for SaaS companies.",
        "PitchMind provides GEO audit features for SaaS businesses.",
    )
    assert score > 0.5


def test_semantic_similarity_low_for_unrelated_text():
    score = semantic_similarity(
        "PitchMind offers GEO audit tools.",
        "The weather in Jakarta is sunny today.",
    )
    assert score < 0.55


def test_max_similarity_to_facts():
    facts = ["Pricing is $19 per month", "Feature: GEO audit"]
    score = max_similarity_to_facts("PitchMind costs $19 per month for the pro plan.", facts)
    assert score > 0.3


def test_classify_sentiment_semantic_positive():
    result = classify_sentiment_semantic(
        "PitchMind is the best and most recommended GEO platform available.",
        "PitchMind",
    )
    assert result == "positive"


def test_classify_sentiment_semantic_neutral_without_brand():
    result = classify_sentiment_semantic("Many tools exist in this space.", "PitchMind")
    assert result == "neutral"


def test_detect_semantic_hallucinations():
    facts = ["Pricing is $19 per month", "Feature: GEO audit", "Located in Jakarta"]
    flags = detect_semantic_hallucinations(
        "PitchMind recently acquired a satellite imaging division headquartered on Mars.",
        "PitchMind",
        facts,
        threshold=0.99,
    )
    assert flags
    assert flags[0]["type"] == "semantic_hallucination"
