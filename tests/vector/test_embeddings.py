from app.vector import embeddings


class FakeEmbeddings:
    pass


def test_get_embeddings_creates_model_only_once(
    monkeypatch,
) -> None:
    created_models: list[FakeEmbeddings] = []

    def fake_constructor(**kwargs) -> FakeEmbeddings:
        model = FakeEmbeddings()
        created_models.append(model)
        return model

    monkeypatch.setattr(
        embeddings,
        "HuggingFaceEmbeddings",
        fake_constructor,
    )

    embeddings.get_embeddings.cache_clear()

    first_model = embeddings.get_embeddings()
    second_model = embeddings.get_embeddings()

    assert first_model is second_model
    assert len(created_models) == 1

    embeddings.get_embeddings.cache_clear()
