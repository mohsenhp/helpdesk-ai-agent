from app.service import ask_agent


EXIT_COMMANDS = {"exit", "quit"}


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
