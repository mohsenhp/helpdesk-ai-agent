from typing import Any, Literal, TypedDict


Route = Literal["sql", "vector", "hybrid"]

DocumentType = Literal[
    "kb_articles",
    "incident_reports",
    "runbooks",
    "support_emails",
    "release_notes",
]


class AgentState(TypedDict):
    question: str
    route: Route | None

    sql_query: str | None
    vector_query: str | None
    document_type: DocumentType | None

    sql_results: dict[str, Any] | None
    vector_results: list[dict[str, Any]]

    answer: str | None
