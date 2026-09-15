from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# States
# ==========================================================

CART_STATES = [
    "empty",
    "single_item",
    "multi_item",
    "quantity_changed",
    "item_removed",
    "saved_for_later",
    "coupon_applied",
    "gift_option",
    "low_stock_warning",
    "checkout_ready",
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
# Cart Item
# ==========================================================

def generate_cart_item(
    force_low_stock: bool = False,
) -> dict:

    category = random.choice(
        CATEGORIES
    )

    quantity = random.randint(
        1,
        4,
    )

    price = round(
        random.uniform(
            9.99,
            499.99,
        ),
        2,
    )

    low_stock = (
        force_low_stock
        or random.random() < 0.12
    )

    if low_stock:

        stock_text = random.choice(
            [
                "Only 1 left in stock",
                "Only 2 left in stock",
                "Low stock",
            ]
        )

    else:

        stock_text = "In Stock"

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
            price,

        "quantity":
            quantity,

        "prime":
            random.random()
            < 0.7,

        "gift_available":
            random.random()
            < 0.6,

        "gift_selected":
            False,

        "low_stock":
            low_stock,

        "stock_text":
            stock_text,

        "seller":
            random.choice(
                [
                    "Amazon",
                    "Official Store",
                    "Prime Retail",
                    "Direct Seller",
                ]
            ),

        "saved":
            False,
    }


# ==========================================================
# Totals
# ==========================================================

def calculate_totals(
    items: list[dict],
    coupon_discount: float = 0.0,
) -> dict:

    subtotal = sum(
        item["price"]
        * item["quantity"]
        for item in items
    )

    discount = round(
        subtotal
        * coupon_discount,
        2,
    )

    after_discount = (
        subtotal
        - discount
    )

    shipping = (
        0.0
        if after_discount >= 35
        else 5.99
    )

    tax = round(
        after_discount
        * 0.08,
        2,
    )

    total = round(
        after_discount
        + shipping
        + tax,
        2,
    )

    return {

        "subtotal":
            round(
                subtotal,
                2,
            ),

        "discount":
            discount,

        "shipping":
            shipping,

        "tax":
            tax,

        "total":
            total,
    }


# ==========================================================
# Saved Items
# ==========================================================

def generate_saved_items() -> list[dict]:

    count = random.randint(
        1,
        3,
    )

    items = []

    for _ in range(count):

        item = generate_cart_item()

        item["saved"] = True

        item["quantity"] = 1

        items.append(
            item
        )

    return items


# ==========================================================
# Recommendations
# ==========================================================

def generate_recommendations() -> list[dict]:

    results = []

    for _ in range(
        random.randint(
            4,
            7,
        )
    ):

        category = random.choice(
            CATEGORIES
        )

        results.append(
            {
                "title":
                    random.choice(
                        PRODUCT_TITLES[
                            category
                        ]
                    ),

                "image":
                    get_category_image(
                        category
                    ),

                "price":
                    round(
                        random.uniform(
                            8.99,
                            249.99,
                        ),
                        2,
                    ),

                "rating":
                    round(
                        random.uniform(
                            3.8,
                            5.0,
                        ),
                        1,
                    ),
            }
        )

    return results


# ==========================================================
# Main Generator
# ==========================================================

def generate_cart_data() -> dict:

    state = random.choice(
        CART_STATES
    )


    # ======================================================
    # Empty
    # ======================================================

    if state == "empty":

        items = []


    # ======================================================
    # Single
    # ======================================================

    elif state == "single_item":

        items = [
            generate_cart_item()
        ]


    # ======================================================
    # Low Stock
    # ======================================================

    elif state == "low_stock_warning":

        items = [
            generate_cart_item(
                force_low_stock=True
            )
        ]

        for _ in range(
            random.randint(
                1,
                2,
            )
        ):

            items.append(
                generate_cart_item()
            )


    # ======================================================
    # Default Multiple
    # ======================================================

    else:

        items = [
            generate_cart_item()
            for _ in range(
                random.randint(
                    2,
                    5,
                )
            )
        ]


    # ======================================================
    # Quantity Changed
    # ======================================================

    if (
        state == "quantity_changed"
        and items
    ):

        target = random.choice(
            items
        )

        target["quantity"] = random.randint(
            3,
            7,
        )


    # ======================================================
    # Gift Option
    # ======================================================

    if (
        state == "gift_option"
        and items
    ):

        target = random.choice(
            items
        )

        target["gift_available"] = True
        target["gift_selected"] = True


    # ======================================================
    # Item Removed
    # ======================================================

    removed_item = None

    if (
        state == "item_removed"
        and items
    ):

        removed_item = items.pop(
            random.randrange(
                len(items)
            )
        )


    # ======================================================
    # Saved For Later
    # ======================================================

    saved_items = []

    if state == "saved_for_later":

        if items:

            saved_item = items.pop(
                random.randrange(
                    len(items)
                )
            )

            saved_item["saved"] = True

            saved_item["quantity"] = 1

            saved_items.append(
                saved_item
            )

        saved_items.extend(
            generate_saved_items()
        )

    elif random.random() < 0.3:

        saved_items = (
            generate_saved_items()
        )


    # ======================================================
    # Coupon
    # ======================================================

    coupon_applied = (
        state == "coupon_applied"
    )

    coupon_percent = (
        random.choice(
            [
                5,
                10,
                15,
            ]
        )
        if coupon_applied
        else 0
    )


    totals = calculate_totals(
        items,
        coupon_discount=(
            coupon_percent / 100
        ),
    )


    # ======================================================
    # Checkout Ready
    # ======================================================

    checkout_ready = (
        state == "checkout_ready"
        or (
            items
            and all(
                not item["low_stock"]
                for item in items
            )
        )
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "items":
            items,

        "saved_items":
            saved_items,

        "removed_item":
            removed_item,

        "coupon_applied":
            coupon_applied,

        "coupon_percent":
            coupon_percent,

        "totals":
            totals,

        "checkout_ready":
            checkout_ready,

        "cart_count":
            sum(
                item["quantity"]
                for item in items
            ),

        "recommendations":
            generate_recommendations(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_cart_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON CART GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Cart items:",
        len(
            data["items"]
        ),
    )

    print(
        "Saved items:",
        len(
            data["saved_items"]
        ),
    )

    print(
        "Cart count:",
        data["cart_count"],
    )

    print(
        "Total:",
        data["totals"]["total"],
    )