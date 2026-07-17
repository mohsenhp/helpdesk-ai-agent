from app.providers.vector_store import get_azure_vector_store


def test_azure_search_contains_documents():
    vector_store = get_azure_vector_store()

    results = vector_store.similarity_search(
        "VPN troubleshooting",
        k=3,
    )

    assert len(results) > 0

    for document in results:
        assert document.page_content
        assert "source" in document.metadata
