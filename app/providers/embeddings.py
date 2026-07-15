from app.config import settings


def get_azure_embeddings():
    from langchain_openai import AzureOpenAIEmbeddings

    return AzureOpenAIEmbeddings(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        azure_deployment=settings.azure_openai_deployment,
        api_version=settings.azure_openai_api_version,
    )
