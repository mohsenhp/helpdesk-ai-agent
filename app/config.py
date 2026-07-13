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
    checkpoint_database_url: str | None


def _optional_environment_variable(name: str) -> str | None:
    value = os.getenv(name)

    if value is None:
        return None

    stripped_value = value.strip()

    return stripped_value or None


settings = Settings(
    google_api_key=os.environ["GOOGLE_API_KEY"],
    gemini_model=os.environ["GEMINI_MODEL"],
    embedding_model=os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    ),
    checkpoint_database_url=_optional_environment_variable(
        "CHECKPOINT_DATABASE_URL"
    ),
)
