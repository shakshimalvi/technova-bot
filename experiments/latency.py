import sys
import time
import csv
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.graph import graph


RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

CSV_FILE = RESULTS_DIR / "latency_results.csv"


def measure_latency(question: str, thread_id: str) -> float:
    start_time = time.perf_counter()

    graph.invoke(
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

    end_time = time.perf_counter()

    return end_time - start_time


def main():
    questions = [
        "Where is my order TN1001?",
        "What is the return policy?",
        "What is the warranty policy?",
        "What is the shipping policy?",
    ]

    print("TechNova Latency Test")
    print("=" * 40)

    results = []
    latencies = []

    for i, question in enumerate(questions, start=1):
        thread_id = f"latency-test-{i}"

        latency = measure_latency(
            question,
            thread_id
        )

        latencies.append(latency)

        results.append({
            "question": question,
            "latency_seconds": round(latency, 2)
        })

        print(f"\nQuestion: {question}")
        print(f"Latency: {latency:.2f} seconds")

    average_latency = sum(latencies) / len(latencies)

    print("\n" + "=" * 40)
    print(f"Average latency: {average_latency:.2f} seconds")

    # Save results to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["question", "latency_seconds"]
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {CSV_FILE}")


if __name__ == "__main__":
    main()