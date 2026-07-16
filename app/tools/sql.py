from typing import Any

from app.database.search import search_database


def search_sql(
    query: str,
) -> dict[str, Any]:
    """
    Retrieve structured information from the SQL database.

    This abstraction allows the SQL backend to change
    (SQLite -> Azure SQL) without affecting the agent.
    """

    return search_database(query)
