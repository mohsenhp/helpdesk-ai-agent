from langgraph.graph import END, START, StateGraph

from app.agent.nodes import (
    create_retrieval_plan,
    retrieve_hybrid,
    retrieve_sql,
    retrieve_vector,
    route_question,
)
from app.agent.state import AgentState, Route


def select_retrieval_route(state: AgentState) -> Route:
    route = state["route"]

    if route is None:
        raise RuntimeError("The routing node did not select a route.")

    return route


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("route_question", route_question)
    builder.add_node("plan_retrieval", create_retrieval_plan)
    builder.add_node("retrieve_sql", retrieve_sql)
    builder.add_node("retrieve_vector", retrieve_vector)
    builder.add_node("retrieve_hybrid", retrieve_hybrid)

    builder.add_edge(START, "route_question")
    builder.add_edge("route_question", "plan_retrieval")

    builder.add_conditional_edges(
        "plan_retrieval",
        select_retrieval_route,
        {
            "sql": "retrieve_sql",
            "vector": "retrieve_vector",
            "hybrid": "retrieve_hybrid",
        },
    )

    builder.add_edge("retrieve_sql", END)
    builder.add_edge("retrieve_vector", END)
    builder.add_edge("retrieve_hybrid", END)

    return builder.compile()


agent_graph = build_graph()
