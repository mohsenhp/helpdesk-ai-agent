from app.database.loader import load_csv_files
from app.database.models import Base
from app.database.providers.azure_sql import engine


def recreate_database() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def main() -> None:
    print("Recreating Azure SQL database schema...")

    recreate_database()

    print("Loading enterprise dataset...")

    load_csv_files(engine)

    print("Azure SQL database initialized.")


if __name__ == "__main__":
    main()
