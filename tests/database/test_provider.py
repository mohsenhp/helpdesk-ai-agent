import pytest

from app.config import settings
from app.database.connection import get_session_factory


def test_local_database_provider_returns_sqlite_session(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        settings,
        "database_provider",
        "local",
    )

    session_factory = get_session_factory()

    assert session_factory is not None


def test_unsupported_database_provider_raises_error(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        settings,
        "database_provider",
        "invalid",
    )

    with pytest.raises(ValueError):
        get_session_factory()
