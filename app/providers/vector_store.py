from app.config import VECTOR_DB_PATH
from app.vector.constants import COLLECTION_NAME
from app.vector.embeddings import get_embeddings


def get_local_vector_store():
    from langchain_chroma import Chroma

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


def get_azure_vector_store():
    raise NotImplementedError(
        "Azure AI Search vector store is not implemented yet."
    )
