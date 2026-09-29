from langchain_core.tools import tool


ORDERS = {
    "TN1001": {
        "item": "Laptop Pro 14",
        "status": "Shipped",
        "eta": "2 days",
    },
    "TN1002": {
        "item": "Noise-cancel Earbuds",
        "status": "Processing",
        "eta": "5 days",
    },
    "TN1003": {
        "item": "Phone X",
        "status": "Delivered",
        "eta": "-",
    },
}


POLICIES = {
    "returns": "Returns accepted within 30 days in original packaging.",
    "warranty": "All electronics carry a 1-year manufacturer warranty.",
    "shipping": "Free shipping above Rs. 999. Delivery in 3-5 days.",
}


@tool
def get_order_status(order_id: str) -> str:
    """Look up the status, item, and estimated delivery of a TechNova order using its order ID."""

    order_id = order_id.strip().upper()

    order = ORDERS.get(order_id)

    if order is None:
        return f"No order was found with order ID {order_id}."

    return (
        f"Order {order_id}: "
        f"Item: {order['item']}, "
        f"Status: {order['status']}, "
        f"ETA: {order['eta']}."
    )


@tool
def get_policy(topic: str) -> str:
    """Look up a TechNova store policy for returns, warranty, or shipping."""

    topic = topic.strip().lower()

    policy = POLICIES.get(topic)

    if policy is None:
        return (
            "Policy topic not found. Available topics are: "
            "returns, warranty, shipping."
        )

    return policy