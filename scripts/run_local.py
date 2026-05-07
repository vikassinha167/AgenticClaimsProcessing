from __future__ import annotations

import asyncio
import json
import logging
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.agents.orchestrator import ClaimsOrchestrator
from app.config import get_settings
from app.logger import configure_logging
from app.models import ClaimPayload

async def main() -> None:
    configure_logging()
    logger = logging.getLogger("run_local")
    settings = get_settings()

    sample_path = Path(__file__).resolve().parents[1] / "app" / "data" / "sample" / "claim_sample.json"
    logger.info("Loading sample claim from %s", sample_path)

    with sample_path.open("r", encoding="utf-8") as input_file:
        sample_claim = ClaimPayload.model_validate(json.load(input_file))

    orchestrator = ClaimsOrchestrator(settings)
    result = await orchestrator.process_claim(sample_claim)
    logger.info("Final decision: %s", result.decision)
    logger.info("Decision trace: %s", json.dumps(result.trace, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
