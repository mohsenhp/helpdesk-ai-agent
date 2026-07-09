from pathlib import Path

import pandas as pd

from app.database.connection import DATABASE_PATH, engine
from app.database.models import Base

DATASET_SQL_PATH = Path("data/raw/enterprise_dataset/sql")


TABLE_FILES = {
    "users": "users.csv",
    "assets": "assets.csv",
    "software_versions": "software_versions.csv",
    "tickets": "tickets.csv",
    "incidents": "incidents.csv",
    "changes": "changes.csv",
}


def create_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    Base.metadata.create_all(engine)


def load_csv_files() -> None:
    for table_name, file_name in TABLE_FILES.items():
        csv_path = DATASET_SQL_PATH / file_name

        if not csv_path.exists():
            raise FileNotFoundError(f"Missing CSV file: {csv_path}")

        df = pd.read_csv(csv_path)

        if table_name == "incidents" and "resolved" in df.columns:
            df["resolved"] = df["resolved"].astype(str).str.lower().map(
                {"true": True, "false": False}
            )

        df.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False,
        )

        print(f"Loaded {table_name}: {len(df)} rows")


def main() -> None:
    create_database()
    load_csv_files()

    print(f"\nSQLite database created at: {DATABASE_PATH}")


if __name__ == "__main__":
    main()