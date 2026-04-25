from __future__ import annotations

import logging
from typing import Any

import requests
from azure.identity import DefaultAzureCredential

from app.config import Settings


class FoundryClient:
    def __init__(self, settings: Settings) -> None:
        self.logger = logging.getLogger("FoundryClient")
        self.settings = settings
        self.base_url = str(settings.foundry_endpoint).rstrip("/")
        self.project_id = settings.foundry_project_id
        self.credential = DefaultAzureCredential()
        self.scope = settings.foundry_scope

    @property
    def headers(self) -> dict[str, str]:
        token = self.credential.get_token(self.scope).token
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    async def register_agent(self, agent_name: str, agent_type: str, metadata: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/projects/{self.project_id}/agents"
        payload = {"name": agent_name, "type": agent_type, "metadata": metadata}
        self.logger.debug("Registering Foundry agent %s", agent_name)
        response = requests.post(url, json=payload, headers=self.headers, timeout=15)
        response.raise_for_status()
        return response.json()

    async def log_trace(self, claim_id: str, step: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/projects/{self.project_id}/traces"
        body = {"claim_id": claim_id, "step": step, "payload": payload}
        self.logger.debug("Logging Foundry trace: %s %s", claim_id, step)
        response = requests.post(url, json=body, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    async def store_evaluation(self, claim_id: str, metrics: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/projects/{self.project_id}/evaluations"
        body = {"claim_id": claim_id, "metrics": metrics}
        self.logger.debug("Storing Foundry evaluation for %s", claim_id)
        response = requests.post(url, json=body, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()
