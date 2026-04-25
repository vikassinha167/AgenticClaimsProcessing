from __future__ import annotations

import asyncio
import logging

from app.config import get_settings
from app.tools.foundry_sdk import FoundryClient
from app.logging import configure_logging


AGENT_REGISTRY = [
    {"name": "ExtractionAgent", "type": "extraction", "metadata": {"description": "Document Intelligence extraction agent."}},
    {"name": "CodingAgent", "type": "coding", "metadata": {"description": "ICD/CPT mapping and code reasoning agent."}},
    {"name": "ValidationAgent", "type": "validation", "metadata": {"description": "Policy and rules validation agent."}},
    {"name": "FraudDetectionAgent", "type": "fraud", "metadata": {"description": "Hybrid fraud detection agent using ML, RAG, and heuristics."}},
    {"name": "DecisionAgent", "type": "decision", "metadata": {"description": "Final claim decision agent."}},
    {"name": "CriticAgent", "type": "critic", "metadata": {"description": "Quality and safety review agent."}},
]


async def main() -> None:
    configure_logging()
    logger = logging.getLogger("deploy_foundry_agents")
    settings = get_settings()

    client = FoundryClient(settings)
    for agent in AGENT_REGISTRY:
        registration = await client.register_agent(agent["name"], agent["type"], agent["metadata"])
        logger.info("Registered agent %s: %s", agent["name"], registration.get("id"))


if __name__ == "__main__":
    asyncio.run(main())
