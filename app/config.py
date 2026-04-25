from __future__ import annotations

import os
from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl


class Settings(BaseSettings):
    # Azure environment
    azure_openai_endpoint: HttpUrl = Field(..., env="AZURE_OPENAI_ENDPOINT")
    azure_openai_key: str = Field(..., env="AZURE_OPENAI_KEY")
    azure_openai_deployment: str = Field(..., env="AZURE_OPENAI_DEPLOYMENT")

    azure_form_recognizer_endpoint: HttpUrl = Field(..., env="AZURE_FORM_RECOGNIZER_ENDPOINT")
    azure_form_recognizer_key: str = Field(..., env="AZURE_FORM_RECOGNIZER_KEY")

    azure_search_endpoint: HttpUrl = Field(..., env="AZURE_SEARCH_ENDPOINT")
    azure_search_key: str = Field(..., env="AZURE_SEARCH_KEY")
    azure_search_index: str = Field(..., env="AZURE_SEARCH_INDEX")

    foundry_project_id: str = Field(..., env="AZURE_FOUNDRY_PROJECT_ID")
    foundry_endpoint: HttpUrl = Field(..., env="AZURE_FOUNDRY_ENDPOINT")
    foundry_api_key: str = Field(..., env="AZURE_FOUNDRY_API_KEY")

    fraud_api_url: HttpUrl = Field(..., env="FRAUD_API_URL")
    fraud_api_key: str = Field(..., env="FRAUD_API_KEY")

    mcp_host: str = Field(default="0.0.0.0", env="MCP_HOST")
    mcp_port: int = Field(default=8000, env="MCP_PORT")

    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    environment: str = Field(default="production", env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
