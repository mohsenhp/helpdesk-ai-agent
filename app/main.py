from app.agent.graph import agent_graph


TEST_QUESTIONS = [
    "How many open Critical VPN tickets are there?",
    "How do I troubleshoot VPN after a Windows update?",
    (
        "Which users have open VPN tickets and what KB article "
        "should support follow?"
    ),
]


def main() -> None:
    for question in TEST_QUESTIONS:
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

        print("=" * 80)
        print(f"Question: {question}")
        print(f"Route: {result['route']}")
        print(f"SQL query: {result['sql_query']}")
        print(f"Vector query: {result['vector_query']}")
        print(f"Document type: {result['document_type']}")
        print()
        print("Answer:")
        print(result["answer"])
        print()


if __name__ == "__main__":
    main()
