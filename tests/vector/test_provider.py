from app.providers.vector_store import get_vector_store


def test_local_vector_store_provider(monkeypatch):
    monkeypatch.setenv(
        "VECTOR_STORE_PROVIDER",
        "local",
    )

    assert get_vector_store is not None
