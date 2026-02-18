"""Application configuration from environment variables."""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """All configuration is loaded from environment variables or .env file."""

    # App
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000"]

    # Azure AI Foundry
    azure_ai_foundry_project_connection_string: Optional[str] = None
    azure_subscription_id: Optional[str] = None
    azure_resource_group: Optional[str] = None
    azure_ai_hub_name: Optional[str] = None

    # Azure OpenAI
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_deployment: str = "gpt-4o"
    azure_openai_api_version: str = "2025-01-01-preview"

    # Cosmos DB
    cosmos_db_endpoint: Optional[str] = None
    cosmos_db_key: Optional[str] = None
    cosmos_db_database: str = "agents-platform"
    cosmos_db_container: str = "agent-memory"

    # Content Safety
    azure_content_safety_endpoint: Optional[str] = None
    azure_content_safety_key: Optional[str] = None

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
