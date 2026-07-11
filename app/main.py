import json
from typing import Any

from app.agent.graph import agent_graph


TEST_QUESTIONS = [
    "How many open Critical VPN tickets are there?",
    "How do I troubleshoot VPN after a Windows update?",
    (
        "Which users have open VPN tickets and what KB article "
        "should support follow?"
    ),
]


def print_json(value: Any) -> None:
    print(
        json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )


def main() -> None:
    for question in TEST_QUESTIONS:
        result = agent_graph.invoke(
            {
                "question": question,
                "route": None,
                "sql_results": None,
                "vector_results": [],
            }
        )

        print("=" * 80)
        print(f"Question: {question}")
        print(f"Route: {result['route']}")

        if result["sql_results"] is not None:
            print("\nSQL results:")
            print_json(result["sql_results"])

        if result["vector_results"]:
            print("\nVector results:")
            print_json(result["vector_results"])


if __name__ == "__main__":
    main()
