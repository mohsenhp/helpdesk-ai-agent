from typing import Any

from langchain_chroma import Chroma

from app.config import VECTOR_DB_PATH
from app.vector.constants import COLLECTION_NAME
from app.vector.embeddings import get_embeddings


def get_vector_store() -> Chroma:
    if not VECTOR_DB_PATH.exists():
        raise RuntimeError(
            "Vector database does not exist. "
            "Run 'python -m app.vector.loader' first."
        )

    return Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=get_embeddings(),
        collection_name=COLLECTION_NAME,
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
