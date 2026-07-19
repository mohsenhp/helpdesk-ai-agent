from typing import Any

from app.providers.vector_store import get_vector_store


def search_documents(
    query: str,
    k: int = 5,
    document_type: str | None = None,
) -> list[dict[str, Any]]:

    metadata_filter = None

    if document_type is not None:
        metadata_filter = {
            "document_type": document_type,
        }

    results = get_vector_store().similarity_search_with_score(
        query=query,
        k=k,
        filter=metadata_filter,
    )

    return [
        {
            "content": document.page_content,
            "metadata": document.metadata,
            "distance": distance,
        }
        for document, distance in results
    ]
