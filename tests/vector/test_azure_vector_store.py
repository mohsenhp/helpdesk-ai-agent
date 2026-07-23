import pytest

from app.config import settings
from app.providers.vector_store import get_azure_vector_store


pytestmark = pytest.mark.integration


@pytest.fixture
def azure_configured():
    if not settings.azure_search_endpoint:
        pytest.skip("Azure Search endpoint not configured")

    if not settings.azure_search_api_key:
        pytest.skip("Azure Search API key not configured")


def test_create_azure_vector_store(
    azure_configured,
):
    vector_store = get_azure_vector_store()

    assert vector_store is not None


def test_azure_vector_search(
    azure_configured,
):
    vector_store = get_azure_vector_store()

    results = vector_store.similarity_search(
        "VPN troubleshooting",
        k=2,
    )

    assert isinstance(results, list)


def test_azure_vector_metadata_filter(
    azure_configured,
):
    vector_store = get_azure_vector_store()

    results = vector_store.similarity_search(
        "VPN",
        k=5,
        filters="document_type eq 'runbooks'",
    )

    assert isinstance(results, list)
