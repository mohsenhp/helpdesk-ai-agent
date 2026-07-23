from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import settings
from app.providers.embeddings import get_azure_embeddings


def get_local_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )


@lru_cache(maxsize=1)
def get_embeddings():
    if settings.embedding_provider == "azure":
        return get_azure_embeddings()

    if settings.embedding_provider == "local":
        return get_local_embeddings()

    raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")
