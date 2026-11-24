from app.config import VECTOR_DB_PATH
from app.vector.constants import COLLECTION_NAME

from app.config import settings
from app.vector.embeddings import get_embeddings


def get_local_vector_store():
    from langchain_chroma import Chroma

    if not VECTOR_DB_PATH.exists():
        raise RuntimeError(
            "Vector database does not exist. Run 'python -m app.vector.loader' first."
        )

    return Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=get_embeddings(),
        collection_name=COLLECTION_NAME,
    )


def get_postgres_vector_store():
    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL must be configured for PostgreSQL vector storage."
        )

    from langchain_postgres import PGVector

    return PGVector(
        embeddings=get_embeddings(),
        collection_name=COLLECTION_NAME,
        connection=settings.database_url,
        embedding_length=768,
        use_jsonb=True,
    )


def get_azure_vector_store():
    if not settings.azure_search_endpoint:
        raise RuntimeError("Azure Search endpoint is not configured")

    if not settings.azure_search_api_key:
        raise RuntimeError("Azure Search API key is not configured")

    from langchain_community.vectorstores.azuresearch import AzureSearch

    class HelpdeskAzureSearch(AzureSearch):
        def add_embeddings(
            self,
            text_embeddings,
            metadatas=None,
            **kwargs,
        ):
            import uuid

            documents = []

            for index, (text, embedding) in enumerate(text_embeddings):
                metadata = metadatas[index] if metadatas else {}

                documents.append(
                    {
                        "id": str(uuid.uuid4()),
                        "content": text,
                        "source": metadata.get("source", ""),
                        "file_name": metadata.get("file_name", ""),
                        "document_type": metadata.get("document_type", ""),
                        "content_vector": embedding,
                    }
                )

            result = self.client.upload_documents(documents=documents)

            return [item.key for item in result if item.succeeded]

        def add_documents(
            self,
            documents,
            **kwargs,
        ):
            texts = [document.page_content for document in documents]

            metadatas = [document.metadata for document in documents]

            embeddings = self.embedding_function.embed_documents(texts)

            return self.add_embeddings(
                zip(texts, embeddings),
                metadatas,
            )

        def similarity_search(
            self,
            query,
            k=4,
            **kwargs,
        ):
            metadata_filter = kwargs.pop(
                "filter",
                None,
            )

            if metadata_filter is not None:
                kwargs["filters"] = metadata_filter

            return super().similarity_search(
                query,
                k=k,
                **kwargs,
            )

    return HelpdeskAzureSearch(
        azure_search_endpoint=settings.azure_search_endpoint,
        azure_search_key=settings.azure_search_api_key,
        index_name=settings.azure_search_index,
        embedding_function=get_embeddings(),
    )


def get_vector_store():
    providers = {
        "local": get_local_vector_store,
        "azure": get_azure_vector_store,
        "postgres": get_postgres_vector_store,
    }

    try:
        return providers[settings.vector_store_provider]()
    except KeyError:
        raise RuntimeError(
            f"Unsupported vector store provider: {settings.vector_store_provider}"
        )
