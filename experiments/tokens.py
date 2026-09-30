import sys
import csv
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.graph import graph


RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

CSV_FILE = RESULTS_DIR / "token_results.csv"


def measure_tokens(question: str, thread_id: str):
    result = graph.invoke(
        {
            "messages": [
                ("user", question)
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    response = result["messages"][-1]

    usage = response.response_metadata.get("token_usage", {})

    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    return input_tokens, output_tokens, total_tokens


def main():

    questions = [
        "Where is my order TN1001?",
        "What is the return policy?",
        "What is the warranty policy?",
        "What is the shipping policy?",
    ]

    print("TechNova Token Usage Test")
    print("=" * 40)

    results = []

    for i, question in enumerate(questions, start=1):

        thread_id = f"token-test-{i}"

        input_tokens, output_tokens, total_tokens = measure_tokens(
            question,
            thread_id
        )

        results.append({
            "question": question,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens
        })

        print(f"\nQuestion: {question}")
        print(f"Input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Total tokens: {total_tokens}")

    # Save results
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "question",
                "input_tokens",
                "output_tokens",
                "total_tokens"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n" + "=" * 40)
    print(f"Results saved to: {CSV_FILE}")


if __name__ == "__main__":
    main()