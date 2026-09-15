from __future__ import annotations

import random

from social_media.baemin.generators.media_generator import (
    get_random_food_image,
)


# ==========================================================
# Data Pools
# ==========================================================

FOOD_NAMES = [
    "Original Fried Chicken",
    "Spicy Garlic Chicken",
    "Soy Garlic Chicken",
    "Beef Rice Bowl",
    "Kimchi Fried Rice",
    "Cheese Pizza",
    "Double Burger",
    "Seafood Noodles",
    "Pork Cutlet",
    "Tteokbokki",
]


RESTAURANT_NAMES = [
    "Seoul Chicken Lab",
    "Gangnam Kitchen",
    "Han River Table",
    "Golden Chicken",
    "Kitchen 88",
]


DELIVERY_OPTIONS = [
    {
        "id": "standard",
        "title": "Standard delivery",
        "subtitle": "30-40 min",
        "fee": 1500,
        "icon": "delivery_dining",
    },
    {
        "id": "express",
        "title": "Fast delivery",
        "subtitle": "20-30 min",
        "fee": 3000,
        "icon": "bolt",
    },
    {
        "id": "pickup",
        "title": "Pickup",
        "subtitle": "Ready in 15-20 min",
        "fee": 0,
        "icon": "storefront",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def format_price(
    value: int,
) -> str:

    return f"₩{value:,}"


# ==========================================================
# Cart Item
# ==========================================================

def generate_cart_item(
    index: int,
) -> dict:

    quantity = random.randint(
        1,
        3,
    )

    unit_price = random.randrange(
        7000,
        25000,
        500,
    )

    options = random.sample(
        [
            "Extra sauce",
            "No onions",
            "Large size",
            "Extra cheese",
            "Less spicy",
            "Add drink",
        ],
        k=random.randint(
            0,
            2,
        ),
    )

    return {
        "id":
            index,

        "name":
            random.choice(
                FOOD_NAMES
            ),

        "image":
            get_random_food_image(),

        "quantity":
            quantity,

        "unit_price":
            unit_price,

        "unit_price_text":
            format_price(
                unit_price
            ),

        "total_price":
            unit_price
            * quantity,

        "total_price_text":
            format_price(
                unit_price
                * quantity
            ),

        "options":
            options,
    }


# ==========================================================
# Cart Generator
# ==========================================================

def generate_cart_data() -> dict:

    cart_items = [
        generate_cart_item(
            index
        )
        for index
        in range(
            random.randint(
                3,
                7,
            )
        )
    ]

    subtotal = sum(
        item["total_price"]
        for item
        in cart_items
    )

    selected_delivery = random.choice(
        DELIVERY_OPTIONS
    )

    delivery_fee = (
        selected_delivery[
            "fee"
        ]
    )

    discount = random.choice(
        [
            0,
            0,
            2000,
            3000,
            5000,
        ]
    )

    service_fee = random.choice(
        [
            0,
            500,
            1000,
        ]
    )

    total = (
        subtotal
        + delivery_fee
        + service_fee
        - discount
    )

    return {

        "restaurant": {
            "name":
                random.choice(
                    RESTAURANT_NAMES
                ),
        },

        "delivery_address": {
            "label":
                "Delivery address",

            "address":
                random.choice(
                    [
                        "Gangnam-gu, Seoul",
                        "Mapo-gu, Seoul",
                        "Songpa-gu, Seoul",
                        "Jongno-gu, Seoul",
                    ]
                ),

            "detail":
                random.choice(
                    [
                        "Apartment 1204",
                        "Building B, Room 302",
                        "Leave at the front door",
                        "Call when you arrive",
                    ]
                ),
        },

        "cart_items":
            cart_items,

        "delivery_options":
            DELIVERY_OPTIONS,

        "selected_delivery":
            selected_delivery[
                "id"
            ],

        "coupon": {
            "available":
                random.random()
                < 0.7,

            "applied":
                discount > 0,

            "discount":
                discount,

            "discount_text":
                (
                    format_price(
                        discount
                    )
                    if discount > 0
                    else None
                ),
        },

        "request": {
            "text":
                random.choice(
                    [
                        "Please leave it at the door.",
                        "Please call when you arrive.",
                        "Please include extra napkins.",
                        "",
                    ]
                ),
        },

        "contactless_delivery":
            random.random()
            < 0.65,

        "pricing": {
            "subtotal":
                format_price(
                    subtotal
                ),

            "delivery_fee":
                (
                    "Free"
                    if delivery_fee == 0
                    else format_price(
                        delivery_fee
                    )
                ),

            "service_fee":
                (
                    "Free"
                    if service_fee == 0
                    else format_price(
                        service_fee
                    )
                ),

            "discount":
                (
                    f"-{format_price(discount)}"
                    if discount > 0
                    else None
                ),

            "total":
                format_price(
                    total
                ),
        },

        "payment_method": {
            "name":
                random.choice(
                    [
                        "Credit card",
                        "Baemin Pay",
                        "Kakao Pay",
                        "Naver Pay",
                    ]
                ),

            "icon":
                random.choice(
                    [
                        "credit_card",
                        "account_balance_wallet",
                        "payments",
                    ]
                ),
        },

        "item_count":
            sum(
                item["quantity"]
                for item
                in cart_items
            ),
    }