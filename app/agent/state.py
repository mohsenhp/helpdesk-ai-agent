from typing import Literal, TypedDict


Route = Literal["sql", "vector", "hybrid"]

class AgentState(TypedDict):
    question: str
    route: Route | None
