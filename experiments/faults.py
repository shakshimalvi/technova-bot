import sys
import csv
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.graph import graph


RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

CSV_FILE = RESULTS_DIR / "fault_results.csv"


TEST_CASES = [
    {
        "name": "Unknown Order ID",
        "question": "Where is my order TN9999?"
    },
    {
        "name": "Invalid Policy Topic",
        "question": "What is the cancellation policy?"
    },
    {
        "name": "Empty Input",
        "question": ""
    },
    {
        "name": "Unexpected Question",
        "question": "What is the capital of France?"
    },
]


def run_test(question: str, thread_id: str):
    try:
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

        return "PASS", response.content

    except Exception as e:
        return "FAIL", f"{type(e).__name__}: {str(e)}"


def main():

    print("TechNova Fault Testing")
    print("=" * 50)

    results = []

    for i, test in enumerate(TEST_CASES, start=1):

        status, response = run_test(
            test["question"],
            f"fault-test-{i}"
        )

        results.append({
            "test_case": test["name"],
            "question": test["question"],
            "status": status,
            "response": response
        })

        print(f"\nTest: {test['name']}")
        print(f"Question: {test['question']}")
        print(f"Status: {status}")
        print(f"Response: {response}")

    # Save results
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "test_case",
                "question",
                "status",
                "response"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    passed = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    failed = len(results) - passed

    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print(f"Results saved to: {CSV_FILE}")


if __name__ == "__main__":
    main()