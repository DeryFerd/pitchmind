from pitchmind_geo.parser import classify_sentiment, extract_mentions


def test_extract_brand_mention_in_text():
    result = extract_mentions(
        "PitchMind is the best GEO tool available.",
        "PitchMind",
        "https://pitchmind.io",
        ["CompetitorX"],
    )
    assert result.brand_mentioned is True
    assert result.competitors_mentioned["CompetitorX"] is False


def test_extract_competitor_mention():
    result = extract_mentions(
        "CompetitorX leads the market, PitchMind is also good.",
        "PitchMind",
        "https://pitchmind.io",
        ["CompetitorX"],
    )
    assert result.brand_mentioned is True
    assert result.competitors_mentioned["CompetitorX"] is True


def test_extract_brand_via_citation_domain():
    result = extract_mentions(
        "See https://pitchmind.io for details.",
        "PitchMind",
        "https://pitchmind.io",
        [],
        citations=["https://pitchmind.io/blog"],
    )
    assert result.brand_mentioned is True


def test_sentiment_positive():
    assert (
        classify_sentiment(
            "PitchMind is the best and most recommended GEO platform available.",
            "PitchMind",
        )
        == "positive"
    )


def test_sentiment_neutral_without_brand():
    assert classify_sentiment("Many tools exist in this space.", "PitchMind") == "neutral"
