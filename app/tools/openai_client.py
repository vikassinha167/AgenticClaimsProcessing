from __future__ import annotations

import logging
from typing import Any

from azure.ai.openai import OpenAIClient as AzureOpenAIService
from azure.core.credentials import AzureKeyCredential

from app.config import Settings


class AzureOpenAIClient:
    def __init__(self, settings: Settings) -> None:
        self.logger = logging.getLogger("AzureOpenAIClient")
        self.settings = settings
        self.client = AzureOpenAIService(
            endpoint=str(settings.azure_openai_endpoint),
            credential=AzureKeyCredential(settings.azure_openai_key),
        )

    async def generate(self, prompt: str, max_tokens: int = 1200) -> str:
        response = self.client.chat.completions.create(
            engine=self.settings.azure_openai_deployment,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.0,
        )
        self.logger.debug("OpenAI response status: %s", response.usage)
        return response.choices[0].message.content.strip()
