from langchain_chroma import Chroma

from app.config import VECTOR_DB_PATH
from app.vector.embeddings import embeddings


def get_vector_store() -> Chroma:
    return Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embeddings,
        collection_name="helpdesk_documents",
    )


def search_documents(query: str, k: int = 5) -> list[dict]:
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    return [
        {
            "content": document.page_content,
            "metadata": document.metadata,
            "score": score,
        }
        for document, score in results
    ]


def main() -> None:
    results = search_documents(
        "How do I troubleshoot VPN after Windows update?",
        k=3,
    )

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print(f"Source: {result['metadata']['source']}")
        print(f"Type: {result['metadata']['document_type']}")
        print(f"Distance: {result['score']:.4f}")
        print(result["content"][:500])


if __name__ == "__main__":
    main()