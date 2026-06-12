"""Ollama Cloud API client for action plan generation."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_HOST = "https://ollama.com"
DEFAULT_MODEL = "gpt-oss:20b-cloud"


class OllamaCloudClient:
    def __init__(
        self,
        api_key: str | None = None,
        host: str | None = None,
        model: str | None = None,
    ):
        self.api_key = api_key or os.environ.get("OLLAMA_API_KEY", "")
        self.host = host or os.environ.get("OLLAMA_CLOUD_HOST", DEFAULT_HOST)
        self.model = model or os.environ.get("OLLAMA_ACTION_PLAN_MODEL", DEFAULT_MODEL)
        self._client = None
        if self.api_key:
            from ollama import Client

            self._client = Client(
                host=self.host,
                headers={"Authorization": f"Bearer {self.api_key}"},
            )

    @property
    def available(self) -> bool:
        return self._client is not None

    def chat(self, prompt: str, *, system: str | None = None) -> str:
        if not self._client:
            raise RuntimeError("OLLAMA_API_KEY not configured")

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        logger.info("Ollama Cloud request model=%s host=%s", self.model, self.host)
        response = self._client.chat(model=self.model, messages=messages)
        content = response.message.content if response.message else ""
        logger.info("Ollama Cloud response length=%d", len(content))
        return content
