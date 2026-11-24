from sqlalchemy import text

from app.config import DATABASE_PATH, settings
from app.database.loader import load_csv_files
from app.database.models import Base


def get_engine():
    if settings.database_provider == "local":
        from app.database.providers.sqlite import engine
        return engine

    if settings.database_provider == "postgres":
        from app.database.providers.postgres import engine
        return engine

    raise ValueError(
        "Database initialization supports only "
        "'local' and 'postgres' providers."
    )


def create_database(engine) -> None:
    if settings.database_provider == "local":
        DATABASE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if DATABASE_PATH.exists():
            DATABASE_PATH.unlink()

    Base.metadata.create_all(engine)


def reset_postgres_sequences(engine) -> None:
    if settings.database_provider != "postgres":
        return

    table_names = [
        "users",
        "assets",
        "software_versions",
        "tickets",
        "incidents",
        "changes",
    ]

    with engine.begin() as connection:
        for table_name in table_names:
            connection.execute(
                text(
                    f"""
                    SELECT setval(
                        pg_get_serial_sequence(
                            :table_name,
                            'id'
                        ),
                        COALESCE(
                            (SELECT MAX(id) FROM "{table_name}"),
                            1
                        ),
                        EXISTS(
                            SELECT 1 FROM "{table_name}"
                        )
                    )
                    """
                ),
                {"table_name": table_name},
            )


def main() -> None:
    engine = get_engine()

    create_database(engine)
    load_csv_files(engine)
    reset_postgres_sequences(engine)

    if settings.database_provider == "local":
        print(f"\nSQLite database created at: {DATABASE_PATH}")
    else:
        print("\nPostgreSQL database initialized successfully.")


if __name__ == "__main__":
    main()
