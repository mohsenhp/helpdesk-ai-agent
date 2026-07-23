from functools import lru_cache

from app.agent.checkpoint import get_checkpointer
from langgraph.graph import END, START, StateGraph

from app.agent.nodes import (
    create_retrieval_plan,
    generate_answer,
    resolve_current_question,
    retrieve_hybrid,
    retrieve_sql,
    retrieve_vector,
    route_question,
    save_conversation_turn,
)
from app.agent.state import AgentState, Route


def select_retrieval_route(state: AgentState) -> Route:
    route = state["route"]

    if route is None:
        raise RuntimeError("The routing node did not select a route.")

    return route


def build_graph(
    checkpointer=None,
):
    builder = StateGraph(AgentState)

    builder.add_node(
        "resolve_question",
        resolve_current_question,
    )
    builder.add_node(
        "route_question",
        route_question,
    )
    builder.add_node(
        "plan_retrieval",
        create_retrieval_plan,
    )
    builder.add_node(
        "retrieve_sql",
        retrieve_sql,
    )
    builder.add_node(
        "retrieve_vector",
        retrieve_vector,
    )
    builder.add_node(
        "retrieve_hybrid",
        retrieve_hybrid,
    )
    builder.add_node(
        "generate_answer",
        generate_answer,
    )
    builder.add_node(
        "save_conversation_turn",
        save_conversation_turn,
    )

    builder.add_edge(
        START,
        "resolve_question",
    )
    builder.add_edge(
        "resolve_question",
        "route_question",
    )
    builder.add_edge(
        "route_question",
        "plan_retrieval",
    )

    builder.add_conditional_edges(
        "plan_retrieval",
        select_retrieval_route,
        {
            "sql": "retrieve_sql",
            "vector": "retrieve_vector",
            "hybrid": "retrieve_hybrid",
            "chat": "generate_answer",
        },
    )

    builder.add_edge(
        "retrieve_sql",
        "generate_answer",
    )
    builder.add_edge(
        "retrieve_vector",
        "generate_answer",
    )
    builder.add_edge(
        "retrieve_hybrid",
        "generate_answer",
    )

    builder.add_edge(
        "generate_answer",
        "save_conversation_turn",
    )
    builder.add_edge(
        "save_conversation_turn",
        END,
    )

    return builder.compile(
        checkpointer=checkpointer,
    )


@lru_cache(maxsize=1)
def get_agent_graph():
    return build_graph(
        checkpointer=get_checkpointer(),
    )
