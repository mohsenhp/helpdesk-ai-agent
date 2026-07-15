from typing import Any

from app.config import settings
from app.providers.vector_store import (
    get_local_vector_store,
    get_azure_vector_store,
)


def get_vector_store():
    if settings.vector_store_provider == "local":
        return get_local_vector_store()

    if settings.vector_store_provider == "azure":
        return get_azure_vector_store()

    raise ValueError(
        f"Unsupported vector store provider: "
        f"{settings.vector_store_provider}"
    )


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
