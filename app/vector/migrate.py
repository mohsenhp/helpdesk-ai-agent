from app.vector.loader import load_documents
from app.vector.pipeline import split_documents
from app.providers.vector_store import get_azure_vector_store


def migrate_to_azure() -> None:
    documents = load_documents()

    if not documents:
        raise RuntimeError("No documents found")

    chunks = split_documents(documents)

    vector_store = get_azure_vector_store()

    vector_store.add_documents(chunks)

    print(f"Migrated documents: {len(documents)}")
    print(f"Migrated chunks: {len(chunks)}")


def main() -> None:
    migrate_to_azure()


if __name__ == "__main__":
    main()
