from __future__ import annotations

import random

from faker import Faker

from social_media.baemin.generators.media_generator import (
    get_random_food_image,
    get_random_restaurant_image,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Controlled Pools
# ==========================================================

RESTAURANT_SUFFIXES = [
    "Kitchen",
    "Chicken",
    "Table",
    "House",
    "Cafe",
    "Bistro",
    "Grill",
    "Express",
]


MENU_POOL = [
    "Original Fried Chicken",
    "Spicy Garlic Chicken",
    "Cheese Fries",
    "Kimchi Fried Rice",
    "Beef Bibimbap",
    "Tteokbokki",
    "Double Burger",
    "Cheese Pizza",
    "Seafood Noodles",
    "Pork Cutlet",
    "Coke",
    "Iced Tea",
]


ORDER_STATUSES = [
    "Delivered",
    "Cancelled",
    "Refunded",
]


ACTIVE_STATUSES = [
    "Preparing",
    "Picked up",
    "On the way",
]


TABS = [
    "Active",
    "Past orders",
]


# ==========================================================
# Helpers
# ==========================================================

def format_price(
    value: int,
) -> str:

    return f"₩{value:,}"


def generate_restaurant_name() -> str:

    prefix = random.choice(
        [
            fake.first_name(),
            fake.last_name(),
            fake.city().split()[0],
            "Seoul",
            "Daily",
            "Golden",
            "Happy",
            "Fresh",
            "Urban",
        ]
    )

    suffix = random.choice(
        RESTAURANT_SUFFIXES
    )

    return f"{prefix} {suffix}"


def generate_menu_summary() -> list[str]:

    return random.sample(
        MENU_POOL,
        k=random.randint(
            1,
            4,
        ),
    )


# ==========================================================
# Active Order
# ==========================================================

def generate_active_order(
    index: int,
) -> dict:

    status = random.choice(
        ACTIVE_STATUSES
    )

    eta_minutes = random.randint(
        8,
        35,
    )

    return {

        "id":
            index,

        "order_id":
            f"BM-{random.randint(100000, 999999)}",

        "restaurant_name":
            generate_restaurant_name(),

        "restaurant_image":
            (
                get_random_restaurant_image()
                or get_random_food_image()
            ),

        "status":
            status,

        "eta":
            f"{eta_minutes} min",

        "eta_label":
            random.choice(
                [
                    "Estimated arrival",
                    "Expected delivery",
                    "Arrives in",
                ]
            ),

        "progress":
            random.randint(
                30,
                85,
            ),

        "menu_names":
            generate_menu_summary(),

        "total":
            format_price(
                random.randrange(
                    15000,
                    65000,
                    500,
                )
            ),

        "delivery_address":
            fake.street_address(),

        "can_track":
            True,
    }


# ==========================================================
# Past Order
# ==========================================================

def generate_past_order(
    index: int,
) -> dict:

    status = random.choices(
        population=[
            "Delivered",
            "Cancelled",
            "Refunded",
        ],
        weights=[
            82,
            12,
            6,
        ],
        k=1,
    )[0]

    menu_names = (
        generate_menu_summary()
    )

    return {

        "id":
            index,

        "order_id":
            f"BM-{random.randint(100000, 999999)}",

        "restaurant_name":
            generate_restaurant_name(),

        "restaurant_image":
            (
                get_random_restaurant_image()
                or get_random_food_image()
            ),

        "status":
            status,

        "date":
            fake.date_time_between(
                start_date="-10M",
                end_date="-1d",
            ).strftime(
                "%b %d, %Y · %H:%M"
            ),

        "timestamp":
            fake.date_time_between(
                start_date="-90d",
                end_date="-1d",
            ).strftime(
                "%m/%d %H:%M"
            ),

        "menu_names":
            menu_names,

        "item_count":
            len(
                menu_names
            ),

        "total":
            format_price(
                random.randrange(
                    10000,
                    80000,
                    500,
                )
            ),

        "delivery_address":
            fake.street_address(),

        "reviewed":
            random.random()
            < 0.45,

        "can_reorder":
            status
            == "Delivered",
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_order_history_data() -> dict:

    active_count = random.choice(
        [
            0,
            1,
            1,
            2,
        ]
    )

    active_orders = [

        generate_active_order(
            index
        )

        for index in range(
            active_count
        )
    ]

    past_orders = [

        generate_past_order(
            index
        )

        for index in range(
            random.randint(
                8,
                18,
            )
        )
    ]

    selected_tab = (
        "Active"
        if active_orders
        and random.random() < 0.45
        else "Past orders"
    )

    return {

        "page_title":
            random.choice(
                [
                    "My orders",
                    "Order history",
                    "Your orders",
                ]
            ),

        "tabs":
            TABS,

        "selected_tab":
            selected_tab,

        "active_orders":
            active_orders,

        "past_orders":
            past_orders,

        "active_count":
            len(
                active_orders
            ),

        "past_count":
            len(
                past_orders
            ),

        "user_location":
            fake.city(),

        "empty_active_message":
            random.choice(
                [
                    "No active deliveries right now.",
                    "You don't have an active order.",
                    "Your next delicious order will appear here.",
                ]
            ),
    }