
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
    initialize_local_data: bool = False

    # Database
    database_provider: str = "local"
    database_url: str | None = None

    # LLM
    llm_provider: str = "google"
    google_api_key: str | None = None
    gemini_model: str = "gemini-3.5-flash"
    gcp_project_id: str | None = None
    gcp_region: str = "europe-north1"
    vertex_llm_location: str = "eu"

    # Embeddings and vector store
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vertex_embedding_model: str = "text-embedding-005"
    embedding_provider: str = "local"
    vector_store_provider: str = "local"
    vector_collection_name: str = "helpdesk_documents"

    # LangGraph checkpoint storage
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
    azure_search_index: str = "helpdesk-documents"

    # Azure SQL
    azure_sql_connection_string: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
