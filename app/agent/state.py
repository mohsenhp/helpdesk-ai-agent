from typing import Any, Literal, TypedDict


Route = Literal["sql", "vector", "hybrid"]

class AgentState(TypedDict):
    question: str
    route: Route | None
    sql_results: dict[str, Any] | None
    vector_results: list[dict[str, Any]]
