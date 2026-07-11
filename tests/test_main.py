import pytest

from app import main


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
        main,
        "agent_graph",
        FakeGraph(),
    )

    answer = main.ask_agent(
        "How many open Critical VPN tickets are there?"
    )

    assert answer == "There are 2 open Critical VPN tickets."


def test_ask_agent_rejects_missing_answer(monkeypatch) -> None:
    monkeypatch.setattr(
        main,
        "agent_graph",
        GraphWithoutAnswer(),
    )

    with pytest.raises(
        RuntimeError,
        match="The agent did not generate an answer",
    ):
        main.ask_agent("Question")
