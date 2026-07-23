from app.agent.graph import get_agent_graph


def ask_agent(
    question: str,
    conversation_id: str,
) -> str:
    result = get_agent_graph().invoke(
        {
            "question": question,
            "standalone_question": None,
            "route": None,
            "sql_query": None,
            "vector_query": None,
            "document_type": None,
            "sql_results": None,
            "vector_results": [],
            "answer": None,
            "history": [],
        },
        config={
            "configurable": {
                "thread_id": conversation_id,
            }
        },
    )

    answer = result["answer"]

    if answer is None:
        raise RuntimeError("The agent did not generate an answer.")

    return answer
