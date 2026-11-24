from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import settings
from app.providers.embeddings import get_azure_embeddings


def get_local_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vertex_embeddings():
    if not settings.gcp_project_id:
        raise RuntimeError(
            "GCP_PROJECT_ID must be configured for Vertex AI embeddings."
        )

    from langchain_google_vertexai import VertexAIEmbeddings

    return VertexAIEmbeddings(
        model=settings.vertex_embedding_model,
        project=settings.gcp_project_id,
        location=settings.gcp_region,
    )


@lru_cache(maxsize=1)
def get_embeddings():
    if settings.embedding_provider == "azure":
        return get_azure_embeddings()

    if settings.embedding_provider == "local":
        return get_local_embeddings()

    if settings.embedding_provider == "vertex":
        return get_vertex_embeddings()

    raise ValueError(
        f"Unsupported embedding provider: {settings.embedding_provider}"
    )
