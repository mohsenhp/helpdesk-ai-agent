from threading import Lock
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import settings


_lock = Lock()

_memory_checkpointer: InMemorySaver | None = None
_postgres_pool: ConnectionPool | None = None
_postgres_checkpointer: PostgresSaver | None = None


def get_checkpointer() -> Any:
    if settings.checkpoint_database_url is None:
        return _get_memory_checkpointer()

    return _get_postgres_checkpointer()


def _get_memory_checkpointer() -> InMemorySaver:
    global _memory_checkpointer

    with _lock:
        if _memory_checkpointer is None:
            _memory_checkpointer = InMemorySaver()

        return _memory_checkpointer


def _get_postgres_checkpointer() -> PostgresSaver:
    global _postgres_pool
    global _postgres_checkpointer

    with _lock:
        if _postgres_checkpointer is not None:
            return _postgres_checkpointer

        database_url = settings.checkpoint_database_url

        if database_url is None:
            raise RuntimeError(
                "Checkpoint database URL is not configured."
            )

        _postgres_pool = ConnectionPool(
            conninfo=database_url,
            min_size=1,
            max_size=10,
            open=False,
            kwargs={
                "autocommit": True,
                "prepare_threshold": 0,
                "row_factory": dict_row,
            },
        )
        _postgres_pool.open(wait=True)

        _postgres_checkpointer = PostgresSaver(
            _postgres_pool
        )
        _postgres_checkpointer.setup()

        return _postgres_checkpointer


def close_checkpoint_resources() -> None:
    global _postgres_pool
    global _postgres_checkpointer

    with _lock:
        if _postgres_pool is not None:
            _postgres_pool.close()

        _postgres_pool = None
        _postgres_checkpointer = None


def main() -> None:
    checkpointer = get_checkpointer()

    if isinstance(checkpointer, PostgresSaver):
        print(
            "PostgreSQL checkpoint storage initialized."
        )
    else:
        print(
            "CHECKPOINT_DATABASE_URL is not configured; "
            "using in-memory checkpoint storage."
        )

    close_checkpoint_resources()


if __name__ == "__main__":
    main()
