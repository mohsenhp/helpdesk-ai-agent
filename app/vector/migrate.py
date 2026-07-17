from app.vector.loader import load_documents
from app.vector.pipeline import split_documents
from app.providers.vector_store import get_azure_vector_store


def migrate_documents_to_azure_search() -> None:
    raw_documents = load_documents()

    if not raw_documents:
        raise RuntimeError("No documents found to migrate")

    chunks = split_documents(raw_documents)

    if not chunks:
        raise RuntimeError("No document chunks created")

    vector_store = get_azure_vector_store()

    vector_store.add_documents(chunks)

    print(
        f"Migrated documents: {len(raw_documents)}"
    )
    print(
        f"Migrated chunks: {len(chunks)}"
    )


def main() -> None:
    migrate_documents_to_azure_search()


if __name__ == "__main__":
    main()
