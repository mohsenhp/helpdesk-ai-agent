from app.agent.graph import build_graph


def test_graph_can_be_compiled() -> None:
    graph = build_graph()

    assert graph is not None
