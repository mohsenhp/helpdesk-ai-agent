from typing import Any

from app.vector.search import search_documents


def search_knowledge(
    query: str,
    k: int = 5,
    document_type: str | None = None,
) -> list[dict[str, Any]]:
    """
    Retrieve semantic knowledge documents.

    This abstraction allows migration from
    Chroma -> Azure AI Search later.
    """

    return search_documents(
        query=query,
        k=k,
        document_type=document_type,
    )
