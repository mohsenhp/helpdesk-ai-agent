from langchain_core.documents import Document

from app.config import settings
from app.vector.pipeline import split_documents


def load_documents() -> list[Document]:
    from app.config import DATASET_DIR

    documents_dir = DATASET_DIR / "documents"

    documents: list[Document] = []

    for path in documents_dir.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in {".md", ".txt"}:
            continue

        relative_path = path.relative_to(DATASET_DIR)

        documents.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={
                    "source": str(relative_path),
                    "file_name": path.name,
                    "document_type": path.parent.name,
                },
            )
        )

    return documents


def load_to_local_vector_store(
    documents: list[Document],
) -> None:
    import shutil

    from langchain_chroma import Chroma

    from app.config import VECTOR_DB_PATH
    from app.vector.constants import COLLECTION_NAME
    from app.vector.embeddings import get_embeddings

    chunks = split_documents(documents)

    if VECTOR_DB_PATH.exists():
        shutil.rmtree(VECTOR_DB_PATH)

    VECTOR_DB_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=str(VECTOR_DB_PATH),
        collection_name=COLLECTION_NAME,
    )

    print(f"Created local vector database: {VECTOR_DB_PATH}")
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")


def load_to_azure_vector_store(
    documents: list[Document],
) -> None:
    from app.providers.vector_store import (
        get_azure_vector_store,
    )

    chunks = split_documents(documents)

    vector_store = get_azure_vector_store()

    vector_store.add_documents(
        documents=chunks,
    )

    print("Uploaded documents to Azure AI Search")
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")


def build_vector_database() -> None:
    documents = load_documents()

    if not documents:
        raise RuntimeError("No documents found.")

    if settings.vector_store_provider == "local":
        load_to_local_vector_store(documents)

    elif settings.vector_store_provider == "azure":
        load_to_azure_vector_store(documents)

    else:
        raise RuntimeError(
            f"Unsupported vector store provider: {settings.vector_store_provider}"
        )


def main() -> None:
    print(f"Vector store provider: {settings.vector_store_provider}")

    build_vector_database()


if __name__ == "__main__":
    main()
