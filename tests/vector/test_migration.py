from app.providers.vector_store import get_vector_store


def test_vector_store_provider_exists():
    store = get_vector_store()

    assert store is not None
