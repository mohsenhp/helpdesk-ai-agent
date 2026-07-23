from typing import Any

from langgraph.checkpoint.memory import InMemorySaver

from app.agent import graph as graph_module
from app.agent.state import AgentState


def make_state(question: str) -> AgentState:
    return {
        "question": question,
        "standalone_question": None,
        "route": None,
        "sql_query": None,
        "vector_query": None,
        "document_type": None,
        "sql_results": None,
        "vector_results": [],
        "answer": None,
        "history": [],
    }


def thread_config(thread_id: str) -> dict[str, Any]:
    return {
        "configurable": {
            "thread_id": thread_id,
        }
    }


def build_test_graph(
    monkeypatch,
    observed_histories: dict[str, list[dict[str, str]]],
):
    def fake_resolve_question(
        state: AgentState,
    ) -> dict[str, str]:
        history = list(state["history"])

        observed_histories[state["question"]] = history

        if history:
            previous_question = history[-1]["question"]
            standalone_question = f"{state['question']} (context: {previous_question})"
        else:
            standalone_question = state["question"]

        return {
            "standalone_question": standalone_question,
        }

    def fake_route_question(
        state: AgentState,
    ) -> dict[str, str]:
        return {
            "route": "sql",
        }

    def fake_create_retrieval_plan(
        state: AgentState,
    ) -> dict[str, str | None]:
        return {
            "sql_query": state["standalone_question"],
            "vector_query": None,
            "document_type": None,
        }

    def fake_retrieve_sql(
        state: AgentState,
    ) -> dict[str, dict[str, Any]]:
        return {
            "sql_results": {
                "rows": [
                    {
                        "query": state["sql_query"],
                    }
                ]
            }
        }

    def fake_retrieve_vector(
        state: AgentState,
    ) -> dict[str, list[dict[str, Any]]]:
        return {
            "vector_results": [],
        }

    def fake_retrieve_hybrid(
        state: AgentState,
    ) -> dict[str, Any]:
        return {
            "sql_results": {
                "rows": [],
            },
            "vector_results": [],
        }

    def fake_generate_answer(
        state: AgentState,
    ) -> dict[str, str]:
        return {
            "answer": (f"Answer to: {state['standalone_question']}"),
        }

    def fake_save_conversation_turn(
        state: AgentState,
    ) -> dict[str, list[dict[str, str]]]:
        answer = state["answer"]

        if answer is None:
            raise RuntimeError("Cannot save a conversation turn without an answer.")

        return {
            "history": [
                {
                    "question": state["question"],
                    "answer": answer,
                }
            ]
        }

    monkeypatch.setattr(
        graph_module,
        "resolve_current_question",
        fake_resolve_question,
    )
    monkeypatch.setattr(
        graph_module,
        "route_question",
        fake_route_question,
    )
    monkeypatch.setattr(
        graph_module,
        "create_retrieval_plan",
        fake_create_retrieval_plan,
    )
    monkeypatch.setattr(
        graph_module,
        "retrieve_sql",
        fake_retrieve_sql,
    )
    monkeypatch.setattr(
        graph_module,
        "retrieve_vector",
        fake_retrieve_vector,
    )
    monkeypatch.setattr(
        graph_module,
        "retrieve_hybrid",
        fake_retrieve_hybrid,
    )
    monkeypatch.setattr(
        graph_module,
        "generate_answer",
        fake_generate_answer,
    )
    monkeypatch.setattr(
        graph_module,
        "save_conversation_turn",
        fake_save_conversation_turn,
    )

    return graph_module.build_graph(
        checkpointer=InMemorySaver(),
    )


def test_same_thread_restores_previous_history(
    monkeypatch,
) -> None:
    observed_histories: dict[
        str,
        list[dict[str, str]],
    ] = {}

    graph = build_test_graph(
        monkeypatch,
        observed_histories,
    )

    first_question = "Which users have open VPN tickets?"
    follow_up = "Which of them are in Finance?"

    first_result = graph.invoke(
        make_state(first_question),
        config=thread_config("conversation-1"),
    )

    second_result = graph.invoke(
        make_state(follow_up),
        config=thread_config("conversation-1"),
    )

    assert observed_histories[first_question] == []

    assert observed_histories[follow_up] == [
        {
            "question": first_question,
            "answer": ("Answer to: Which users have open VPN tickets?"),
        }
    ]

    assert second_result["standalone_question"] == (
        "Which of them are in Finance? (context: Which users have open VPN tickets?)"
    )

    assert len(first_result["history"]) == 1
    assert len(second_result["history"]) == 2

    assert second_result["history"][0]["question"] == (first_question)
    assert second_result["history"][1]["question"] == (follow_up)


def test_different_threads_have_isolated_history(
    monkeypatch,
) -> None:
    observed_histories: dict[
        str,
        list[dict[str, str]],
    ] = {}

    graph = build_test_graph(
        monkeypatch,
        observed_histories,
    )

    thread_a_question = "Show open VPN tickets."
    thread_b_question = "Which of them are Critical?"

    graph.invoke(
        make_state(thread_a_question),
        config=thread_config("thread-a"),
    )

    thread_b_result = graph.invoke(
        make_state(thread_b_question),
        config=thread_config("thread-b"),
    )

    assert observed_histories[thread_a_question] == []
    assert observed_histories[thread_b_question] == []

    assert thread_b_result["standalone_question"] == (thread_b_question)
    assert len(thread_b_result["history"]) == 1
