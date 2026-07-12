import pytest

from app import service


class FakeGraph:
    def invoke(self, state: dict) -> dict:
        return {
            **state,
            "route": "sql",
            "answer": "There are 2 open Critical VPN tickets.",
        }


class GraphWithoutAnswer:
    def invoke(self, state: dict) -> dict:
        return {
            **state,
            "answer": None,
        }


def test_ask_agent_returns_generated_answer(monkeypatch) -> None:
    monkeypatch.setattr(
        service,
        "agent_graph",
        FakeGraph(),
    )

    answer = service.ask_agent(
        "How many open Critical VPN tickets are there?"
    )

    assert answer == "There are 2 open Critical VPN tickets."


def test_ask_agent_rejects_missing_answer(monkeypatch) -> None:
    monkeypatch.setattr(
        service,
        "agent_graph",
        GraphWithoutAnswer(),
    )

    with pytest.raises(
        RuntimeError,
        match="The agent did not generate an answer",
    ):
        service.ask_agent("Question")
