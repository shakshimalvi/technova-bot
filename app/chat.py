from app.graph import graph, MODEL


def chat():
    print("=" * 60)
    print("        TechNova Customer Support Bot")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print("Type 'exit' to quit.")
    print()

    thread_id = input("Enter conversation ID: ").strip()

    if not thread_id:
        thread_id = "user1-chat1"

    config = {
        "configurable": {
            "thread_id": thread_id
        },
        "run_name": "technova_chat",
        "tags": [
            "assignment",
            "technova",
            "gpt-oss-20b"
        ],
        "metadata": {
            "user_id": "user1",
            "session_id": thread_id,
            "model_name": MODEL,
            "app_version": "1.0"
        }
    }

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Bot: Please enter a question.")
            continue

        try:
            result = graph.invoke(
                {
                    "messages": [
                        ("user", question)
                    ]
                },
                config=config
            )

            response = result["messages"][-1]

            print("\nBot:", response.content)

        except Exception as e:
            print("\nERROR:", type(e).__name__)
            print("MESSAGE:", str(e))
            print(
                "Bot: Sorry, I couldn't process your request. "
                "Please try again."
            )


if __name__ == "__main__":
    chat()