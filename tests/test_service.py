import pytest

from app import service


class FakeGraph:
    def __init__(self) -> None:
        self.received_config: dict | None = None

    def invoke(
        self,
        state: dict,
        config: dict,
    ) -> dict:
        self.received_config = config

        return {
            **state,
            "route": "sql",
            "answer": (
                "There are 2 open Critical VPN tickets."
            ),
        }


class GraphWithoutAnswer:
    def invoke(
        self,
        state: dict,
        config: dict,
    ) -> dict:
        return {
            **state,
            "answer": None,
        }


def test_ask_agent_returns_generated_answer(
    monkeypatch,
) -> None:
    fake_graph = FakeGraph()

    monkeypatch.setattr(
        service,
        "agent_graph",
        fake_graph,
    )

    answer = service.ask_agent(
        question=(
            "How many open Critical VPN tickets are there?"
        ),
        conversation_id="conversation-123",
    )

    assert answer == (
        "There are 2 open Critical VPN tickets."
    )
    assert fake_graph.received_config == {
        "configurable": {
            "thread_id": "conversation-123",
        }
    }


def test_ask_agent_rejects_missing_answer(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        service,
        "agent_graph",
        GraphWithoutAnswer(),
    )

    with pytest.raises(
        RuntimeError,
        match="The agent did not generate an answer",
    ):
        service.ask_agent(
            question="Question",
            conversation_id="conversation-123",
        )
