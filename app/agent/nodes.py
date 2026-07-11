from typing import Any

from app.agent.router import classify_question
from app.agent.state import AgentState, Route
from app.database.search import search_database
from app.vector.search import search_documents


def route_question(state: AgentState) -> dict[str, Route]:
    decision = classify_question(state["question"])

    return {
        "route": decision.route,
    }


def retrieve_sql(
    state: AgentState,
) -> dict[str, dict[str, Any]]:
    results = search_database(state["question"])

    return {
        "sql_results": results,
    }


def retrieve_vector(
    state: AgentState,
) -> dict[str, list[dict[str, Any]]]:
    results = search_documents(
        query=state["question"],
        k=5,
    )

    return {
        "vector_results": results,
    }


def retrieve_hybrid(
    state: AgentState,
) -> dict[str, Any]:
    sql_results = search_database(state["question"])
    vector_results = search_documents(
        query=state["question"],
        k=5,
    )

    return {
        "sql_results": sql_results,
        "vector_results": vector_results,
    }
