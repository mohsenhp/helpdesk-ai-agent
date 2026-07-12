import pandas as pd

from app.config import DATABASE_PATH, DATASET_DIR
from app.database.connection import engine
from app.database.models import Base


DATASET_SQL_PATH = DATASET_DIR / "sql"

TABLE_FILES = {
    "users": "users.csv",
    "assets": "assets.csv",
    "software_versions": "software_versions.csv",
    "tickets": "tickets.csv",
    "incidents": "incidents.csv",
    "changes": "changes.csv",
}


def create_database() -> None:
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    Base.metadata.create_all(engine)


def load_csv_files() -> None:
    for table_name, file_name in TABLE_FILES.items():
        csv_path = DATASET_SQL_PATH / file_name

        if not csv_path.exists():
            raise FileNotFoundError(
                f"Missing CSV file: {csv_path}"
            )

        dataframe = pd.read_csv(csv_path)

        if table_name == "incidents":
            dataframe["resolved"] = (
                dataframe["resolved"]
                .astype(str)
                .str.lower()
                .map(
                    {
                        "true": True,
                        "false": False,
                    }
                )
            )

        dataframe.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False,
        )

        print(
            f"Loaded {table_name}: "
            f"{len(dataframe)} rows"
        )


def main() -> None:
    create_database()
    load_csv_files()

    print(
        "\nSQLite database created at: "
        f"{DATABASE_PATH}"
    )


if __name__ == "__main__":
    main()
