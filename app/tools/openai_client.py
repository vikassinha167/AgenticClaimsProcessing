from __future__ import annotations

import logging

import requests

from app.config import Settings


class FoundryOpenAIClient:
    def __init__(self, settings: Settings) -> None:
        self.logger = logging.getLogger("FoundryOpenAIClient")
        self.settings = settings

    async def generate(self, prompt: str, max_tokens: int = 1200) -> str:
        return self._invoke_foundry_model(prompt, max_tokens)

    def _invoke_foundry_model(self, prompt: str, max_tokens: int = 1200) -> str:
        url = (
            f"{self.settings.foundry_endpoint.rstrip('/')}"
            f"/projects/{self.settings.foundry_project_id}/models/{self.settings.azure_openai_deployment}/invoke"
        )
        headers = {
            "Authorization": f"Bearer {self.settings.foundry_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "input": prompt,
            "parameters": {
                "max_tokens": max_tokens,
                "temperature": 0.0,
            },
        }
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        self.logger.debug("Foundry model response: %s", data)

        if isinstance(data, dict):
            if "output" in data:
                return str(data["output"]).strip()
            if "outputs" in data and isinstance(data["outputs"], list) and data["outputs"]:
                first = data["outputs"][0]
                if isinstance(first, dict):
                    return str(first.get("content") or first.get("text") or "").strip()
                return str(first).strip()
            if "choices" in data and isinstance(data["choices"], list):
                choice = data["choices"][0]
                return str(choice.get("message", {}).get("content", "")).strip()
        return str(data).strip()
