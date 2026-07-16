import pandas as pd
from sqlalchemy import text

from app.config import DATASET_DIR


DATASET_SQL_PATH = DATASET_DIR / "sql"


TABLE_FILES = {
    "users": "users.csv",
    "assets": "assets.csv",
    "software_versions": "software_versions.csv",
    "tickets": "tickets.csv",
    "incidents": "incidents.csv",
    "changes": "changes.csv",
}


def load_csv_files(engine) -> None:
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

        with engine.begin() as connection:
            connection.execute(
                text(
                    f"SET IDENTITY_INSERT {table_name} ON"
                )
            )

            dataframe.to_sql(
                table_name,
                con=connection,
                if_exists="append",
                index=False,
            )

            connection.execute(
                text(
                    f"SET IDENTITY_INSERT {table_name} OFF"
                )
            )

        print(
            f"Loaded {table_name}: "
            f"{len(dataframe)} rows"
        )
