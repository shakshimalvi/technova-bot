import sys
import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = PROJECT_ROOT / "results"

REPORT_FILE = PROJECT_ROOT / "report.pdf"


# --------------------------------------------------
# Helper function
# --------------------------------------------------

def read_csv(filename):
    file_path = RESULTS_DIR / filename

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


# --------------------------------------------------
# Load experiment results
# --------------------------------------------------

latency_results = read_csv("latency_results.csv")
token_results = read_csv("token_results.csv")
fault_results = read_csv("fault_results.csv")
evaluation_results = read_csv("evaluation_results.csv")


# --------------------------------------------------
# Calculate metrics
# --------------------------------------------------

latencies = [
    float(row["latency_seconds"])
    for row in latency_results
]

average_latency = sum(latencies) / len(latencies)


total_tokens = [
    int(row["total_tokens"])
    for row in token_results
]

average_tokens = sum(total_tokens) / len(total_tokens)


fault_passed = sum(
    1
    for row in fault_results
    if row["status"] == "PASS"
)

fault_total = len(fault_results)

evaluation_passed = sum(
    1
    for row in evaluation_results
    if row["status"] == "PASS"
)

evaluation_total = len(evaluation_results)

evaluation_accuracy = (
    evaluation_passed / evaluation_total * 100
)


# --------------------------------------------------
# PDF setup
# --------------------------------------------------

document = SimpleDocTemplate(
    str(REPORT_FILE),
    pagesize=A4,
    rightMargin=45,
    leftMargin=45,
    topMargin=45,
    bottomMargin=45,
)


styles = getSampleStyleSheet()


title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=22,
    spaceAfter=20,
)


heading_style = ParagraphStyle(
    "HeadingCustom",
    parent=styles["Heading1"],
    fontSize=15,
    spaceBefore=14,
    spaceAfter=8,
)


body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=10,
    leading=15,
    spaceAfter=8,
)


# --------------------------------------------------
# Document content
# --------------------------------------------------

story = []


# Title
story.append(
    Paragraph(
        "TechNova Customer Support Bot",
        title_style
    )
)

story.append(
    Paragraph(
        "Project Evaluation and Performance Report",
        ParagraphStyle(
            "Subtitle",
            parent=body_style,
            alignment=TA_CENTER,
            fontSize=12,
        ),
    )
)

story.append(Spacer(1, 20))


# --------------------------------------------------
# 1. Project Overview
# --------------------------------------------------

story.append(
    Paragraph(
        "1. Project Overview",
        heading_style
    )
)

story.append(
    Paragraph(
        "TechNova Customer Support Bot is an AI-powered customer "
        "support application for an electronics store. The system "
        "can answer questions about order status, returns, warranty, "
        "and shipping policies.",
        body_style,
    )
)

story.append(
    Paragraph(
        "The application uses LangGraph to control the workflow, "
        "NVIDIA's hosted GPT-OSS-20B model for natural-language "
        "understanding, and custom tools for retrieving order and "
        "policy information.",
        body_style,
    )
)


# --------------------------------------------------
# 2. Technology Stack
# --------------------------------------------------

story.append(
    Paragraph(
        "2. Technology Stack",
        heading_style
    )
)

tech_data = [
    ["Component", "Technology"],
    ["Programming Language", "Python"],
    ["LLM", "GPT-OSS-20B via NVIDIA"],
    ["Workflow", "LangGraph"],
    ["LLM Framework", "LangChain"],
    ["Memory", "LangGraph MemorySaver"],
    ["Observability", "LangSmith"],
    ["Version Control", "Git / GitHub"],
]


tech_table = Table(
    tech_data,
    colWidths=[2.2 * inch, 3.7 * inch]
)

tech_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ])
)

story.append(tech_table)


# --------------------------------------------------
# 3. Architecture
# --------------------------------------------------

story.append(
    Paragraph(
        "3. System Architecture",
        heading_style
    )
)

story.append(
    Paragraph(
        "The application follows a tool-using agent workflow:",
        body_style,
    )
)

architecture = (
    "User Question → LangGraph Agent → GPT-OSS-20B → "
    "Tool Decision → Order/Policy Tool → Tool Result → "
    "LLM Response → User"
)

story.append(
    Paragraph(
        architecture,
        body_style
    )
)

story.append(
    Paragraph(
        "The order-status tool retrieves information from the "
        "application's order data, while the policy tool retrieves "
        "returns, warranty, and shipping information.",
        body_style,
    )
)


# --------------------------------------------------
# 4. Tools
# --------------------------------------------------

story.append(
    Paragraph(
        "4. Available Tools",
        heading_style
    )
)

tools_data = [
    ["Tool", "Purpose"],
    [
        "get_order_status",
        "Retrieves order item, status, and ETA."
    ],
    [
        "get_policy",
        "Retrieves returns, warranty, and shipping policies."
    ],
]


tools_table = Table(
    tools_data,
    colWidths=[2.2 * inch, 3.7 * inch]
)

tools_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ])
)

story.append(tools_table)


# --------------------------------------------------
# 5. Latency Results
# --------------------------------------------------

story.append(
    Paragraph(
        "5. Latency Measurement",
        heading_style
    )
)

story.append(
    Paragraph(
        f"The average measured latency across four test questions "
        f"was <b>{average_latency:.2f} seconds</b>.",
        body_style,
    )
)

latency_data = [
    ["Question", "Latency (seconds)"]
]

for row in latency_results:
    latency_data.append([
        row["question"],
        row["latency_seconds"]
    ])

latency_data.append([
    "Average",
    f"{average_latency:.2f}"
])


latency_table = Table(
    latency_data,
    colWidths=[4.3 * inch, 1.6 * inch]
)

latency_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ])
)

story.append(latency_table)


# --------------------------------------------------
# 6. Token Usage
# --------------------------------------------------

story.append(
    Paragraph(
        "6. Token Usage",
        heading_style
    )
)

story.append(
    Paragraph(
        f"The average total token usage across the four test "
        f"questions was <b>{average_tokens:.2f} tokens per request</b>.",
        body_style,
    )
)

token_data = [
    [
        "Question",
        "Input",
        "Output",
        "Total"
    ]
]

for row in token_results:
    token_data.append([
        row["question"],
        row["input_tokens"],
        row["output_tokens"],
        row["total_tokens"],
    ])

token_table = Table(
    token_data,
    colWidths=[
        3.2 * inch,
        0.8 * inch,
        0.8 * inch,
        0.8 * inch
    ]
)

token_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ])
)

story.append(token_table)


# --------------------------------------------------
# 7. Fault Testing
# --------------------------------------------------

story.append(
    Paragraph(
        "7. Fault Testing",
        heading_style
    )
)

fault_rate = (
    fault_passed / fault_total * 100
    if fault_total
    else 0
)

story.append(
    Paragraph(
        f"The chatbot successfully completed "
        f"<b>{fault_passed} of {fault_total}</b> fault-handling "
        f"test cases ({fault_rate:.0f}%).",
        body_style,
    )
)

fault_data = [
    ["Test Case", "Status"]
]

for row in fault_results:
    fault_data.append([
        row["test_case"],
        row["status"]
    ])

fault_table = Table(
    fault_data,
    colWidths=[4.5 * inch, 1.4 * inch]
)

fault_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ])
)

story.append(fault_table)


# --------------------------------------------------
# 8. Evaluation
# --------------------------------------------------

story.append(
    Paragraph(
        "8. Functional Evaluation",
        heading_style
    )
)

story.append(
    Paragraph(
        f"The evaluation contained {evaluation_total} predefined "
        f"test cases. {evaluation_passed} tests passed, resulting "
        f"in a measured accuracy of <b>{evaluation_accuracy:.2f}%</b> "
        f"on this test set.",
        body_style,
    )
)

evaluation_data = [
    ["Test Case", "Status"]
]

for row in evaluation_results:
    evaluation_data.append([
        row["test_case"],
        row["status"]
    ])

evaluation_table = Table(
    evaluation_data,
    colWidths=[4.5 * inch, 1.4 * inch]
)

evaluation_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ])
)

story.append(evaluation_table)


# --------------------------------------------------
# 9. Observability
# --------------------------------------------------

story.append(
    Paragraph(
        "9. LangSmith Observability",
        heading_style
    )
)

story.append(
    Paragraph(
        "LangSmith was configured to trace the chatbot workflow. "
        "The traces allow inspection of model calls, tool execution, "
        "runs, metadata, and overall execution flow. This provides "
        "useful visibility when debugging and evaluating the application.",
        body_style,
    )
)


# --------------------------------------------------
# 10. Limitations
# --------------------------------------------------

story.append(
    Paragraph(
        "10. Limitations",
        heading_style
    )
)

limitations = [
    "The order and policy data are static demonstration data.",
    "Latency depends on external model/API response time.",
    "The functional evaluation uses a small predefined test set.",
    "The current chatbot can answer questions outside the intended customer-support domain.",
    "The measured evaluation accuracy should not be interpreted as general real-world accuracy.",
]

for limitation in limitations:
    story.append(
        Paragraph(
            "• " + limitation,
            body_style
        )
    )


# --------------------------------------------------
# 11. Conclusion
# --------------------------------------------------

story.append(
    Paragraph(
        "11. Conclusion",
        heading_style
    )
)

story.append(
    Paragraph(
        "The TechNova Customer Support Bot demonstrates a complete "
        "tool-using AI workflow using LangGraph, LangChain, and "
        "GPT-OSS-20B through NVIDIA. The project includes tool "
        "integration, conversation memory, observability, latency "
        "measurement, token tracking, fault testing, and functional "
        "evaluation.",
        body_style,
    )
)

story.append(
    Paragraph(
        "The experiment results provide a reproducible baseline for "
        "future improvements such as stricter domain control, larger "
        "evaluation datasets, improved error handling, and performance "
        "optimization.",
        body_style,
    )
)


# --------------------------------------------------
# Build PDF
# --------------------------------------------------

document.build(story)

print("=" * 50)
print("TechNova Report Generated Successfully")
print("=" * 50)
print(f"Report saved to: {REPORT_FILE}")