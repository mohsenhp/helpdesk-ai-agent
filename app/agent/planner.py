from typing import Literal
from pydantic import BaseModel, Field

from app.agent.state import Route, DocumentType
from app.llm import llm


class RetrievalPlan(BaseModel):
    sql_query: str | None = Field(
        description=(
            "A concise natural-language description of the structured "
            "database facts to retrieve. Use null when SQL retrieval "
            "is not required."
        )
    )
    vector_query: str | None = Field(
        description=(
            "A concise semantic search query for document retrieval. "
            "Use null when vector retrieval is not required."
        )
    )
    document_type: DocumentType | None = Field(
        description=(
            "The required document type when the user explicitly asks "
            "for a specific kind of document. Otherwise use null."
        )
    )


planner_llm = llm.with_structured_output(RetrievalPlan)


PLANNER_PROMPT = """
You are a retrieval planner for an enterprise help-desk AI agent.

The question has already been classified into this route:

{route}

Create a retrieval plan.

Rules:

- sql_query:
  Describe only the structured database facts required.
  Preserve important filters such as category, priority, status,
  severity, department, user, asset, and date constraints.
  Use null when the route does not require SQL.

- vector_query:
  Rewrite the question as a concise semantic document search query.
  Focus on the technical issue, troubleshooting topic, incident,
  change, or release information.
  Do not include SQL-specific wording unless it helps document search.
  Use null when the route does not require vector search.

- document_type:
  Set a document type only when the user explicitly requests one.
  Map these concepts:
    KB article or knowledge-base article -> kb_articles
    incident report -> incident_reports
    runbook -> runbooks
    support email -> support_emails
    release note -> release_notes
  Otherwise use null.

Examples:

Question:
How many open Critical VPN tickets are there?

Route:
sql

Plan:
sql_query = "count open Critical VPN tickets"
vector_query = null
document_type = null

Question:
How do I troubleshoot VPN after a Windows update?

Route:
vector

Plan:
sql_query = null
vector_query = "VPN connection failure after Windows update troubleshooting"
document_type = null

Question:
Which users have open VPN tickets and what KB article should support follow?

Route:
hybrid

Plan:
sql_query = "users with open VPN tickets"
vector_query = "VPN troubleshooting guidance"
document_type = "kb_articles"

User question:
{question}
""".strip()


def plan_retrieval(
    question: str,
    route: Route,
) -> RetrievalPlan:
    prompt = PLANNER_PROMPT.format(
        question=question,
        route=route,
    )

    return planner_llm.invoke(prompt)
