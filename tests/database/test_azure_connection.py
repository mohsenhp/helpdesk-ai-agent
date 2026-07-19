import os

import pytest
from sqlalchemy import text


@pytest.mark.integration
def test_azure_database_connection():
    if not os.getenv("AZURE_SQL_CONNECTION_STRING"):
        pytest.skip(
            "Azure SQL connection string not configured",
        )

    from app.database.providers.azure_sql import engine

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1
