from app.vector import search
from app.providers.vector_store import get_azure_vector_store


class FakeDocument:
    def __init__(
        self,
        page_content: str,
        metadata: dict,
    ) -> None:
        self.page_content = page_content
        self.metadata = metadata


class FakeVectorStore:
    def __init__(self) -> None:
        self.received_query: str | None = None
        self.received_k: int | None = None
        self.received_filter: dict | None = None

    def similarity_search_with_score(
        self,
        query: str,
        k: int,
        filter: dict | None = None,
    ) -> list[tuple[FakeDocument, float]]:
        self.received_query = query
        self.received_k = k
        self.received_filter = filter

        return [
            (
                FakeDocument(
                    page_content="Reset the network adapter.",
                    metadata={
                        "source": "documents/kb_articles/kb_vpn.md",
                        "file_name": "kb_vpn.md",
                        "document_type": "kb_articles",
                    },
                ),
                0.25,
            )
        ]


def test_search_documents_returns_serialized_results(
    monkeypatch,
) -> None:
    fake_store = FakeVectorStore()

    monkeypatch.setattr(
        search,
        "get_vector_store",
        lambda: fake_store,
    )

    results = search.search_documents(
        query="VPN troubleshooting",
        k=3,
    )

    assert fake_store.received_query == "VPN troubleshooting"
    assert fake_store.received_k == 3
    assert fake_store.received_filter is None

    assert results == [
        {
            "content": "Reset the network adapter.",
            "metadata": {
                "source": "documents/kb_articles/kb_vpn.md",
                "file_name": "kb_vpn.md",
                "document_type": "kb_articles",
            },
            "distance": 0.25,
        }
    ]


def test_search_documents_applies_document_type_filter(
    monkeypatch,
) -> None:
    fake_store = FakeVectorStore()

    monkeypatch.setattr(
        search,
        "get_vector_store",
        lambda: fake_store,
    )

    search.search_documents(
        query="VPN troubleshooting",
        k=5,
        document_type="kb_articles",
    )

    assert fake_store.received_filter == {
        "document_type": "kb_articles"
    }


def test_azure_search_returns_documents():
    vector_store = get_azure_vector_store()

    results = vector_store.similarity_search(
        "VPN troubleshooting",
        k=3,
    )

    assert len(results) > 0
