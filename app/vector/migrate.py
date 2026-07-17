from app.vector.loader import load_documents
from app.providers.vector_store import get_azure_vector_store


def migrate_documents_to_azure_search() -> None:
    documents = load_documents()

    if not documents:
        raise RuntimeError("No documents found to migrate")

    vector_store = get_azure_vector_store()

    vector_store.add_documents(documents)

    print(
        f"Migrated {len(documents)} documents to Azure AI Search"
    )


def main() -> None:
    migrate_documents_to_azure_search()


if __name__ == "__main__":
    main()
