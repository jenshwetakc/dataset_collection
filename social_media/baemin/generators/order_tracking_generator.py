from __future__ import annotations

import random

from social_media.baemin.generators.media_generator import (
    get_random_avatar,
    get_random_food_image,
)


# ==========================================================
# Status Pools
# ==========================================================

ORDER_STATES = [
    {
        "id": "confirmed",
        "title": "Order confirmed",
        "subtitle": "The restaurant received your order.",
        "icon": "check_circle",
    },
    {
        "id": "preparing",
        "title": "Preparing your order",
        "subtitle": "The restaurant is preparing your food.",
        "icon": "skillet",
    },
    {
        "id": "picked_up",
        "title": "Picked up",
        "subtitle": "Your rider has picked up the order.",
        "icon": "delivery_dining",
    },
    {
        "id": "on_the_way",
        "title": "On the way",
        "subtitle": "Your rider is heading to you.",
        "icon": "near_me",
    },
    {
        "id": "delivered",
        "title": "Delivered",
        "subtitle": "Your order has arrived.",
        "icon": "home",
    },
]


RESTAURANTS = [
    "Seoul Chicken Lab",
    "Gangnam Kitchen",
    "Golden Chicken",
    "Kitchen 88",
    "Han River Table",
]


DRIVER_NAMES = [
    "Minjun",
    "Jisoo",
    "Hyunwoo",
    "Sora",
    "Yuna",
    "Jiho",
]


ORDER_ITEMS = [
    "Original Fried Chicken",
    "Spicy Garlic Chicken",
    "Cheese Fries",
    "Kimchi Fried Rice",
    "Coke",
    "Tteokbokki",
]


# ==========================================================
# Generator
# ==========================================================

def generate_order_tracking_data() -> dict:

    current_index = random.randint(
        1,
        3,
    )

    eta_minutes = random.randint(
        8,
        28,
    )

    item_count = random.randint(
        2,
        5,
    )

    order_items = random.sample(
        ORDER_ITEMS,
        k=min(
            item_count,
            len(
                ORDER_ITEMS
            ),
        ),
    )

    return {

        "order_id":
            f"BM-{random.randint(100000, 999999)}",

        "restaurant": {
            "name":
                random.choice(
                    RESTAURANTS
                ),

            "image":
                get_random_food_image(),
        },

        "eta": {
            "minutes":
                eta_minutes,

            "text":
                f"Arriving in {eta_minutes} min",

            "time_range":
                random.choice(
                    [
                        "12:40 - 12:50",
                        "18:20 - 18:35",
                        "19:10 - 19:25",
                        "20:05 - 20:20",
                    ]
                ),
        },

        "current_status_index":
            current_index,

        "statuses":
            ORDER_STATES,

        "driver": {
            "name":
                random.choice(
                    DRIVER_NAMES
                ),

            "avatar":
                get_random_avatar(),

            "rating":
                round(
                    random.uniform(
                        4.7,
                        5.0,
                    ),
                    1,
                ),

            "vehicle":
                random.choice(
                    [
                        "Motorbike",
                        "Scooter",
                        "Bicycle",
                    ]
                ),
        },

        "delivery_address": {
            "title":
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
                    ]
                ),
        },

        "order_items":
            order_items,

        "total":
            f"₩{random.randrange(18000, 65000, 500):,}",

        "support_message":
            random.choice(
                [
                    "Need help with your delivery?",
                    "Something wrong with your order?",
                    "Contact support if you need assistance.",
                ]
            ),
    }