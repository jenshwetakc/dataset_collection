from __future__ import annotations

import random
from datetime import (
    datetime,
    timedelta,
)

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# States
# ==========================================================

ORDER_PAGE_STATES = [
    "no_orders",
    "recent_orders",
    "delivered",
    "shipped",
    "arriving_today",
    "cancelled",
    "return_started",
    "refund_processing",
    "tracking_open",
    "order_detail_open",
]


# ==========================================================
# Categories
# ==========================================================

CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home",
    "Books",
    "Grocery",
]


# ==========================================================
# Product Titles
# ==========================================================

PRODUCT_TITLES = {

    "Electronics": [
        "Wireless Noise Cancelling Headphones",
        "Portable Bluetooth Speaker",
        "Smart Watch with Fitness Tracking",
        "Mechanical Keyboard",
        "USB-C Fast Charger",
    ],

    "Fashion": [
        "Lightweight Running Shoes",
        "Classic Cotton Casual Shirt",
        "Minimal Crossbody Bag",
        "Relaxed Fit Jacket",
        "Comfort Walking Sneakers",
    ],

    "Home": [
        "Modern LED Desk Lamp",
        "Compact Coffee Maker",
        "Storage Organizer Set",
        "Nonstick Cookware Set",
        "Soft Cotton Bedding Set",
    ],

    "Books": [
        "Practical Machine Learning Handbook",
        "Modern Software Engineering",
        "Introduction to UI Design",
        "Creative Thinking for Everyday Problems",
    ],

    "Grocery": [
        "Premium Roasted Coffee Beans",
        "Healthy Mixed Nut Pack",
        "Assorted Tea Collection",
        "Breakfast Cereal Variety Pack",
    ],
}


# ==========================================================
# Order Statuses
# ==========================================================

ORDER_STATUSES = [
    "Delivered",
    "Shipped",
    "Arriving Today",
    "Preparing for Shipment",
]


# ==========================================================
# Date Helpers
# ==========================================================

def random_past_date(
    max_days: int = 120,
) -> datetime:

    return (
        datetime.now()
        - timedelta(
            days=random.randint(
                1,
                max_days,
            )
        )
    )


def format_date(
    value: datetime,
) -> str:

    return value.strftime(
        "%b %d, %Y"
    )


# ==========================================================
# Product Item
# ==========================================================

def generate_order_item() -> dict:

    category = random.choice(
        CATEGORIES
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
                    8.99,
                    499.99,
                ),
                2,
            ),

        "quantity":
            random.randint(
                1,
                3,
            ),

        "returnable":
            random.random()
            < 0.75,
    }


# ==========================================================
# Tracking Steps
# ==========================================================

def generate_tracking_steps(
    status: str,
) -> list[dict]:

    definitions = [
        "Ordered",
        "Shipped",
        "Out for delivery",
        "Delivered",
    ]

    if status == "Delivered":

        active_index = 3

    elif status == "Arriving Today":

        active_index = 2

    elif status == "Shipped":

        active_index = 1

    else:

        active_index = 0

    return [
        {
            "label":
                label,

            "complete":
                index <= active_index,

            "current":
                index == active_index,
        }

        for index, label
        in enumerate(
            definitions
        )
    ]


# ==========================================================
# Order
# ==========================================================

def generate_order(
    forced_status: str | None = None,
) -> dict:

    order_date = random_past_date()

    status = (
        forced_status
        if forced_status is not None
        else random.choice(
            ORDER_STATUSES
        )
    )

    item_count = random.randint(
        1,
        3,
    )

    items = [
        generate_order_item()
        for _ in range(
            item_count
        )
    ]

    subtotal = sum(
        item["price"]
        * item["quantity"]
        for item in items
    )

    order_number = (
        f"{random.randint(100, 999)}-"
        f"{random.randint(1000000, 9999999)}-"
        f"{random.randint(1000000, 9999999)}"
    )

    return {

        "order_number":
            order_number,

        "date":
            format_date(
                order_date
            ),

        "status":
            status,

        "items":
            items,

        "total":
            round(
                subtotal,
                2,
            ),

        "tracking_steps":
            generate_tracking_steps(
                status
            ),

        "delivery_text":
            random.choice(
                [
                    "Delivered to front door",
                    "Delivered to reception",
                    "Package left in a safe place",
                    "Delivery scheduled",
                ]
            ),

        "payment_method":
            random.choice(
                [
                    "Visa ending in 4242",
                    "Mastercard ending in 7311",
                    "Gift Card",
                    "Account Balance",
                ]
            ),

        "shipping_address":
            random.choice(
                [
                    "Home address",
                    "Office address",
                    "Primary delivery address",
                ]
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_orders_data() -> dict:

    state = random.choice(
        ORDER_PAGE_STATES
    )


    # ======================================================
    # Empty
    # ======================================================

    if state == "no_orders":

        orders = []


    # ======================================================
    # Delivered
    # ======================================================

    elif state == "delivered":

        orders = [
            generate_order(
                "Delivered"
            )
            for _ in range(
                random.randint(
                    2,
                    4,
                )
            )
        ]


    # ======================================================
    # Shipped
    # ======================================================

    elif state == "shipped":

        orders = [
            generate_order(
                "Shipped"
            )
        ]

        orders.extend(
            generate_order()
            for _ in range(
                random.randint(
                    1,
                    3,
                )
            )
        )


    # ======================================================
    # Arriving Today
    # ======================================================

    elif state == "arriving_today":

        orders = [
            generate_order(
                "Arriving Today"
            )
        ]

        orders.extend(
            generate_order()
            for _ in range(
                random.randint(
                    1,
                    2,
                )
            )
        )


    # ======================================================
    # Cancelled
    # ======================================================

    elif state == "cancelled":

        orders = [
            generate_order(
                "Cancelled"
            )
        ]

        orders.extend(
            generate_order()
            for _ in range(
                random.randint(
                    1,
                    2,
                )
            )
        )


    # ======================================================
    # Default
    # ======================================================

    else:

        orders = [
            generate_order()
            for _ in range(
                random.randint(
                    2,
                    5,
                )
            )
        ]


    # ======================================================
    # Selected Order
    # ======================================================

    selected_order = (
        orders[0]
        if orders
        else None
    )


    # ======================================================
    # Special States
    # ======================================================

    return_started = (
        state
        == "return_started"
    )

    refund_processing = (
        state
        == "refund_processing"
    )

    show_tracking = (
        state
        == "tracking_open"
    )

    show_order_detail = (
        state
        == "order_detail_open"
    )


    return {

        "state":
            state,

        "orders":
            orders,

        "selected_order":
            selected_order,

        "return_started":
            return_started,

        "refund_processing":
            refund_processing,

        "show_tracking":
            show_tracking,

        "show_order_detail":
            show_order_detail,

        "filter_label":
            random.choice(
                [
                    "Past 3 months",
                    "2026",
                    "Past 6 months",
                    "All orders",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_orders_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON ORDERS GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Orders:",
        len(
            data["orders"]
        ),
    )

    print(
        "Tracking open:",
        data["show_tracking"],
    )

    print(
        "Order detail open:",
        data["show_order_detail"],
    )