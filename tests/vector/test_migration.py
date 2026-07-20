from app.providers.vector_store import get_vector_store


def test_vector_store_provider_exists(
    monkeypatch,
):
    from app.config import settings

    fake_store = object()

    monkeypatch.setattr(
        settings,
        "vector_store_provider",
        "azure",
    )

    monkeypatch.setattr(
        "app.providers.vector_store.get_azure_vector_store",
        lambda: fake_store,
    )

    store = get_vector_store()

    assert store is fake_store
