import json
import pytest
from app.agent import synthesizer


class FakeResponse:
    def __init__(self, content_blocks: list[dict]) -> None:
        self.content_blocks = content_blocks


def test_serialize_evidence_returns_message_for_none() -> None:
    result = synthesizer._serialize_evidence(None)

    assert result == "No evidence retrieved."


def test_serialize_evidence_returns_message_for_empty_list() -> None:
    result = synthesizer._serialize_evidence([])

    assert result == "No evidence retrieved."


def test_serialize_evidence_converts_dictionary_to_json() -> None:
    evidence = {
        "query_type": "ticket_count",
        "rows": [
            {
                "count": 2,
            }
        ],
    }

    result = synthesizer._serialize_evidence(evidence)

    assert json.loads(result) == evidence


def test_extract_text_returns_single_text_block() -> None:
    response = FakeResponse(
        content_blocks=[
            {
                "type": "text",
                "text": "There are 2 open tickets.",
            }
        ]
    )

    result = synthesizer._extract_text(response)

    assert result == "There are 2 open tickets."


def test_extract_text_combines_multiple_text_blocks() -> None:
    response = FakeResponse(
        content_blocks=[
            {
                "type": "text",
                "text": "First paragraph.",
            },
            {
                "type": "reasoning",
                "reasoning": "Internal reasoning",
            },
            {
                "type": "text",
                "text": "Second paragraph.",
            },
        ]
    )

    result = synthesizer._extract_text(response)

    assert result == "First paragraph.\nSecond paragraph."


def test_extract_text_ignores_non_string_text() -> None:
    response = FakeResponse(
        content_blocks=[
            {
                "type": "text",
                "text": None,
            },
            {
                "type": "text",
                "text": "Valid answer.",
            },
        ]
    )

    result = synthesizer._extract_text(response)

    assert result == "Valid answer."


def test_extract_text_rejects_response_without_text() -> None:
    response = FakeResponse(
        content_blocks=[
            {
                "type": "reasoning",
                "reasoning": "No user-facing text",
            }
        ]
    )

    with pytest.raises(
        RuntimeError,
        match="Gemini returned no textual answer",
    ):
        synthesizer._extract_text(response)


def test_synthesize_answer_invokes_llm_with_evidence(
    monkeypatch,
) -> None:
    captured_prompts: list[str] = []

    class FakeLlm:
        def invoke(self, prompt: str) -> FakeResponse:
            captured_prompts.append(prompt)

            return FakeResponse(
                content_blocks=[
                    {
                        "type": "text",
                        "text": (
                            "There are 2 open Critical VPN tickets."
                        ),
                    }
                ]
            )

    fake_llm = FakeLlm()

    monkeypatch.setattr(
        synthesizer,
        "get_llm",
        lambda: fake_llm,
    )

    answer = synthesizer.synthesize_answer(
        question=(
            "How many open Critical VPN tickets are there?"
        ),
        route="sql",
        sql_results={
            "query_type": "ticket_count",
            "rows": [
                {
                    "count": 2,
                }
            ],
        },
        vector_results=[],
    )

    assert answer == (
        "There are 2 open Critical VPN tickets."
    )
    assert len(captured_prompts) == 1

    prompt = captured_prompts[0]

    assert (
        "How many open Critical VPN tickets are there?"
        in prompt
    )
    assert '"count": 2' in prompt
    assert "No evidence retrieved." in prompt
