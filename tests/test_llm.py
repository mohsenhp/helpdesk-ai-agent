from app import llm


class FakeChatModel:
    pass


def test_get_llm_creates_client_only_once(
    monkeypatch,
) -> None:
    created_clients: list[FakeChatModel] = []

    def fake_constructor(**kwargs) -> FakeChatModel:
        client = FakeChatModel()
        created_clients.append(client)
        return client

    monkeypatch.setattr(
        llm,
        "ChatGoogleGenerativeAI",
        fake_constructor,
    )

    llm.get_llm.cache_clear()

    first_client = llm.get_llm()
    second_client = llm.get_llm()

    assert first_client is second_client
    assert len(created_clients) == 1

    llm.get_llm.cache_clear()
