@"
# TechNova Customer Support Bot

A customer-support chatbot built with LangGraph and NVIDIA AI Endpoints.

## Features

- Order status lookup
- Return policy lookup
- Warranty information
- Shipping information
- Tool calling with LangGraph
- Conversation memory with `MemorySaver`
- Error handling for unknown orders

## Tech Stack

- Python
- LangGraph
- LangChain
- NVIDIA AI Endpoints
- `openai/gpt-oss-20b`

## Project Structure

```text
technova-bot/
├── app/
│   ├── chat.py
│   ├── graph.py
│   └── tools.py
├── .gitignore
└── README.md
