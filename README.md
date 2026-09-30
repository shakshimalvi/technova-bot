# TechNova Customer Support Bot 🤖

An AI-powered customer support chatbot built with **LangGraph, NVIDIA AI Endpoints, and Python**. The chatbot can answer order-status and store-policy questions, use tools when required, maintain conversation memory, and provide observability through LangSmith.

---

## 🚀 Project Overview

The **TechNova Customer Support Bot** is designed for an electronics store and handles common customer-support queries such as:

* 📦 Order status
* 🔄 Return policy
* 🛡️ Warranty information
* 🚚 Shipping policy

The application uses an LLM with tool calling and a LangGraph workflow to decide when external tools should be used.

The project also includes experiments for:

* Latency measurement
* Token usage analysis
* Fault testing
* Functional evaluation
* LangSmith tracing
* PDF report generation

---

## 🏗️ System Architecture

```text
                    User
                     │
                     ▼
              ┌──────────────┐
              │  Chat Input  │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │  LangGraph   │
              │    Agent     │
              └──────┬───────┘
                     │
              Tool required?
                ┌────┴────┐
               Yes        No
                │          │
                ▼          ▼
        ┌──────────────┐  Response
        │  Tool Node   │
        └──────┬───────┘
               │
               ▼
       ┌──────────────────┐
       │ Order / Policy   │
       │      Tools       │
       └────────┬─────────┘
                │
                ▼
             Agent
                │
                ▼
             Response

       Memory: MemorySaver
       Observability: LangSmith
```

---

## 🧠 Technology Stack

| Technology           | Purpose                          |
| -------------------- | -------------------------------- |
| Python               | Application development          |
| LangGraph            | Agent workflow and orchestration |
| LangChain            | LLM and tool integration         |
| NVIDIA AI Endpoints  | LLM access                       |
| `openai/gpt-oss-20b` | Language model                   |
| LangSmith            | Tracing and observability        |
| Python-dotenv        | Environment variable management  |
| ReportLab            | PDF report generation            |
| Git & GitHub         | Version control                  |

---

## 🤖 Model

The project currently uses:

```text
openai/gpt-oss-20b
```

Configuration:

```text
Temperature: 0
Max completion tokens: 256
Timeout: 120 seconds
```

The model is connected to the available TechNova tools through LangChain tool calling.

---

## 🛠️ Available Tools

### 1. Order Status

```python
get_order_status(order_id)
```

Retrieves:

* Order ID
* Product
* Order status
* Estimated delivery

Example:

```text
User: Where is my order TN1001?

Bot: Order TN1001: Item: Laptop Pro 14,
Status: Shipped, ETA: 2 days.
```

---

### 2. Store Policy

```python
get_policy(topic)
```

Supported topics:

* Returns
* Warranty
* Shipping

Example:

```text
User: What is the return policy?

Bot: Returns accepted within 30 days in original packaging.
```

---

## 💾 Conversation Memory

The application uses LangGraph's:

```python
MemorySaver()
```

Conversation state is associated with a `thread_id`.

This allows the chatbot to maintain context during the same conversation.

Example:

```text
User: Where is my order TN1001?

Bot: Your order TN1001 is shipped and expected in 2 days.

User: What about the warranty?

Bot: All electronics carry a 1-year manufacturer warranty.
```

---

## 📊 Experiments and Evaluation

The project includes four experiments.

### 1. Latency Measurement

Four representative queries were tested.

| Query           | Latency |
| --------------- | ------: |
| Order status    |  2.94 s |
| Return policy   |  5.80 s |
| Warranty policy |  2.63 s |
| Shipping policy |  3.82 s |

**Average latency: 3.80 seconds**

Results are stored in:

```text
results/latency_results.csv
```

---

### 2. Token Usage

Token usage was measured for the same four queries.

| Query           | Input | Output | Total |
| --------------- | ----: | -----: | ----: |
| Order status    |   373 |     48 |   421 |
| Return policy   |   366 |     61 |   427 |
| Warranty policy |   368 |     40 |   408 |
| Shipping policy |   372 |     53 |   425 |

**Average total tokens: 420.25**

Results are stored in:

```text
results/token_results.csv
```

---

### 3. Fault Testing

The chatbot was tested against:

* Unknown order ID
* Invalid policy topic
* Empty input
* Unexpected question

Result:

```text
4 / 4 tests passed
Pass rate: 100%
```

Results are stored in:

```text
results/fault_results.csv
```

One observed limitation is that the chatbot can answer questions outside the intended TechNova support scope instead of strictly refusing them.

---

### 4. Functional Evaluation

Five predefined test cases were evaluated:

1. Order status
2. Return policy
3. Warranty policy
4. Shipping policy
5. Unknown order

Result:

```text
Total tests: 5
Passed: 5
Failed: 0
Accuracy: 100%
```

This result represents **5/5 predefined evaluation cases**, not general-purpose chatbot accuracy.

Results are stored in:

```text
results/evaluation_results.csv
```

---

## 🔍 LangSmith Observability

LangSmith tracing is enabled to monitor chatbot executions.

The project tracks information such as:

* LLM calls
* Tool calls
* Execution flow
* Latency
* Token usage
* Errors
* Conversation runs

This helps with debugging, performance analysis, and evaluation.

---

## 📁 Project Structure

```text
technova-bot/
│
├── README.md
├── .env.example
├── requirements.txt
├── report.pdf
│
├── app/
│   ├── chat.py
│   ├── graph.py
│   └── tools.py
│
├── experiments/
│   ├── latency.py
│   ├── tokens.py
│   ├── faults.py
│   ├── evaluate.py
│   └── generate_report.py
│
└── results/
    ├── latency_results.csv
    ├── token_results.csv
    ├── fault_results.csv
    └── evaluation_results.csv
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/shakshimalvi/technova-bot.git
cd technova-bot
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

```text
NVIDIA_API_KEY=your_nvidia_api_key
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=TechNova-Bot
```

**Never commit your actual `.env` file or API keys to GitHub.**

---

## ▶️ Run the Chatbot

From the project root:

```powershell
python -m app.chat
```

Enter a conversation ID when prompted.

Example:

```text
============================================================
        TechNova Customer Support Bot
============================================================
Model: openai/gpt-oss-20b
Type 'exit' to quit.

Enter conversation ID: user1-chat1

You: Where is my order TN1001?

Bot: Order TN1001: Item: Laptop Pro 14,
Status: Shipped, ETA: 2 days.
```

Type:

```text
exit
```

to end the conversation.

---

## 🧪 Run Experiments

### Latency

```powershell
python experiments\latency.py
```

### Token Usage

```powershell
python experiments\tokens.py
```

### Fault Testing

```powershell
python experiments\faults.py
```

### Functional Evaluation

```powershell
python experiments\evaluate.py
```

### Generate PDF Report

```powershell
python experiments\generate_report.py
```

The generated report is:

```text
report.pdf
```

---

## 📄 Project Report

The complete experimental report is available in:

```text
report.pdf
```

It contains:

* Project overview
* Technology stack
* System architecture
* Tool descriptions
* Latency analysis
* Token usage
* Fault testing
* Functional evaluation
* LangSmith observability
* Limitations
* Conclusion

---

## 🔐 Security

API keys and other sensitive configuration values are stored in `.env`.

The following files are excluded from Git:

```text
.env
venv/
__pycache__/
*.pyc
```

Only `.env.example` with placeholder values is included in the repository.

---

## ⚠️ Limitations

* Order and policy information currently comes from predefined in-memory data.
* The chatbot is not connected to a real e-commerce database.
* The evaluation dataset contains only five predefined functional test cases.
* Latency depends on the external model/API response time and network conditions.
* The current chatbot can respond to questions outside the intended customer-support scope.
* Production deployment would require authentication, persistent storage, monitoring, and stronger validation.

---

## 🎯 Learning Outcomes

This project provided practical experience with:

* LangGraph agent workflows
* LLM tool calling
* LangChain tools
* Conversation memory
* Error handling
* LangSmith observability
* LLM latency measurement
* Token usage analysis
* Automated functional testing
* Fault testing
* Git and GitHub workflow
* Technical documentation and reporting

---

## 👩‍💻 Author

**Shakshi Malvi**

B.Tech — Computer Science & Engineering

Interested in:

* Data Science
* Machine Learning
* Generative AI
* NLP
* AI Engineering

GitHub:
https://github.com/shakshimalvi

---

## ⭐ Project Summary

TechNova Customer Support Bot demonstrates how an LLM can be combined with **LangGraph, tools, memory, and observability** to build a structured customer-support application.

The project goes beyond basic chatbot implementation by including **performance experiments, token analysis, fault testing, functional evaluation, LangSmith tracing, and a documented PDF report**.
