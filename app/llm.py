from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings
from app.providers.azure import get_azure_llm


def get_google_llm():
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        temperature=0,
    )


def get_vertex_llm():
    if not settings.gcp_project_id:
        raise RuntimeError(
            "GCP_PROJECT_ID must be configured for Vertex AI."
        )

    from langchain_google_vertexai import ChatVertexAI

    return ChatVertexAI(
        model=settings.gemini_model,
        project=settings.gcp_project_id,
        location=settings.vertex_llm_location,
        temperature=0,
    )


@lru_cache(maxsize=1)
def get_llm():
    if settings.llm_provider == "azure":
        return get_azure_llm()

    if settings.llm_provider == "google":
        return get_google_llm()

    if settings.llm_provider == "vertex":
        return get_vertex_llm()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )
