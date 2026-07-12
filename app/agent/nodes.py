from typing import Any

from app.agent.planner import plan_retrieval
from app.agent.router import classify_question
from app.agent.state import AgentState, DocumentType, Route
from app.agent.synthesizer import synthesize_answer
from app.agent.resolver import resolve_question
from app.database.search import search_database
from app.vector.search import search_documents


def route_question(state: AgentState) -> dict[str, Route]:
    question = state["standalone_question"]

    if question is None:
        raise RuntimeError(
            "The current question was not resolved."
        )

    decision = classify_question(question)

    return {
        "route": decision.route,
    }


def create_retrieval_plan(
    state: AgentState,
) -> dict[str, str | DocumentType | None]:
    route = state["route"]
    question = state["standalone_question"]

    if route is None:
        raise RuntimeError(
            "The routing node did not select a route."
        )

    if question is None:
        raise RuntimeError(
            "The current question was not resolved."
        )

    plan = plan_retrieval(
        question=question,
        route=route,
    )

    return {
        "sql_query": plan.sql_query,
        "vector_query": plan.vector_query,
        "document_type": plan.document_type,
    }


def retrieve_sql(
    state: AgentState,
) -> dict[str, dict[str, Any]]:
    query = state["sql_query"]

    if query is None:
        raise RuntimeError("SQL retrieval query was not planned.")

    return {
        "sql_results": search_database(query),
    }


def retrieve_vector(
    state: AgentState,
) -> dict[str, list[dict[str, Any]]]:
    query = state["vector_query"]

    if query is None:
        raise RuntimeError("Vector retrieval query was not planned.")

    return {
        "vector_results": search_documents(
            query=query,
            k=5,
            document_type=state["document_type"],
        ),
    }


def retrieve_hybrid(
    state: AgentState,
) -> dict[str, Any]:
    sql_query = state["sql_query"]
    vector_query = state["vector_query"]

    if sql_query is None:
        raise RuntimeError("SQL retrieval query was not planned.")

    if vector_query is None:
        raise RuntimeError("Vector retrieval query was not planned.")

    return {
        "sql_results": search_database(sql_query),
        "vector_results": search_documents(
            query=vector_query,
            k=5,
            document_type=state["document_type"],
        ),
    }


def generate_answer(
    state: AgentState,
) -> dict[str, str]:
    route = state["route"]

    if route is None:
        raise RuntimeError("Cannot generate an answer without a route.")

    answer = synthesize_answer(
        question=state["question"],
        route=route,
        sql_results=state["sql_results"],
        vector_results=state["vector_results"],
    )

    return {
        "answer": answer,
    }


def resolve_current_question(
    state: AgentState,
) -> dict[str, str]:
    resolved = resolve_question(
        question=state["question"],
        history=state["history"],
    )

    return {
        "standalone_question": resolved.standalone_question,
    }


def save_conversation_turn(
    state: AgentState,
) -> dict[str, list[dict[str, str]]]:
    answer = state["answer"]

    if answer is None:
        raise RuntimeError(
            "Cannot save a conversation turn without an answer."
        )

    return {
        "history": [
            {
                "question": state["question"],
                "answer": answer,
            }
        ]
    }
