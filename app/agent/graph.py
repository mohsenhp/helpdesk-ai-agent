from langgraph.graph import END, START, StateGraph

from app.agent.router import classify_question
from app.agent.state import AgentState


def route_question(state: AgentState) -> dict[str, str]:
    decision = classify_question(state["question"])

    return {
        "route": decision.route,
    }

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("route_question", route_question)

    builder.add_edge(START, "route_question")
    builder.add_edge("route_question", END)

    return builder.compile()


agent_graph = build_graph()
