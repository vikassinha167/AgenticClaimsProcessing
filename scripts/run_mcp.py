from __future__ import annotations

import logging

import uvicorn
from app.config import get_settings
from app.logging import configure_logging


def main() -> None:
    configure_logging()
    logger = logging.getLogger("run_mcp")
    settings = get_settings()
    logger.info("Starting MCP server on %s:%s", settings.mcp_host, settings.mcp_port)
    uvicorn.run("app.mcp.server:app", host=settings.mcp_host, port=settings.mcp_port, log_level=settings.log_level.lower())


if __name__ == "__main__":
    main()
