from app.agent.graph import agent_graph


def ask_agent(question: str) -> str:
    result = agent_graph.invoke(
        {
            "question": question,
            "route": None,
            "sql_query": None,
            "vector_query": None,
            "document_type": None,
            "sql_results": None,
            "vector_results": [],
            "answer": None,
        }
    )

    answer = result["answer"]

    if answer is None:
        raise RuntimeError("The agent did not generate an answer.")

    return answer
