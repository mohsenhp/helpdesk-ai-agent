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


@lru_cache(maxsize=1)
def get_llm():
    if settings.llm_provider == "azure":
        return get_azure_llm()

    if settings.llm_provider == "google":
        return get_google_llm()

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
