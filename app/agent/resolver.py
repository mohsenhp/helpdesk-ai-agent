import json

from pydantic import BaseModel, Field

from app.agent.state import ConversationTurn
from app.llm import get_llm


class ResolvedQuestion(BaseModel):
    standalone_question: str = Field(
        description=(
            "A complete standalone help-desk question that can be "
            "understood without seeing the conversation history."
        )
    )


RESOLUTION_PROMPT = """
You rewrite follow-up questions for an enterprise help-desk agent.

Use the conversation history only to resolve references such as:

- they
- them
- those
- that issue
- the previous tickets
- the affected users
- which ones

Return a standalone version of the current question.

Rules:

1. Preserve all constraints from the current question.
2. Use prior context only when necessary.
3. Do not answer the question.
4. Do not invent facts or filters.
5. If the current question is already standalone, return it unchanged.

Conversation history:
{history}

Current question:
{question}
""".strip()


def resolve_question(
    question: str,
    history: list[ConversationTurn],
) -> ResolvedQuestion:
    if not history:
        return ResolvedQuestion(
            standalone_question=question,
        )

    history_json = json.dumps(
        history,
        indent=2,
        ensure_ascii=False,
    )

    resolver_llm = get_llm().with_structured_output(ResolvedQuestion)

    prompt = RESOLUTION_PROMPT.format(
        history=history_json,
        question=question,
    )

    return resolver_llm.invoke(prompt)
