from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# States
# ==========================================================

CUSTOMER_SERVICE_STATES = [
    "help_home",
    "search_help",
    "faq_expanded",
    "order_issue",
    "refund_help",
    "contact_options",
    "chat_open",
    "callback_form",
    "support_dialog",
    "resolved_state",
]


# ==========================================================
# Help Topics
# ==========================================================

HELP_TOPICS = [
    {
        "title": "Your Orders",
        "description": "Track packages, cancel orders, or report problems.",
        "icon": "package_2",
    },
    {
        "title": "Returns & Refunds",
        "description": "Return an item or check refund status.",
        "icon": "assignment_return",
    },
    {
        "title": "Payments",
        "description": "Manage payment methods and payment issues.",
        "icon": "credit_card",
    },
    {
        "title": "Prime",
        "description": "Manage membership and Prime benefits.",
        "icon": "workspace_premium",
    },
    {
        "title": "Account Settings",
        "description": "Update login, security, and account information.",
        "icon": "manage_accounts",
    },
    {
        "title": "Delivery",
        "description": "Get help with missing or delayed packages.",
        "icon": "local_shipping",
    },
]


# ==========================================================
# FAQ
# ==========================================================

FAQS = [
    {
        "question": "Where is my order?",
        "answer": (
            "You can view the latest tracking information "
            "from Your Orders."
        ),
    },
    {
        "question": "How do I return an item?",
        "answer": (
            "Open Your Orders, select the product, "
            "and choose Return or Replace Items."
        ),
    },
    {
        "question": "When will my refund arrive?",
        "answer": (
            "Refund timing depends on your payment method "
            "and return processing status."
        ),
    },
    {
        "question": "How can I change my delivery address?",
        "answer": (
            "You may change the address before the order "
            "enters the shipping process."
        ),
    },
    {
        "question": "How do I cancel an order?",
        "answer": (
            "If cancellation is still available, open "
            "Your Orders and select Cancel Items."
        ),
    },
]


# ==========================================================
# Search Suggestions
# ==========================================================

SEARCH_SUGGESTIONS = [
    "track my package",
    "return an item",
    "refund status",
    "cancel an order",
    "payment problem",
    "change delivery address",
]


# ==========================================================
# Recent Order
# ==========================================================

def generate_recent_order() -> dict:

    category = random.choice(
        [
            "Electronics",
            "Fashion",
            "Home",
            "Books",
        ]
    )

    titles = {
        "Electronics": [
            "Wireless Headphones",
            "Bluetooth Speaker",
            "Mechanical Keyboard",
        ],

        "Fashion": [
            "Running Shoes",
            "Casual Jacket",
            "Crossbody Bag",
        ],

        "Home": [
            "LED Desk Lamp",
            "Coffee Maker",
            "Storage Organizer",
        ],

        "Books": [
            "Modern Software Engineering",
            "Practical Machine Learning",
        ],
    }

    return {

        "title":
            random.choice(
                titles[
                    category
                ]
            ),

        "category":
            category,

        "image":
            get_category_image(
                category
            ),

        "status":
            random.choice(
                [
                    "Delivered",
                    "Shipped",
                    "Arriving tomorrow",
                ]
            ),

        "order_number":
            (
                f"{random.randint(100,999)}-"
                f"{random.randint(1000000,9999999)}"
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_customer_service_data() -> dict:

    state = random.choice(
        CUSTOMER_SERVICE_STATES
    )

    faqs = []

    expanded_index = None

    if state == "faq_expanded":

        expanded_index = random.randrange(
            len(FAQS)
        )

    for index, faq in enumerate(
        FAQS
    ):

        faqs.append(
            {
                "question":
                    faq["question"],

                "answer":
                    faq["answer"],

                "expanded":
                    (
                        index
                        == expanded_index
                    ),
            }
        )

    recent_orders = [
        generate_recent_order()
        for _ in range(
            random.randint(
                1,
                3,
            )
        )
    ]

    return {

        "state":
            state,

        "help_topics":
            HELP_TOPICS,

        "faqs":
            faqs,

        "search_query":
            (
                random.choice(
                    SEARCH_SUGGESTIONS
                )
                if state == "search_help"
                else ""
            ),

        "search_suggestions":
            SEARCH_SUGGESTIONS,

        "recent_orders":
            recent_orders,

        "show_order_issue":
            state == "order_issue",

        "show_refund_help":
            state == "refund_help",

        "show_contact_options":
            state == "contact_options",

        "show_chat":
            state == "chat_open",

        "show_callback":
            state == "callback_form",

        "show_support_dialog":
            state == "support_dialog",

        "show_resolved":
            state == "resolved_state",

        "chat_messages": [
            {
                "sender": "support",
                "text": "Hi, how can I help you today?",
            },
            {
                "sender": "user",
                "text": "I need help with a recent order.",
            },
            {
                "sender": "support",
                "text": (
                    "I can help with that. "
                    "Please select the order you need assistance with."
                ),
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_customer_service_data()
    )

    print(
        "\n=============================="
    )

    print(
        "AMAZON CUSTOMER SERVICE"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Recent orders:",
        len(
            data["recent_orders"]
        ),
    )

    print(
        "Chat:",
        data["show_chat"],
    )