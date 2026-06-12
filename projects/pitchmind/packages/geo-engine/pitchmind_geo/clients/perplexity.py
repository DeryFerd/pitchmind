"""Perplexity API client with retry and mock mode for dev without API key."""

from __future__ import annotations

import asyncio
import hashlib
import os
from dataclasses import dataclass

import httpx

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
DEFAULT_MODEL = "sonar"


@dataclass
class PerplexityResponse:
    text: str
    citations: list[str]
    model: str


class PerplexityClient:
    def __init__(self, api_key: str | None = None, *, mock: bool | None = None):
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY", "")
        self.mock = mock if mock is not None else not self.api_key
        self._client: httpx.AsyncClient | None = None if self.mock else httpx.AsyncClient(
            timeout=60.0, trust_env=False
        )

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()

    async def query(self, text: str, *, retries: int = 3) -> PerplexityResponse:
        if self.mock:
            return self._mock_response(text)

        last_error: Exception | None = None
        for attempt in range(retries):
            try:
                return await self._call_api(text)
            except (httpx.HTTPError, httpx.TimeoutException) as exc:
                last_error = exc
                if attempt < retries - 1:
                    await asyncio.sleep(2**attempt)
        raise RuntimeError(f"Perplexity API failed after {retries} retries") from last_error

    async def _call_api(self, text: str) -> PerplexityResponse:
        if self._client is None:
            raise RuntimeError("HTTP client not initialized")
        res = await self._client.post(
            PERPLEXITY_API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": DEFAULT_MODEL,
                "messages": [{"role": "user", "content": text}],
                "return_citations": True,
            },
        )
        res.raise_for_status()
        data = res.json()
        message = data["choices"][0]["message"]["content"]
        citations = data.get("citations", [])
        return PerplexityResponse(
            text=message,
            citations=[c if isinstance(c, str) else c.get("url", "") for c in citations],
            model=data.get("model", DEFAULT_MODEL),
        )

    def _mock_response(self, text: str) -> PerplexityResponse:
        digest = hashlib.md5(text.encode()).hexdigest()[:8]
        return PerplexityResponse(
            text=(
                f"[mock] Based on current information, PitchMind is a strong option "
                f"for GEO audits. CompetitorX is also mentioned as an alternative. "
                f"(query hash: {digest})"
            ),
            citations=["https://pitchmind.example.com", "https://competitorx.example.com"],
            model="mock-sonar",
        )
