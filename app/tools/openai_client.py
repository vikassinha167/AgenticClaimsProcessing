from __future__ import annotations

import logging

from azure.ai.openai import OpenAIClient
from azure.identity import DefaultAzureCredential

from app.config import Settings


class AzureOpenAIClient:
    def __init__(self, settings: Settings) -> None:
        self.logger = logging.getLogger("AzureOpenAIClient")
        self.settings = settings
        self.client = OpenAIClient(
            endpoint=str(settings.azure_ai_services_endpoint),
            credential=DefaultAzureCredential(),
        )

    async def generate(self, prompt: str, max_tokens: int = 1200) -> str:
        response = self.client.chat.completions.create(
            engine=self.settings.azure_openai_deployment,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.0,
        )
        self.logger.debug("OpenAI response usage: %s", response.usage)
        return response.choices[0].message.content.strip()
