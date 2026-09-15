from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# States
# ==========================================================

CHECKOUT_STATES = [
    "address_selection",
    "address_form_open",
    "delivery_selection",
    "payment_selection",
    "payment_form_open",
    "review_order",
    "validation_error",
    "promo_applied",
    "place_order_ready",
    "order_placed",
]


# ==========================================================
# Product Data
# ==========================================================

CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home",
    "Books",
    "Grocery",
]


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

    "Grocery": [
        "Premium Roasted Coffee Beans",
        "Healthy Mixed Nut Pack",
        "Assorted Tea Collection",
    ],
}


# ==========================================================
# Addresses
# ==========================================================

def generate_addresses() -> list[dict]:

    addresses = [
        {
            "name": "Alex Morgan",
            "line1": "24 Maple Street",
            "line2": "Apartment 302",
            "city": "Seoul",
            "postal_code": "02841",
            "country": "South Korea",
        },
        {
            "name": "Alex Morgan",
            "line1": "101 Central Avenue",
            "line2": "Office 8F",
            "city": "Seoul",
            "postal_code": "04524",
            "country": "South Korea",
        },
        {
            "name": "Alex Morgan",
            "line1": "73 Riverside Road",
            "line2": "",
            "city": "Incheon",
            "postal_code": "21554",
            "country": "South Korea",
        },
    ]

    selected_index = random.randrange(
        len(addresses)
    )

    for index, address in enumerate(
        addresses
    ):

        address["selected"] = (
            index == selected_index
        )

    return addresses


# ==========================================================
# Delivery Options
# ==========================================================

def generate_delivery_options() -> list[dict]:

    options = [
        {
            "title": "FREE delivery",
            "subtitle": "Delivery in 3–5 business days",
            "price": 0.0,
        },
        {
            "title": "Standard delivery",
            "subtitle": "Delivery in 2–3 business days",
            "price": 4.99,
        },
        {
            "title": "Priority delivery",
            "subtitle": "Delivery tomorrow",
            "price": 9.99,
        },
    ]

    selected_index = random.randrange(
        len(options)
    )

    for index, option in enumerate(
        options
    ):

        option["selected"] = (
            index == selected_index
        )

    return options


# ==========================================================
# Payment Methods
# ==========================================================

def generate_payment_methods() -> list[dict]:

    methods = [
        {
            "type": "Visa",
            "label": "Visa ending in 4242",
            "icon": "credit_card",
        },
        {
            "type": "Mastercard",
            "label": "Mastercard ending in 7311",
            "icon": "credit_card",
        },
        {
            "type": "Balance",
            "label": "Amazon account balance",
            "icon": "account_balance_wallet",
        },
    ]

    selected_index = random.randrange(
        len(methods)
    )

    for index, method in enumerate(
        methods
    ):

        method["selected"] = (
            index == selected_index
        )

    return methods


# ==========================================================
# Order Item
# ==========================================================

def generate_checkout_item() -> dict:

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
                    299.99,
                ),
                2,
            ),

        "quantity":
            random.randint(
                1,
                3,
            ),

        "prime":
            random.random()
            < 0.7,
    }


# ==========================================================
# Totals
# ==========================================================

def calculate_totals(
    items: list[dict],
    delivery_price: float,
    promo_percent: int = 0,
) -> dict:

    subtotal = sum(
        item["price"]
        * item["quantity"]
        for item in items
    )

    discount = round(
        subtotal
        * (
            promo_percent / 100
        ),
        2,
    )

    taxable = (
        subtotal
        - discount
        + delivery_price
    )

    tax = round(
        taxable * 0.08,
        2,
    )

    total = round(
        taxable
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

        "delivery":
            delivery_price,

        "tax":
            tax,

        "total":
            total,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_checkout_data() -> dict:

    state = random.choice(
        CHECKOUT_STATES
    )

    addresses = generate_addresses()

    delivery_options = (
        generate_delivery_options()
    )

    payment_methods = (
        generate_payment_methods()
    )

    items = [
        generate_checkout_item()
        for _ in range(
            random.randint(
                1,
                4,
            )
        )
    ]


    # ======================================================
    # Selected Values
    # ======================================================

    selected_address = next(
        address
        for address in addresses
        if address["selected"]
    )

    selected_delivery = next(
        option
        for option
        in delivery_options
        if option["selected"]
    )

    selected_payment = next(
        method
        for method
        in payment_methods
        if method["selected"]
    )


    # ======================================================
    # Promo
    # ======================================================

    promo_applied = (
        state == "promo_applied"
    )

    promo_percent = (
        random.choice(
            [
                5,
                10,
                15,
            ]
        )
        if promo_applied
        else 0
    )


    # ======================================================
    # Validation
    # ======================================================

    validation_error = (
        state
        == "validation_error"
    )

    validation_message = (
        random.choice(
            [
                "Please select a valid payment method.",
                "Your delivery address is incomplete.",
                "Please review the highlighted fields.",
            ]
        )
        if validation_error
        else None
    )


    # ======================================================
    # Totals
    # ======================================================

    totals = calculate_totals(
        items,
        delivery_price=
            selected_delivery["price"],

        promo_percent=
            promo_percent,
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "addresses":
            addresses,

        "selected_address":
            selected_address,

        "delivery_options":
            delivery_options,

        "selected_delivery":
            selected_delivery,

        "payment_methods":
            payment_methods,

        "selected_payment":
            selected_payment,

        "items":
            items,

        "promo_applied":
            promo_applied,

        "promo_percent":
            promo_percent,

        "validation_error":
            validation_error,

        "validation_message":
            validation_message,

        "show_address_form":
            (
                state
                == "address_form_open"
            ),

        "show_payment_form":
            (
                state
                == "payment_form_open"
            ),

        "show_order_confirmation":
            (
                state
                == "order_placed"
            ),

        "place_order_ready":
            (
                state
                in {
                    "review_order",
                    "place_order_ready",
                    "promo_applied",
                }
            ),

        "totals":
            totals,

        "order_number":
            (
                f"{random.randint(100,999)}-"
                f"{random.randint(1000000,9999999)}"
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_checkout_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON CHECKOUT GENERATOR"
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
        "Promo:",
        data["promo_applied"],
    )

    print(
        "Total:",
        data["totals"]["total"],
    )