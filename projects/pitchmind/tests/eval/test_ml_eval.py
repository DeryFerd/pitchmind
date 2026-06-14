"""ML eval gate — precision/recall/F1 on labeled hallucination + sentiment dataset."""

from __future__ import annotations

import json
from pathlib import Path

from pitchmind_geo.hallucination import BrandFactsData, check_hallucinations
from pitchmind_geo.parser import classify_sentiment

DATASET = Path(__file__).parent / "fixtures" / "ml_eval_dataset.json"
MIN_SENTIMENT_ACCURACY = 0.35
MIN_HALLUCINATION_RECALL = 0.45
MIN_HALLUCINATION_PRECISION = 0.45
MIN_HALLUCINATION_F1 = 0.45


def _load_cases() -> list[dict]:
    return json.loads(DATASET.read_text(encoding="utf-8"))


def _facts_from_strings(strings: list[str]) -> BrandFactsData:
    pricing = None
    features: list[str] = []
    location = None
    founded_year = None
    for item in strings:
        if item.startswith("Pricing is $"):
            monthly = item.replace("Pricing is $", "").replace(" per month", "")
            pricing = {"monthly": float(monthly)}
        elif item.startswith("Feature: "):
            features.append(item.replace("Feature: ", ""))
        elif item.startswith("Located in "):
            location = item.replace("Located in ", "")
        elif item.startswith("Founded in "):
            founded_year = int(item.replace("Founded in ", ""))
    return BrandFactsData(
        pricing=pricing,
        features=features or None,
        location=location,
        founded_year=founded_year,
    )


def _hallucination_predicted(flags: list[dict]) -> bool:
    return any(
        f["type"] in ("semantic_hallucination", "pricing_mismatch", "feature_hallucination")
        for f in flags
    )


def test_ml_eval_dataset_metrics():
    cases = _load_cases()
    assert len(cases) >= 25

    sentiment_correct = 0
    tp = fp = fn = 0

    for case in cases:
        brand = case["brand_name"]
        facts = _facts_from_strings(case["facts"])
        predicted_sentiment = classify_sentiment(case["response"], brand)
        if predicted_sentiment == case["expect_sentiment"]:
            sentiment_correct += 1

        flags = check_hallucinations(case["response"], brand, facts)
        predicted_hallucination = _hallucination_predicted(flags)
        expected = case["expect_hallucination"]

        if predicted_hallucination and expected:
            tp += 1
        elif predicted_hallucination and not expected:
            fp += 1
        elif not predicted_hallucination and expected:
            fn += 1

    sentiment_accuracy = sentiment_correct / len(cases)
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    assert sentiment_accuracy >= MIN_SENTIMENT_ACCURACY, sentiment_accuracy
    assert recall >= MIN_HALLUCINATION_RECALL, recall
    assert precision >= MIN_HALLUCINATION_PRECISION, precision
    assert f1 >= MIN_HALLUCINATION_F1, f1
