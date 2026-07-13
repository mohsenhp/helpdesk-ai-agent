from types import SimpleNamespace

from langgraph.checkpoint.memory import InMemorySaver

from app.agent import checkpoint


def reset_checkpoint_state() -> None:
    checkpoint.close_checkpoint_resources()
    checkpoint._memory_checkpointer = None


def test_uses_memory_checkpointer_without_database_url(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        checkpoint,
        "settings",
        SimpleNamespace(
            checkpoint_database_url=None,
        ),
    )

    reset_checkpoint_state()

    first = checkpoint.get_checkpointer()
    second = checkpoint.get_checkpointer()

    assert isinstance(first, InMemorySaver)
    assert first is second

    reset_checkpoint_state()


def test_postgres_checkpointer_is_initialized_once(
    monkeypatch,
) -> None:
    created_pools: list[object] = []
    setup_calls: list[bool] = []

    class FakePool:
        def __init__(self, **kwargs) -> None:
            created_pools.append(self)

        def open(self, wait: bool) -> None:
            assert wait is True

        def close(self) -> None:
            pass

    class FakePostgresSaver:
        def __init__(self, pool) -> None:
            self.pool = pool

        def setup(self) -> None:
            setup_calls.append(True)

    monkeypatch.setattr(
        checkpoint,
        "settings",
        SimpleNamespace(
            checkpoint_database_url="postgresql://example",
        ),
    )
    monkeypatch.setattr(
        checkpoint,
        "ConnectionPool",
        FakePool,
    )
    monkeypatch.setattr(
        checkpoint,
        "PostgresSaver",
        FakePostgresSaver,
    )

    reset_checkpoint_state()

    first = checkpoint.get_checkpointer()
    second = checkpoint.get_checkpointer()

    assert first is second
    assert len(created_pools) == 1
    assert len(setup_calls) == 1

    reset_checkpoint_state()
