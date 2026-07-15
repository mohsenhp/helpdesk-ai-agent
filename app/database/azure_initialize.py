from app.database.loader import load_csv_files
from app.database.models import Base
from app.database.providers.azure_sql import engine


def create_database() -> None:
    Base.metadata.create_all(engine)


def main() -> None:
    print("Creating Azure SQL database schema...")

    create_database()

    print("Loading enterprise dataset...")

    load_csv_files(engine)

    print(
        "Azure SQL database initialized."
    )


if __name__ == "__main__":
    main()
