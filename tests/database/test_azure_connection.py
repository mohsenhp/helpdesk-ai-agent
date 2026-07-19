import os
import pytest

if not os.getenv("AZURE_SQL_CONNECTION_STRING"):
    pytest.skip(
        "Azure SQL connection string not configured",
        allow_module_level=True,
    )

from app.database.providers.azure_sql import engine
