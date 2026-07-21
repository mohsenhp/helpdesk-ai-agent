import json
from typing import Any

from app.llm import get_llm


SYNTHESIS_PROMPT = """
You are an enterprise help-desk assistant.

Answer the user's question using only the retrieved evidence provided below.

Rules:

1. Do not invent facts, users, ticket numbers, incidents, procedures,
   or document contents.
2. If the evidence is insufficient, clearly say what information is missing.
3. For structured evidence:
   - Treat counts, statuses, users, priorities, departments, ticket IDs,
     incidents, and other structured values as authoritative.
4. For document evidence:
   - Summarize relevant troubleshooting steps and guidance.
   - Mention document names when useful.
5. For hybrid evidence:
   - Combine structured facts with document guidance.
6. Keep the answer concise but complete.
7. Do not mention internal implementation details such as SQL, Chroma,
   embeddings, LangGraph, routing, or vector distance.
8. Do not expose raw JSON unless the user explicitly asks for it.

User question:
{question}

Retrieval route:
{route}

Structured evidence:
{sql_evidence}

Document evidence:
{vector_evidence}
""".strip()


def _serialize_evidence(value: Any) -> str:
    if value is None or value == []:
        return "No evidence retrieved."

    return json.dumps(
        value,
        indent=2,
        ensure_ascii=False,
        default=str,
    )


def _extract_text(response: Any) -> str:
    text_parts: list[str] = []

    for block in response.content_blocks:
        if block.get("type") == "text":
            text = block.get("text")

            if isinstance(text, str):
                text_parts.append(text)

    if not text_parts:
        raise RuntimeError("Gemini returned no textual answer.")

    return "\n".join(text_parts).strip()


def synthesize_answer(
    question: str,
    route: str,
    sql_results: dict[str, Any] | None,
    vector_results: list[dict[str, Any]],
) -> str:
    if route == "chat":
        prompt = f"""
    You are an enterprise help-desk assistant.

    Respond naturally to the user's message.
    If it is a greeting, greet the user and offer help.
    Do not mention documents, tickets, incidents, or retrieved information.

    User message:
    {question}
    """.strip()
    else:
        prompt = SYNTHESIS_PROMPT.format(
            question=question,
            route=route,
            sql_evidence=_serialize_evidence(sql_results),
            vector_evidence=_serialize_evidence(vector_results),
        )

    response = get_llm().invoke(prompt)

    return _extract_text(response)
