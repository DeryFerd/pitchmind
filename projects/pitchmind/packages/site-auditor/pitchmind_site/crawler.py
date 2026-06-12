"""HTTP fetch utilities for site audit."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import httpx

USER_AGENT = "PitchMindBot/1.0 (+https://pitchmind.io/bot)"
TIMEOUT = 15.0


@dataclass
class FetchResult:
    url: str
    status_code: int | None
    text: str
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status_code is not None and 200 <= self.status_code < 400


def normalize_base_url(url: str) -> str:
    parsed = urlparse(url.strip())
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc or parsed.path.split("/")[0]
    return f"{scheme}://{netloc}"


def fetch_url(url: str, client: httpx.Client | None = None) -> FetchResult:
    owns_client = client is None
    http = client or httpx.Client(timeout=TIMEOUT, follow_redirects=True, trust_env=False)
    try:
        res = http.get(url, headers={"User-Agent": USER_AGENT})
        return FetchResult(url=url, status_code=res.status_code, text=res.text)
    except httpx.HTTPError as exc:
        return FetchResult(url=url, status_code=None, text="", error=str(exc))
    finally:
        if owns_client:
            http.close()


def fetch_site_pages(base_url: str, client: httpx.Client | None = None) -> dict[str, FetchResult]:
    base = normalize_base_url(base_url)
    owns_client = client is None
    http = client or httpx.Client(timeout=TIMEOUT, follow_redirects=True, trust_env=False)
    try:
        return {
            "homepage": fetch_url(base, http),
            "llms_txt": fetch_url(urljoin(base + "/", "llms.txt"), http),
            "robots_txt": fetch_url(urljoin(base + "/", "robots.txt"), http),
        }
    finally:
        if owns_client:
            http.close()
