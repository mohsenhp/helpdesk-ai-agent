from app.providers import vector_store


def test_vector_store_provider_exists(
    monkeypatch,
):
    class FakeVectorStore:
        pass

    monkeypatch.setattr(
        vector_store,
        "get_azure_vector_store",
        lambda: FakeVectorStore(),
    )

    from app.config import settings

    monkeypatch.setattr(
        settings,
        "vector_store_provider",
        "azure",
    )

    store = vector_store.get_vector_store()

    assert store is not None
