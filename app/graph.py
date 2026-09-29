from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.tools import get_order_status, get_policy


load_dotenv()


MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are TechNova Support Bot, a helpful customer-support assistant
for TechNova, an electronics store.

You can help customers with:
- Order status
- Returns
- Warranty
- Shipping

Important rules:
1. Use the available tools whenever the user asks for order information
   or store policies.
2. Never guess order information or policy information.
3. If an order ID is unknown, clearly tell the customer.
4. Remember information from earlier messages in the same conversation.
5. Answer clearly and concisely.
6. Never expose internal errors or Python stack traces to the customer.
"""


tools = [get_order_status, get_policy]


llm = ChatNVIDIA(
    model=MODEL,
    temperature=0,
    max_completion_tokens=256,
    timeout=120
)


llm_with_tools = llm.bind_tools(tools)


def agent(state: MessagesState):
    messages = state["messages"]

    response = llm_with_tools.invoke(
        [
            ("system", SYSTEM_PROMPT),
            *messages,
        ]
    )

    return {"messages": [response]}


tool_node = ToolNode(tools)


builder = StateGraph(MessagesState)

builder.add_node("agent", agent)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition,
)

builder.add_edge("tools", "agent")


memory = MemorySaver()

graph = builder.compile(checkpointer=memory)