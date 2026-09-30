\# TechNova Customer Support Bot 🤖



An AI-powered customer support chatbot built with \*\*LangGraph, NVIDIA AI, and LangSmith\*\*.



The bot can handle common e-commerce support requests such as order tracking, return policies, warranty information, and shipping details. It uses \*\*tool calling\*\* to retrieve information and \*\*conversation memory\*\* to maintain context across messages.



\## 🚀 Features



\* 📦 Order status lookup using Order ID

\* ↩️ Return policy lookup

\* 🛡️ Warranty information

\* 🚚 Shipping information

\* 🔧 LLM tool calling with LangGraph

\* 🧠 Conversation memory using `MemorySaver`

\* ⚠️ Unknown order handling

\* 🔍 LangSmith tracing and observability

\* 💬 Customer-friendly responses

\* 🔐 API keys protected using `.env`



\## 🏗️ Architecture



```text

&#x20;                   ┌─────────────────┐

&#x20;                   │      User       │

&#x20;                   └────────┬────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌─────────────────┐

&#x20;                   │  Chat Interface │

&#x20;                   │   app/chat.py   │

&#x20;                   └────────┬────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌─────────────────┐

&#x20;                   │  LangGraph      │

&#x20;                   │     Agent       │

&#x20;                   └────────┬────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌─────────────────┐

&#x20;                   │ GPT-OSS-20B     │

&#x20;                   │ NVIDIA Endpoint │

&#x20;                   └────────┬────────┘

&#x20;                            │

&#x20;                      Tool Decision

&#x20;                      ┌─────┴─────┐

&#x20;                      ▼           ▼

&#x20;             ┌─────────────┐ ┌─────────────┐

&#x20;             │get\_order\_   │ │get\_policy() │

&#x20;             │status()     │ │             │

&#x20;             └──────┬──────┘ └──────┬──────┘

&#x20;                    │               │

&#x20;                    └───────┬───────┘

&#x20;                            ▼

&#x20;                   ┌─────────────────┐

&#x20;                   │  Agent Response │

&#x20;                   └────────┬────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌─────────────────┐

&#x20;                   │      User       │

&#x20;                   └─────────────────┘



&#x20;       ┌─────────────────┐     ┌─────────────────┐

&#x20;       │   MemorySaver   │     │    LangSmith    │

&#x20;       │ Conversation    │     │    Tracing      │

&#x20;       │    Memory       │     │  Observability  │

&#x20;       └─────────────────┘     └─────────────────┘

```



\## 🧰 Tech Stack



| Technology          | Purpose                      |

| ------------------- | ---------------------------- |

| Python              | Application development      |

| LangChain           | LLM and tool integration     |

| LangGraph           | Agent workflow orchestration |

| NVIDIA AI Endpoints | LLM inference                |

| GPT-OSS-20B         | Language model               |

| LangSmith           | Tracing and observability    |

| MemorySaver         | Conversation memory          |



\## 📁 Project Structure



```text

technova-bot/

│

├── app/

│   ├── chat.py

│   ├── graph.py

│   └── tools.py

│

├── .env

├── .gitignore

└── README.md

```



\## 🔧 Available Tools



\### `get\_order\_status()`



Looks up an order using its Order ID.



Example:



```text

TN1001

```



Response:



```text

Order TN1001:

Item: Laptop Pro 14,

Status: Shipped,

ETA: 2 days.

```



\### `get\_policy()`



Retrieves TechNova policies for:



\* Returns

\* Warranty

\* Shipping



\## 💬 Example Conversation



```text

You: Where is my order TN1001?



Bot: Your order TN1001 (Laptop Pro 14) has been shipped

and is expected to arrive in 2 days.

```



Another example:



```text

You: What is the warranty policy?



Bot: All electronics carry a 1-year manufacturer warranty.

```



\## 🧠 Conversation Memory



The application uses LangGraph's `MemorySaver` to maintain conversation state.



This allows the assistant to use information from earlier messages within the same conversation thread.



\## 🔍 LangSmith Observability



LangSmith is integrated for tracing and monitoring.



It allows the project to track:



\* Agent runs

\* Tool calls

\* Execution flow

\* Run metadata

\* Model interactions



This makes it easier to debug and understand the agent's behavior.



\## ⚙️ Setup



\### 1. Clone the repository



```bash

git clone https://github.com/shakshimalvi/technova-bot.git

cd technova-bot

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the virtual environment



Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### 4. Install dependencies



```bash

pip install langchain langgraph langchain-nvidia-ai-endpoints langsmith python-dotenv

```



\### 5. Create `.env`



Add your API keys:



```text

NVIDIA\_API\_KEY=your\_nvidia\_api\_key

LANGSMITH\_TRACING=true

LANGSMITH\_API\_KEY=your\_langsmith\_api\_key

LANGSMITH\_PROJECT=TechNova-Bot

```



\*\*Never commit your `.env` file to GitHub.\*\*



\### 6. Run the application



```bash

python -m app.chat

```



\## 🔐 Security



API keys are stored in `.env` and excluded from Git using `.gitignore`.



The repository does not contain the actual API keys.



\## 🎯 Learning Outcomes



Through this project, I gained practical experience with:



\* AI agent workflows

\* LangGraph state management

\* LLM tool calling

\* Conversation memory

\* NVIDIA AI Endpoints

\* LangSmith observability

\* Error handling

\* Git and GitHub project management



\## 👩‍💻 Author



\*\*Shakshi Malvi\*\*



GitHub: https://github.com/shakshimalvi



\---





