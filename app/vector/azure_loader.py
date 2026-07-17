from app.providers.vector_store import get_azure_vector_store
from app.vector.loader import load_documents
from app.vector.pipeline import split_documents


def build_azure_vector_store() -> None:
    raw_documents = load_documents()

    if not raw_documents:
        raise RuntimeError("No documents found.")

    chunks = split_documents(raw_documents)

    vector_store = get_azure_vector_store()

    vector_store.add_documents(chunks)

    print(f"Loaded documents: {len(raw_documents)}")
    print(f"Created chunks: {len(chunks)}")
    print("Documents uploaded to Azure AI Search.")
