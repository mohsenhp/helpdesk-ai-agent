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
            }
        )

        print(f"Question: {question}")
        print(f"Route: {result['route']}")
        print()


if __name__ == "__main__":
    main()
