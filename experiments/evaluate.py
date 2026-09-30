import sys
import csv
import re
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.graph import graph


RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

CSV_FILE = RESULTS_DIR / "evaluation_results.csv"


TEST_CASES = [
    {
        "name": "Order Status",
        "question": "Where is my order TN1001?",
        "expected_keywords": ["TN1001", "Shipped", "2 days"],
    },
    {
        "name": "Return Policy",
        "question": "What is the return policy?",
        "expected_keywords": ["30 days", "original packaging"],
    },
    {
        "name": "Warranty Policy",
        "question": "What is the warranty policy?",
        "expected_keywords": ["1", "year", "manufacturer warranty"],
    },
    {
        "name": "Shipping Policy",
        "question": "What is the shipping policy?",
        "expected_keywords": ["999", "3-5"],
    },
    {
        "name": "Unknown Order",
        "question": "Where is my order TN9999?",
        "expected_keywords": ["TN9999", "couldn't find"],
    },
]


def normalize_text(text: str) -> str:
    """
    Normalize text so that differences in formatting,
    punctuation, currency symbols, and Unicode characters
    do not incorrectly cause evaluation failures.
    """

    text = text.lower()

    # Normalize apostrophes
    text = text.replace("’", "'")
    text = text.replace("‘", "'")

    # Normalize different dash/hyphen characters
    # Normalize different dash/hyphen characters
    for dash in ["‐", "-", "‒", "–", "—", "−", "﹘", "﹣", "－"]:
        text = text.replace(dash, "-")

    # Remove currency symbols
    text = text.replace("₹", "")

    # Replace punctuation with spaces,
    # while keeping hyphens
    text = re.sub(r"[^a-z0-9-]+", " ", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def evaluate_response(response: str, expected_keywords: list) -> bool:
    """
    Check whether all expected keywords are present
    in the normalized model response.
    """

    response_normalized = normalize_text(response)

    return all(
        normalize_text(keyword) in response_normalized
        for keyword in expected_keywords
    )


def run_evaluation(question: str, thread_id: str) -> str:
    """
    Send a question to the TechNova LangGraph
    and return the final response.
    """

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

    return result["messages"][-1].content


def main():

    print("TechNova Evaluation Test")
    print("=" * 50)

    results = []

    for i, test in enumerate(TEST_CASES, start=1):

        response = run_evaluation(
            test["question"],
            f"evaluation-test-{i}"
        )

        passed = evaluate_response(
            response,
            test["expected_keywords"]
        )

        status = "PASS" if passed else "FAIL"

        results.append({
            "test_case": test["name"],
            "question": test["question"],
            "expected_keywords": ", ".join(
                test["expected_keywords"]
            ),
            "status": status,
            "response": response,
        })

        print(f"\nTest: {test['name']}")
        print(f"Question: {test['question']}")
        print(f"Status: {status}")
        print(f"Response: {response}")

    # Calculate evaluation metrics
    total_tests = len(results)

    passed_tests = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    failed_tests = total_tests - passed_tests

    accuracy = (
        passed_tests / total_tests * 100
        if total_tests > 0
        else 0
    )

    # Save results to CSV
    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "test_case",
                "question",
                "expected_keywords",
                "status",
                "response"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n" + "=" * 50)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Results saved to: {CSV_FILE}")


if __name__ == "__main__":
    main()