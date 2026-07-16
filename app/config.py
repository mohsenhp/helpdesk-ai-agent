from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "enterprise_dataset"
)

RUNTIME_DIR = PROJECT_ROOT / "runtime"

DATABASE_PATH = RUNTIME_DIR / "helpdesk.db"
VECTOR_DB_PATH = RUNTIME_DIR / "chroma"


@dataclass(frozen=True)
class Settings:
    google_api_key: str
    gemini_model: str
    embedding_model: str

    environment: str
    debug: bool

    llm_provider: str

    database_provider: str
    azure_sql_connection_string: str | None

    vector_store_provider: str
    azure_search_endpoint: str | None
    azure_search_api_key: str | None
    azure_search_index: str | None

    checkpoint_database_url: str | None


def _optional_environment_variable(
    name: str,
) -> str | None:
    value = os.getenv(name)

    if value is None:
        return None

    stripped_value = value.strip()

    return stripped_value or None


def _environment_flag(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


settings = Settings(
    google_api_key=os.getenv(
        "GOOGLE_API_KEY",
        "",
    ),
    gemini_model=os.getenv(
        "GEMINI_MODEL",
        "",
    ),
    embedding_model=os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    ),
    environment=os.getenv(
        "ENVIRONMENT",
        "local",
    ),
    debug=_environment_flag(
        "DEBUG",
        False,
    ),
    llm_provider=os.getenv(
        "LLM_PROVIDER",
        "google",
    ),
    database_provider=os.getenv(
        "DATABASE_PROVIDER",
        "local",
    ),
    azure_sql_connection_string=_optional_environment_variable(
        "AZURE_SQL_CONNECTION_STRING",
    ),
    vector_store_provider=os.getenv(
        "VECTOR_STORE_PROVIDER",
        "local",
    ),
    azure_search_endpoint=_optional_environment_variable(
        "AZURE_SEARCH_ENDPOINT",
    ),
    azure_search_api_key=_optional_environment_variable(
        "AZURE_SEARCH_API_KEY",
    ),
    azure_search_index=_optional_environment_variable(
        "AZURE_SEARCH_INDEX",
    ),
    checkpoint_database_url=_optional_environment_variable(
        "CHECKPOINT_DATABASE_URL",
    ),
)
