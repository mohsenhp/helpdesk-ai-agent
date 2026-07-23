from app.config import settings


def load_local_vector_store() -> None:
    from app.vector.loader import build_local_vector_database

    build_local_vector_database()


def load_azure_vector_store() -> None:
    from app.vector.azure_loader import build_azure_vector_store

    build_azure_vector_store()


def load_vector_store() -> None:
    if settings.vector_store_provider == "local":
        load_local_vector_store()
        return

    if settings.vector_store_provider == "azure":
        load_azure_vector_store()
        return

    raise RuntimeError(
        f"Unsupported vector store provider: {settings.vector_store_provider}"
    )
