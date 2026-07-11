from typing import Any
from langchain_chroma import Chroma

from app.config import VECTOR_DB_PATH
from app.vector.embeddings import embeddings

from app.vector.constants import COLLECTION_NAME


COLLECTION_NAME = COLLECTION_NAME


def get_vector_store() -> Chroma:
    if not VECTOR_DB_PATH.exists():
        raise RuntimeError(
            "Vector database does not exist. "
            "Run 'python -m app.vector.loader' first."
        )

    return Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )


def search_documents(
    query: str,
    k: int = 5,
) -> list[dict[str, Any]]:
    results = get_vector_store().similarity_search_with_score(
        query=query,
        k=k,
    )

    return [
        {
            "content": document.page_content,
            "metadata": document.metadata,
            "distance": distance,
        }
        for document, distance in results
    ]


def main() -> None:
    results = search_documents(
        "How do I troubleshoot VPN after a Windows update?",
        k=3,
    )

    for index, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print(f"\nResult {index}")
        print(f"Source: {metadata['source']}")
        print(f"Type: {metadata['document_type']}")
        print(f"Distance: {result['distance']:.4f}")
        print(result["content"][:500])


if __name__ == "__main__":
    main()
