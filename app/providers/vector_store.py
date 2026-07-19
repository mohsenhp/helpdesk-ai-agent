from app.config import VECTOR_DB_PATH
from app.vector.constants import COLLECTION_NAME

from app.config import settings
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
    if not settings.azure_search_endpoint:
        raise RuntimeError(
            "Azure Search endpoint is not configured"
        )

    if not settings.azure_search_api_key:
        raise RuntimeError(
            "Azure Search API key is not configured"
        )

    from langchain_community.vectorstores.azuresearch import AzureSearch

    return AzureSearch(
        azure_search_endpoint=settings.azure_search_endpoint,
        azure_search_key=settings.azure_search_api_key,
        index_name=settings.azure_search_index,
        embedding_function=get_embeddings(),
    )

def get_vector_store():
    providers = {
        "local": get_local_vector_store,
        "azure": get_azure_vector_store,
    }

    try:
        return providers[
            settings.vector_store_provider
        ]()
    except KeyError:
        raise RuntimeError(
            f"Unsupported vector store provider: "
            f"{settings.vector_store_provider}"
        )
