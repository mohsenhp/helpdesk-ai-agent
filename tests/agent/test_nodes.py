import pytest

from app.agent import nodes
from app.agent.planner import RetrievalPlan
from app.agent.router import RoutingDecision


def make_state() -> dict:
    return {
        "question": "Which users have open VPN tickets?",
        "standalone_question": "Which users have open VPN tickets?",
        "route": None,
        "sql_query": None,
        "vector_query": None,
        "document_type": None,
        "sql_results": None,
        "vector_results": [],
        "answer": None,
        "history": [],
    }


def test_retrieve_sql_rejects_missing_query() -> None:
    state = make_state()

    with pytest.raises(
        RuntimeError,
        match="SQL retrieval query was not planned",
    ):
        nodes.retrieve_sql(state)


def test_retrieve_vector_rejects_missing_query() -> None:
    state = make_state()

    with pytest.raises(
        RuntimeError,
        match="Vector retrieval query was not planned",
    ):
        nodes.retrieve_vector(state)


def test_generate_answer_rejects_missing_route() -> None:
    state = make_state()

    with pytest.raises(
        RuntimeError,
        match="Cannot generate an answer without a route",
    ):
        nodes.generate_answer(state)


def test_route_question_updates_route(monkeypatch) -> None:
    monkeypatch.setattr(
        nodes,
        "classify_question",
        lambda question: RoutingDecision(route="sql"),
    )

    result = nodes.route_question(make_state())

    assert result == {"route": "sql"}


def test_create_retrieval_plan(monkeypatch) -> None:
    state = make_state()
    state["route"] = "hybrid"

    monkeypatch.setattr(
        nodes,
        "plan_retrieval",
        lambda question, route: RetrievalPlan(
            sql_query="users with open VPN tickets",
            vector_query="VPN troubleshooting guidance",
            document_type="kb_articles",
        ),
    )

    result = nodes.create_retrieval_plan(state)

    assert result == {
        "sql_query": "users with open VPN tickets",
        "vector_query": "VPN troubleshooting guidance",
        "document_type": "kb_articles",
    }


def test_retrieve_sql_uses_planned_query(monkeypatch) -> None:
    state = make_state()
    state["sql_query"] = "count open VPN tickets"

    captured_query: list[str] = []

    def fake_search_database(query: str) -> dict:
        captured_query.append(query)
        return {
            "query_type": "ticket_count",
            "rows": [{"count": 4}],
        }

    monkeypatch.setattr(
        nodes,
        "search_database",
        fake_search_database,
    )

    result = nodes.retrieve_sql(state)

    assert captured_query == ["count open VPN tickets"]
    assert result["sql_results"]["rows"] == [{"count": 4}]


def test_retrieve_vector_uses_query_and_filter(monkeypatch) -> None:
    state = make_state()
    state["vector_query"] = "VPN troubleshooting"
    state["document_type"] = "kb_articles"

    captured_arguments: dict = {}

    def fake_search_documents(
        query: str,
        k: int,
        document_type: str | None,
    ) -> list[dict]:
        captured_arguments.update(
            {
                "query": query,
                "k": k,
                "document_type": document_type,
            }
        )
        return [
            {
                "content": "VPN guidance",
                "metadata": {
                    "document_type": "kb_articles",
                },
                "distance": 0.2,
            }
        ]

    monkeypatch.setattr(
        nodes,
        "search_documents",
        fake_search_documents,
    )

    result = nodes.retrieve_vector(state)

    assert captured_arguments == {
        "query": "VPN troubleshooting",
        "k": 5,
        "document_type": "kb_articles",
    }
    assert len(result["vector_results"]) == 1


def test_generate_answer_uses_retrieved_evidence(monkeypatch) -> None:
    state = make_state()
    state["route"] = "sql"
    state["sql_results"] = {
        "rows": [{"count": 2}],
    }

    monkeypatch.setattr(
        nodes,
        "synthesize_answer",
        lambda **kwargs: "There are 2 tickets.",
    )

    result = nodes.generate_answer(state)

    assert result == {
        "answer": "There are 2 tickets.",
    }

def test_resolve_current_question(monkeypatch) -> None:
    state = make_state()
    state["standalone_question"] = None

    monkeypatch.setattr(
        nodes,
        "resolve_question",
        lambda question, history: type(
            "ResolvedQuestion",
            (),
            {
                "standalone_question": (
                    "Which users with open VPN tickets are in Finance?"
                )
            },
        )(),
    )

    result = nodes.resolve_current_question(state)

    assert result == {
        "standalone_question": (
            "Which users with open VPN tickets are in Finance?"
        )
    }


def test_save_conversation_turn() -> None:
    state = make_state()
    state["answer"] = "There are 3 matching users."

    result = nodes.save_conversation_turn(state)

    assert result == {
        "history": [
            {
                "question": "Which users have open VPN tickets?",
                "answer": "There are 3 matching users.",
            }
        ]
    }


def test_save_conversation_turn_rejects_missing_answer() -> None:
    state = make_state()

    with pytest.raises(
        RuntimeError,
        match="Cannot save a conversation turn without an answer",
    ):
        nodes.save_conversation_turn(state)
