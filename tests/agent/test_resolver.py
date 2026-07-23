from app.agent import resolver


def test_first_question_is_returned_without_llm(
    monkeypatch,
) -> None:
    def fail_if_called():
        raise AssertionError("The LLM should not be used for the first question.")

    monkeypatch.setattr(
        resolver,
        "get_llm",
        fail_if_called,
    )

    result = resolver.resolve_question(
        question="Which users have open VPN tickets?",
        history=[],
    )

    assert result.standalone_question == ("Which users have open VPN tickets?")


def test_follow_up_is_rewritten_using_history(
    monkeypatch,
) -> None:
    class FakeStructuredLlm:
        def invoke(
            self,
            prompt: str,
        ) -> resolver.ResolvedQuestion:
            assert "Which of them are in Finance?" in prompt
            assert "open VPN tickets" in prompt

            return resolver.ResolvedQuestion(
                standalone_question=(
                    "Which users with open VPN tickets are in Finance?"
                )
            )

    class FakeLlm:
        def with_structured_output(self, schema):
            return FakeStructuredLlm()

    monkeypatch.setattr(
        resolver,
        "get_llm",
        lambda: FakeLlm(),
    )

    result = resolver.resolve_question(
        question="Which of them are in Finance?",
        history=[
            {
                "question": ("Which users have open VPN tickets?"),
                "answer": "Several users have open VPN tickets.",
            }
        ],
    )

    assert result.standalone_question == (
        "Which users with open VPN tickets are in Finance?"
    )
