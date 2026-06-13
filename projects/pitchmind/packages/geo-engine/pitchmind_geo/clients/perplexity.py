"""Perplexity API client with retry and mock mode for dev without API key."""

from __future__ import annotations

import asyncio
import hashlib
import os
from dataclasses import dataclass

import httpx

from pitchmind_geo.cache import get_cached_response, set_cached_response

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
ESTIMATED_COST_PER_QUERY_USD = 0.02
DEFAULT_MODEL = "sonar"
DEFAULT_AUDIT_BUDGET_USD = 5.0


@dataclass
class PerplexityResponse:
    text: str
    citations: list[str]
    model: str


class PerplexityClient:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        mock: bool | None = None,
        mock_brand: str = "PitchMind",
        mock_competitors: list[str] | None = None,
        budget_usd: float = DEFAULT_AUDIT_BUDGET_USD,
    ):
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY", "")
        self.mock = mock if mock is not None else not self.api_key
        self.mock_brand = mock_brand
        self.mock_competitors = mock_competitors or ["CompetitorX"]
        self._client: httpx.AsyncClient | None = None if self.mock else httpx.AsyncClient(
            timeout=60.0, trust_env=False
        )
        self._harness = None
        if not self.mock:
            from pitchmind_harness import AgentHarness

            self._harness = AgentHarness(budget_usd)

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()

    async def query(self, text: str, *, retries: int = 3) -> PerplexityResponse:
        if self.mock:
            return self._mock_response(text)

        cached = get_cached_response(text)
        if cached:
            return PerplexityResponse(
                text=cached["text"],
                citations=cached.get("citations", []),
                model=cached.get("model", DEFAULT_MODEL),
            )

        async def _fetch() -> PerplexityResponse:
            return await self._call_api(text)

        if self._harness is not None:
            response = await self._harness.execute(
                _fetch,
                cost_estimate=ESTIMATED_COST_PER_QUERY_USD,
            )
        else:
            last_error: Exception | None = None
            for attempt in range(retries):
                try:
                    response = await self._call_api(text)
                    break
                except (httpx.HTTPError, httpx.TimeoutException) as exc:
                    last_error = exc
                    if attempt < retries - 1:
                        await asyncio.sleep(2**attempt)
            else:
                raise RuntimeError(f"Perplexity API failed after {retries} retries") from last_error

        set_cached_response(
            text,
            {
                "text": response.text,
                "citations": response.citations,
                "model": response.model,
            },
        )
        return response

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
        brand = self.mock_brand
        competitor = self.mock_competitors[0] if self.mock_competitors else "CompetitorX"
        digest = int(hashlib.md5(text.encode()).hexdigest(), 16)
        variant = digest % 4

        templates = [
            {
                "text": (
                    f"[mock] Based on current information, {brand} is a strong recommended option "
                    f"for GEO audits. {competitor} is also mentioned as an alternative."
                ),
                "citations": [f"https://{brand.lower().replace(' ', '')}.example.com"],
            },
            {
                "text": (
                    f"[mock] {competitor} leads the GEO audit market with the best visibility. "
                    f"Other tools exist but {competitor} dominates search recommendations."
                ),
                "citations": [f"https://{competitor.lower()}.example.com"],
            },
            {
                "text": (
                    f"[mock] {brand} offers blockchain-powered unlimited API calls and costs $999 "
                    f"per month — an enterprise-only platform that is overpriced and disappointing."
                ),
                "citations": [],
            },
            {
                "text": (
                    f"[mock] Several GEO tools are available. {brand} has mixed reviews — "
                    f"some users find it adequate while others prefer {competitor}."
                ),
                "citations": [
                    f"https://{brand.lower().replace(' ', '')}.example.com",
                    f"https://{competitor.lower()}.example.com",
                ],
            },
        ]

        chosen = templates[variant]
        return PerplexityResponse(
            text=chosen["text"],
            citations=chosen["citations"],
            model="mock-sonar",
        )
