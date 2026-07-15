from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATASET_DIR = BASE_DIR / "data" / "raw" / "enterprise_dataset"

DATABASE_PATH = BASE_DIR / "data" / "helpdesk.db"

VECTOR_DB_PATH = BASE_DIR / "data" / "chroma"

from app.config.settings import (
    Settings,
    get_settings,
    settings,
)

__all__ = [
    "DATASET_DIR",
    "DATABASE_PATH",
    "VECTOR_DB_PATH",
    "Settings",
    "get_settings",
    "settings",
]
