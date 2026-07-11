from app.agent.graph import agent_graph


EXIT_COMMANDS = {"exit", "quit"}


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


def main() -> None:
    print("HelpDesk AI Agent")
    print('Type "exit" or "quit" to stop.')
    print()

    while True:
        question = input("You: ").strip()

        if not question:
            continue

        if question.lower() in EXIT_COMMANDS:
            print("Goodbye.")
            break

        try:
            answer = ask_agent(question)
        except Exception as error:
            print(f"\nAgent error: {error}\n")
            continue

        print(f"\nAgent: {answer}\n")


if __name__ == "__main__":
    main()
