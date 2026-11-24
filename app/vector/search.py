from app.config import settings
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

    vector_store = get_vector_store()

    search_kwargs = {
        "query": query,
        "k": k,
    }

    if metadata_filter is not None:
        if settings.vector_store_provider == "postgres":
            search_kwargs["filter"] = metadata_filter
        else:
            search_kwargs["filters"] = metadata_filter

    results = vector_store.similarity_search_with_score(**search_kwargs)

    return [
        {
            "content": document.page_content,
            "metadata": document.metadata,
            "distance": distance,
        }
        for document, distance in results
    ]
