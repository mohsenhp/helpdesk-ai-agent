import pytest
from sqlalchemy import text

from app.database.providers.azure_sql import engine


@pytest.mark.integration
def test_azure_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1
