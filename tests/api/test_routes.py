from fastapi.testclient import TestClient

from app.api import routes
from app.api.application import create_application


client = TestClient(create_application())


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_ask_returns_agent_answer(monkeypatch) -> None:
    monkeypatch.setattr(
        routes,
        "ask_agent",
        lambda question: "There are 2 open Critical VPN tickets.",
    )

    response = client.post(
        "/ask",
        json={
            "question": "How many open Critical VPN tickets are there?",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "There are 2 open Critical VPN tickets.",
    }


def test_ask_strips_surrounding_whitespace(monkeypatch) -> None:
    captured_questions: list[str] = []

    def fake_ask_agent(question: str) -> str:
        captured_questions.append(question)
        return "Answer"

    monkeypatch.setattr(
        routes,
        "ask_agent",
        fake_ask_agent,
    )

    response = client.post(
        "/ask",
        json={
            "question": "   Show open VPN tickets.   ",
        },
    )

    assert response.status_code == 200
    assert captured_questions == [
        "Show open VPN tickets.",
    ]


def test_ask_rejects_blank_question() -> None:
    response = client.post(
        "/ask",
        json={
            "question": "   ",
        },
    )

    assert response.status_code == 422


def test_ask_rejects_missing_question() -> None:
    response = client.post(
        "/ask",
        json={},
    )

    assert response.status_code == 422


def test_ask_returns_service_unavailable_on_agent_failure(
    monkeypatch,
) -> None:
    def failing_agent(question: str) -> str:
        raise RuntimeError("Gemini unavailable")

    monkeypatch.setattr(
        routes,
        "ask_agent",
        failing_agent,
    )

    response = client.post(
        "/ask",
        json={
            "question": "How many open VPN tickets are there?",
        },
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "The agent is temporarily unavailable.",
    }
