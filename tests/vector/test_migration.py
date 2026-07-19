from app.providers.vector_store import get_vector_store


def test_vector_store_provider_exists(
    monkeypatch,
):
    from app.config import settings

    monkeypatch.setattr(
        settings,
        "vector_store_provider",
        "local",
    )

    store = get_vector_store()

    assert store is not None
