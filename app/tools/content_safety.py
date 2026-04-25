from __future__ import annotations

import logging
from typing import Any

import requests

from app.config import Settings


class ContentSafetyClient:
    def __init__(self, settings: Settings) -> None:
        self.logger = logging.getLogger("ContentSafetyClient")
        self.settings = settings

    async def assess(self, trace: dict[str, Any]) -> bool:
        if not self.settings.azure_content_safety_endpoint or not self.settings.azure_content_safety_key:
            self.logger.warning("Azure Content Safety is not configured; defaulting safe=True")
            return True

        url = str(self.settings.azure_content_safety_endpoint).rstrip("/") + "/contentmoderation"
        headers = {
            "Ocp-Apim-Subscription-Key": self.settings.azure_content_safety_key,
            "Content-Type": "application/json",
        }
        payload = {"content": str(trace)}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            self.logger.warning("Content safety request failed: %s", response.text)
            return False
        data = response.json()
        return not data.get("is_content_unsafe", False)
