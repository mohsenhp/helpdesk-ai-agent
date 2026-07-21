from operator import add
from typing import Annotated, Any, Literal, TypedDict


Route = Literal["sql", "vector", "hybrid", "chat"]

DocumentType = Literal[
    "kb_articles",
    "incident_reports",
    "runbooks",
    "support_emails",
    "release_notes",
]


class ConversationTurn(TypedDict):
    question: str
    answer: str


class AgentState(TypedDict):
    question: str
    standalone_question: str | None
    route: Route | None

    sql_query: str | None
    vector_query: str | None
    document_type: DocumentType | None

    sql_results: dict[str, Any] | None
    vector_results: list[dict[str, Any]]

    answer: str | None

    history: Annotated[list[ConversationTurn], add]
