"""Shared PYTHONPATH bootstrap for tests (replaces per-file sys.path.insert)."""

from __future__ import annotations

import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_PATHS = (
    os.path.join(_ROOT, "packages", "db"),
    os.path.join(_ROOT, "packages", "geo-engine"),
    os.path.join(_ROOT, "packages", "site-auditor"),
    os.path.join(_ROOT, "packages", "harness"),
    _ROOT,
)
for _path in _PATHS:
    if _path not in sys.path:
        sys.path.insert(0, _path)

import numpy as np
import pytest

_POS_WORDS = {"best", "recommended", "excellent", "top", "leading", "great", "strong", "popular"}
_NEG_WORDS = {"worst", "avoid", "poor", "bad", "weak", "overpriced", "disappointing"}


def _fake_encode(texts: list[str]) -> np.ndarray:
    vectors = []
    for text in texts:
        vec = np.zeros(16)
        tokens = set(text.lower().split())
        vec[0] = float(len(tokens & _POS_WORDS))
        vec[1] = float(len(tokens & _NEG_WORDS))
        for token in text.lower().split():
            vec[2 + hash(token) % 14] += 1.0
        vectors.append(vec)
    return np.array(vectors)


@pytest.fixture(autouse=True)
def fake_semantic_encoder(monkeypatch):
    """Deterministic embeddings so unit tests run without downloading the model."""

    try:
        import pitchmind_geo.semantic as semantic

        monkeypatch.setattr(semantic, "encode", _fake_encode)
        semantic._get_model.cache_clear()
    except ImportError:
        pass
