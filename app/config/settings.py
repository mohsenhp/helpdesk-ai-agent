from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # Application
    app_name: str = "Helpdesk AI Agent"
    environment: str = "local"
    debug: bool = False
    initialize_local_data: bool = True
    database_provider: str = "local"

    # Current LLM provider
    llm_provider: str = "google"

    # Existing local LLM settings
    google_api_key: str | None = None
    gemini_model: str = "gemini-3.5-flash"

    # Existing local embedding settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Embedding provider
    embedding_provider: str = "local"
    vector_store_provider: str = "local"

    # Existing LangGraph/database settings
    checkpoint_database_url: str | None = None
    langgraph_strict_msgpack: bool = True

    # Azure OpenAI
    azure_openai_endpoint: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_deployment: str | None = None
    azure_openai_api_version: str | None = None

    # Azure AI Search
    azure_search_endpoint: str | None = None
    azure_search_api_key: str | None = None
    azure_search_index: str | None = None

    # Azure SQL
    azure_sql_connection_string: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Backward compatibility
settings = get_settings()
