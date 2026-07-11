from typing import Any

from app.agent.planner import plan_retrieval
from app.agent.router import classify_question
from app.agent.state import AgentState, DocumentType, Route
from app.agent.synthesizer import synthesize_answer
from app.database.search import search_database
from app.vector.search import search_documents


def route_question(state: AgentState) -> dict[str, Route]:
    decision = classify_question(state["question"])

    return {
        "route": decision.route,
    }


def create_retrieval_plan(
    state: AgentState,
) -> dict[str, str | DocumentType | None]:
    route = state["route"]

    if route is None:
        raise RuntimeError("The routing node did not select a route.")

    plan = plan_retrieval(
        question=state["question"],
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
