from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# States
# ==========================================================

RETURN_STATES = [
    "eligible_items",
    "reason_selected",
    "refund_method",
    "return_method",
    "return_review",
    "return_submitted",
    "refund_processing",
    "refund_complete",
    "return_rejected",
    "no_returnable_items",
]


# ==========================================================
# Categories
# ==========================================================

CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home",
    "Books",
]


# ==========================================================
# Products
# ==========================================================

PRODUCT_TITLES = {

    "Electronics": [
        "Wireless Noise Cancelling Headphones",
        "Portable Bluetooth Speaker",
        "Mechanical Keyboard",
        "USB-C Fast Charger",
    ],

    "Fashion": [
        "Lightweight Running Shoes",
        "Classic Cotton Casual Shirt",
        "Crossbody Shoulder Bag",
        "Comfort Walking Sneakers",
    ],

    "Home": [
        "Modern LED Desk Lamp",
        "Compact Coffee Maker",
        "Storage Organizer Set",
        "Soft Cotton Bedding Set",
    ],

    "Books": [
        "Practical Machine Learning Handbook",
        "Modern Software Engineering",
        "Introduction to UI Design",
    ],
}


# ==========================================================
# Return Reasons
# ==========================================================

RETURN_REASONS = [
    "No longer needed",
    "Wrong item received",
    "Item arrived damaged",
    "Product does not work",
    "Better price available",
    "Item does not match description",
]


# ==========================================================
# Refund Methods
# ==========================================================

REFUND_METHODS = [
    {
        "label": "Original payment method",
        "description": "Refund to the card used for this purchase.",
        "icon": "credit_card",
    },
    {
        "label": "Amazon account balance",
        "description": "Receive the refund faster as account credit.",
        "icon": "account_balance_wallet",
    },
]


# ==========================================================
# Return Methods
# ==========================================================

RETURN_METHODS = [
    {
        "label": "Drop off",
        "description": "Bring the package to a nearby drop-off location.",
        "icon": "store",
        "price": 0.0,
    },
    {
        "label": "Home pickup",
        "description": "A courier will collect the package from your address.",
        "icon": "local_shipping",
        "price": 4.99,
    },
    {
        "label": "Locker return",
        "description": "Return the item using a nearby locker.",
        "icon": "inventory_2",
        "price": 0.0,
    },
]


# ==========================================================
# Item Generator
# ==========================================================

def generate_return_item(
    force_returnable: bool = False,
) -> dict:

    category = random.choice(
        CATEGORIES
    )

    returnable = (
        True
        if force_returnable
        else random.random() < 0.8
    )

    return {

        "title":
            random.choice(
                PRODUCT_TITLES[
                    category
                ]
            ),

        "category":
            category,

        "image":
            get_category_image(
                category
            ),

        "price":
            round(
                random.uniform(
                    9.99,
                    299.99,
                ),
                2,
            ),

        "quantity":
            random.randint(
                1,
                2,
            ),

        "returnable":
            returnable,

        "selected":
            False,

        "order_number":
            (
                f"{random.randint(100,999)}-"
                f"{random.randint(1000000,9999999)}"
            ),

        "purchased":
            random.choice(
                [
                    "Aug 12",
                    "Aug 20",
                    "Aug 27",
                    "Sep 1",
                ]
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_returns_data() -> dict:

    state = random.choice(
        RETURN_STATES
    )


    # ======================================================
    # Items
    # ======================================================

    if state == "no_returnable_items":

        items = [
            generate_return_item()
            for _ in range(
                random.randint(
                    2,
                    4,
                )
            )
        ]

        for item in items:
            item["returnable"] = False

    else:

        items = [
            generate_return_item(
                force_returnable=True
            )
            for _ in range(
                random.randint(
                    2,
                    5,
                )
            )
        ]


    # ======================================================
    # Selected Item
    # ======================================================

    selected_item = None

    if items and state != "no_returnable_items":

        selected_item = random.choice(
            items
        )

        selected_item["selected"] = True


    # ======================================================
    # Reason
    # ======================================================

    selected_reason = (
        random.choice(
            RETURN_REASONS
        )
        if state in {
            "reason_selected",
            "refund_method",
            "return_method",
            "return_review",
            "return_submitted",
            "refund_processing",
            "refund_complete",
        }
        else None
    )


    # ======================================================
    # Refund Method
    # ======================================================

    refund_methods = []

    selected_refund_index = (
        random.randrange(
            len(REFUND_METHODS)
        )
    )

    for index, method in enumerate(
        REFUND_METHODS
    ):

        refund_methods.append(
            {
                **method,

                "selected":
                    (
                        index
                        == selected_refund_index
                    ),
            }
        )


    # ======================================================
    # Return Method
    # ======================================================

    return_methods = []

    selected_return_index = (
        random.randrange(
            len(RETURN_METHODS)
        )
    )

    for index, method in enumerate(
        RETURN_METHODS
    ):

        return_methods.append(
            {
                **method,

                "selected":
                    (
                        index
                        == selected_return_index
                    ),
            }
        )


    # ======================================================
    # Progress
    # ======================================================

    if state == "refund_processing":

        refund_progress = random.randint(
            35,
            80,
        )

    elif state == "refund_complete":

        refund_progress = 100

    else:

        refund_progress = 0


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "items":
            items,

        "selected_item":
            selected_item,

        "reasons":
            RETURN_REASONS,

        "selected_reason":
            selected_reason,

        "refund_methods":
            refund_methods,

        "return_methods":
            return_methods,

        "show_reason_section":
            (
                state
                in {
                    "reason_selected",
                    "refund_method",
                    "return_method",
                    "return_review",
                }
            ),

        "show_refund_method":
            (
                state
                in {
                    "refund_method",
                    "return_method",
                    "return_review",
                }
            ),

        "show_return_method":
            (
                state
                in {
                    "return_method",
                    "return_review",
                }
            ),

        "show_review":
            (
                state
                == "return_review"
            ),

        "show_confirmation":
            (
                state
                == "return_submitted"
            ),

        "show_refund_progress":
            (
                state
                in {
                    "refund_processing",
                    "refund_complete",
                }
            ),

        "refund_progress":
            refund_progress,

        "show_rejected":
            (
                state
                == "return_rejected"
            ),

        "return_id":
            (
                f"RET-{random.randint(100000,999999)}"
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_returns_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON RETURNS GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Items:",
        len(
            data["items"]
        ),
    )

    print(
        "Selected:",
        (
            data["selected_item"]["title"]
            if data["selected_item"]
            else None
        ),
    )