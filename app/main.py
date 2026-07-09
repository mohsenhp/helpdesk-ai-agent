from app.llm import llm


def main() -> None:
    response = llm.invoke(
        "Are we connected?"
    )

    print("Gemini connection successful.\n")
    print(response.content)


if __name__ == "__main__":
    main()
