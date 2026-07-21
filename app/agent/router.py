from typing import Literal

from pydantic import BaseModel, Field

from app.llm import get_llm


class RoutingDecision(BaseModel):
    route: Literal["sql", "vector", "hybrid", "chat"] = Field(
        description=(
            "The retrieval route required to answer the question. "
            "Use sql for structured database facts, vector for semantic "
            "document retrieval, and hybrid when both are required."
        )
    )


ROUTER_PROMPT = """
You are a routing component for an enterprise help-desk AI agent.

Classify the user's question into exactly one retrieval route:

- chat:
  Use for greetings, thanks, acknowledgements, casual conversation,
  or questions that do not require enterprise help-desk data.

- sql:
  Use when the question requires exact structured facts, counts, filters,
  joins, statuses, dates, users, departments, assets, tickets, incidents,
  changes, priorities, or software versions.

- vector:
  Use when the question asks for instructions, troubleshooting guidance,
  explanations, policies, runbooks, knowledge-base articles, incident
  narratives, support emails, or release-note content.

- hybrid:
  Use when the question requires both structured database facts and
  unstructured document guidance.

Examples:

Question: How many open Critical VPN tickets are there?
Route: sql

Question: How do I troubleshoot VPN after a Windows update?
Route: vector

Question: Which users have open VPN tickets and what KB article should
support follow?
Route: hybrid

User question:
{question}
""".strip()


def classify_question(question: str) -> RoutingDecision:
    router_llm = get_llm().with_structured_output(
        RoutingDecision
    )

    prompt = ROUTER_PROMPT.format(
        question=question,
    )

    return router_llm.invoke(prompt)
