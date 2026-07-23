from pathlib import Path

from app.config.settings import (
    Settings,
    get_settings,
    settings,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATASET_DIR = BASE_DIR / "data" / "raw" / "enterprise_dataset"

RUNTIME_DIR = BASE_DIR / "runtime"

DATABASE_PATH = RUNTIME_DIR / "helpdesk.db"

VECTOR_DB_PATH = RUNTIME_DIR / "chroma"

__all__ = [
    "DATASET_DIR",
    "RUNTIME_DIR",
    "DATABASE_PATH",
    "VECTOR_DB_PATH",
    "Settings",
    "get_settings",
    "settings",
]
