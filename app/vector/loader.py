import shutil

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import DATASET_DIR, VECTOR_DB_PATH
from app.vector.embeddings import embeddings


DOCUMENTS_DIR = DATASET_DIR / "documents"
SUPPORTED_EXTENSIONS = {".md", ".txt"}


def load_documents() -> list[Document]:
    documents: list[Document] = []

    for path in DOCUMENTS_DIR.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
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


def reset_vector_database() -> None:
    if VECTOR_DB_PATH.exists():
        shutil.rmtree(VECTOR_DB_PATH)

    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)


def build_vector_database() -> None:
    raw_documents = load_documents()

    if not raw_documents:
        raise RuntimeError(f"No documents found in {DOCUMENTS_DIR}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(raw_documents)

    reset_vector_database()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_PATH),
        collection_name="helpdesk_documents",
    )

    print(f"Loaded documents: {len(raw_documents)}")
    print(f"Created chunks: {len(chunks)}")
    print(f"Vector database created at: {VECTOR_DB_PATH}")


def main() -> None:
    build_vector_database()


if __name__ == "__main__":
    main()
