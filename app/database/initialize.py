from app.config import DATABASE_PATH
from app.database.providers.sqlite import engine
from app.database.loader import load_csv_files
from app.database.models import Base


def create_database() -> None:
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    Base.metadata.create_all(engine)


def main() -> None:
    create_database()
    load_csv_files(engine)

    print(
        "\nSQLite database created at: "
        f"{DATABASE_PATH}"
    )


if __name__ == "__main__":
    main()
