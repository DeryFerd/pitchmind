"""Semantic similarity using sentence-transformers (CPU inference)."""

from __future__ import annotations

import functools
import re

import numpy as np

_MODEL_NAME = "all-MiniLM-L6-v2"
_POSITIVE_ANCHORS = [
    "This is the best and most recommended product in its category.",
    "A top leading excellent choice that users strongly prefer.",
    "Highly rated and popular with great reviews.",
]
_NEGATIVE_ANCHORS = [
    "This product is overpriced, disappointing, and should be avoided.",
    "A poor weak choice with bad reviews that users regret.",
    "The worst option in this category with many complaints.",
]
_DEFAULT_HALLUCINATION_THRESHOLD = 0.35


@functools.lru_cache(maxsize=1)
def _get_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(_MODEL_NAME)


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def encode(texts: list[str]) -> np.ndarray:
    model = _get_model()
    return model.encode(texts, convert_to_numpy=True)


def semantic_similarity(text_a: str, text_b: str) -> float:
    embs = encode([text_a, text_b])
    return _cosine_sim(embs[0], embs[1])


def max_similarity_to_facts(text: str, facts: list[str]) -> float:
    if not facts:
        return 1.0
    embs = encode([text] + facts)
    text_emb = embs[0]
    return max(_cosine_sim(text_emb, fact_emb) for fact_emb in embs[1:])


def _brand_sentences(response: str, brand_name: str) -> list[str]:
    norm_brand = re.sub(r"[^a-z0-9]", "", brand_name.lower())
    sentences = re.split(r"[.!?]\s+", response)
    matched = []
    for sentence in sentences:
        norm_sentence = re.sub(r"[^a-z0-9]", "", sentence.lower())
        if norm_brand and norm_brand in norm_sentence:
            matched.append(sentence.strip())
    return matched


def classify_sentiment_semantic(response: str, brand_name: str) -> str | None:
    """Embedding-based sentiment for brand-context sentences."""
    brand_sentences = _brand_sentences(response, brand_name)
    if not brand_sentences:
        return "neutral"

    text = " ".join(brand_sentences)
    anchors = _POSITIVE_ANCHORS + _NEGATIVE_ANCHORS
    embs = encode([text] + anchors)
    text_emb = embs[0]
    pos_sims = [_cosine_sim(text_emb, emb) for emb in embs[1 : 1 + len(_POSITIVE_ANCHORS)]]
    neg_sims = [_cosine_sim(text_emb, emb) for emb in embs[1 + len(_POSITIVE_ANCHORS) :]]

    pos_score = max(pos_sims) if pos_sims else 0.0
    neg_score = max(neg_sims) if neg_sims else 0.0

    if abs(pos_score - neg_score) < 0.05:
        return "neutral"
    return "positive" if pos_score > neg_score else "negative"


def detect_semantic_hallucinations(
    response: str,
    brand_name: str,
    facts: list[str],
    *,
    threshold: float = _DEFAULT_HALLUCINATION_THRESHOLD,
) -> list[dict]:
    """Flag brand-context sentences with low semantic alignment to known facts."""
    if not facts:
        return []

    flags: list[dict] = []
    for sentence in _brand_sentences(response, brand_name):
        if len(sentence.split()) < 4:
            continue
        similarity = max_similarity_to_facts(sentence, facts)
        if similarity < threshold:
            flags.append({
                "type": "semantic_hallucination",
                "stated": sentence[:200],
                "similarity": round(similarity, 3),
                "threshold": threshold,
                "severity": "high" if similarity < threshold * 0.5 else "medium",
            })
    return flags
