from __future__ import annotations

import os

from pydantic import BaseSettings, Field, HttpUrl


class Settings(BaseSettings):
    # Azure environment
    azure_ai_services_endpoint: HttpUrl = Field(..., env="AZURE_AI_SERVICES_ENDPOINT")
    azure_openai_deployment: str = Field(..., env="AZURE_OPENAI_DEPLOYMENT")

    azure_search_endpoint: HttpUrl = Field(..., env="AZURE_SEARCH_ENDPOINT")
    azure_search_index: str = Field(..., env="AZURE_SEARCH_INDEX")

    foundry_project_id: str = Field(..., env="AZURE_FOUNDRY_PROJECT_ID")
    foundry_endpoint: HttpUrl = Field(..., env="AZURE_FOUNDRY_ENDPOINT")
    foundry_scope: str = Field(default="https://cognitiveservices.azure.com/.default", env="AZURE_FOUNDRY_SCOPE")

    fraud_api_url: HttpUrl = Field(..., env="FRAUD_API_URL")
    fraud_api_key: str | None = Field(None, env="FRAUD_API_KEY")

    mcp_host: str = Field(default="0.0.0.0", env="MCP_HOST")
    mcp_port: int = Field(default=8000, env="MCP_PORT")

    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    environment: str = Field(default="production", env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
