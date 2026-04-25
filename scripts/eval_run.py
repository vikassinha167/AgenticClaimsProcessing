from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

from app.config import get_settings
from app.evaluations.evaluator import EvaluationPipeline
from app.logging import configure_logging


async def main() -> None:
    configure_logging()
    logger = logging.getLogger("eval_run")
    settings = get_settings()

    sample_path = Path(__file__).resolve().parents[1] / "app" / "data" / "sample" / "claim_sample.json"
    with sample_path.open("r", encoding="utf-8") as file:
        claim = json.load(file)

    evaluator = EvaluationPipeline(settings)
    evaluation = await evaluator.evaluate(claim_id=claim["claim_id"], trace={"sample": claim})
    logger.info("Evaluation results: %s", evaluation.json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
