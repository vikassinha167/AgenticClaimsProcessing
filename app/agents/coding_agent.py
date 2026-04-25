from __future__ import annotations

import logging
from typing import List

from app.config import Settings
from app.models import ClaimItem, ClaimPayload, CodingResult
from app.tools.foundry_sdk import FoundryClient
from app.tools.openai_client import FoundryOpenAIClient


class CodingAgent:
    SYSTEM_PROMPT = (
        "You are the Coding Agent. Map healthcare service descriptions to ICD and CPT codes using best practices. "
        "Return structured mappings, the code type, and a concise reasoning summary. "
        "Reference known code mapping patterns and support audit traceability."
    )

    def __init__(self, settings: Settings) -> None:
        self.logger = logging.getLogger("CodingAgent")
        self.settings = settings
        self.openai = FoundryOpenAIClient(settings)
        self.foundry = FoundryClient(settings)

    async def map_codes(self, extraction_result: "app.models.ExtractionResult") -> CodingResult:
        claim = extraction_result.claim
        prompt = self._build_prompt(claim)
        self.logger.debug("Sending coding prompt for claim %s", claim.claim_id)
        response = await self.openai.generate(prompt)
        mapped_services = self._parse_response(response)
        await self.foundry.log_trace(claim.claim_id, "coding_prompt", {"prompt": prompt, "response": response})
        return CodingResult(claim_id=claim.claim_id, mapped_items=mapped_services, reasoning=response, confidence=0.88)

    def _build_prompt(self, claim: ClaimPayload) -> str:
        service_lines = []
        for item in claim.services:
            service_lines.append(f"- {item.description} | {item.provider} | {item.date_of_service or 'unknown'} | {item.amount}")

        return (
            f"{self.SYSTEM_PROMPT}\n"
            f"Claim ID: {claim.claim_id}\n"
            f"Provider: {claim.provider_id}\n"
            f"Services:\n{chr(10).join(service_lines)}\n"
            "Map each line to ICD or CPT as appropriate. Provide output as a JSON list of mapped services."
        )

    def _parse_response(self, response: str) -> List[ClaimItem]:
        import json

        try:
            payload = json.loads(response)
            services = [ClaimItem.parse_obj(item) for item in payload if isinstance(item, dict)]
            return services
        except Exception:
            self.logger.warning("Failed to parse coding response, falling back to original content")
            return []
