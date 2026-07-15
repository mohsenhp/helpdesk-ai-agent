from app.config import settings


def get_session_factory():
    if settings.database_provider == "local":
        from app.database.providers.sqlite import SessionLocal
        return SessionLocal

    if settings.database_provider == "azure":
        from app.database.providers.azure_sql import SessionLocal
        return SessionLocal

    raise ValueError(
        f"Unsupported database provider: {settings.database_provider}"
    )


SessionLocal = get_session_factory()
