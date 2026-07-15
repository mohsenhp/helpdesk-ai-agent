from pathlib import Path

from app.config.settings import Settings, get_settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASE_PATH = BASE_DIR / "data" / "helpdesk.db"

VECTOR_DB_PATH = BASE_DIR / "data" / "chroma"

# Singleton settings instance
settings = get_settings()

__all__ = [
    "DATABASE_PATH",
    "VECTOR_DB_PATH",
    "Settings",
    "get_settings",
    "settings",
]
