from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_game_cover,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

ITEM_TYPES = [
    "Weapon Skin",
    "Trading Card",
    "Sticker",
    "Emoticon",
    "Crate",
    "Collectible",
    "Profile Background",
]


MARKET_FILTERS = [
    "Popular",
    "Newly Listed",
    "Price Low",
    "Price High",
    "Most Sold",
]


GAME_NAMES = [
    "Counter Strike",
    "Dota Arena",
    "Galaxy Front",
    "Shadow Protocol",
    "Neon Strike",
    "Arena Legends",
    "Steel Horizon",
]


# ==========================================================
# Item Name
# ==========================================================

def generate_item_name() -> str:

    templates = [
        lambda: f"{fake.word().title()} Dragon",
        lambda: f"{fake.word().title()} Fade",
        lambda: f"{fake.word().title()} Collection",
        lambda: f"{fake.word().title()} Strike",
        lambda: f"{fake.word().title()} Emblem",
        lambda: f"{fake.word().title()} Card",
        lambda: f"{fake.word().title()} Pattern",
    ]

    return random.choice(
        templates
    )()


# ==========================================================
# Price
# ==========================================================

def generate_price(
    minimum: float = 0.05,
    maximum: float = 150.0,
) -> float:

    return round(
        random.uniform(
            minimum,
            maximum,
        ),
        2,
    )


# ==========================================================
# Market Item
# ==========================================================

def generate_market_item() -> dict:

    price = generate_price()

    quantity = random.randint(
        1,
        5000,
    )

    change = round(
        random.uniform(
            -25,
            35,
        ),
        1,
    )

    return {

        "name":
            generate_item_name(),

        "image":
            get_random_game_cover(),

        "game":
            random.choice(
                GAME_NAMES
            ),

        "item_type":
            random.choice(
                ITEM_TYPES
            ),

        "price_value":
            price,

        "price":
            f"${price:.2f}",

        "quantity":
            quantity,

        "volume":
            random.randint(
                25,
                50000,
            ),

        "change":
            change,

        "positive":
            change >= 0,

        "favorite":
            random.random() < 0.18,
    }


# ==========================================================
# Sell Listing
# ==========================================================

def generate_sell_listing(
    base_price: float,
) -> dict:

    price = max(
        0.03,
        base_price
        * random.uniform(
            0.90,
            1.18,
        ),
    )

    return {

        "seller":
            fake.user_name(),

        "price":
            f"${price:.2f}",

        "price_value":
            round(
                price,
                2,
            ),

        "quantity":
            random.randint(
                1,
                8,
            ),

        "listed":
            random.choice([
                "Just now",
                "2 min ago",
                "8 min ago",
                "20 min ago",
                "1 hr ago",
            ]),
    }


# ==========================================================
# Buy Order
# ==========================================================

def generate_buy_order(
    base_price: float,
) -> dict:

    price = max(
        0.03,
        base_price
        * random.uniform(
            0.72,
            0.98,
        ),
    )

    return {

        "price":
            f"${price:.2f}",

        "price_value":
            round(
                price,
                2,
            ),

        "quantity":
            random.randint(
                1,
                400,
            ),
    }


# ==========================================================
# Transaction
# ==========================================================

def generate_transaction() -> dict:

    price = generate_price(
        0.10,
        80,
    )

    return {

        "type":
            random.choice([
                "Sold",
                "Purchased",
            ]),

        "item":
            generate_item_name(),

        "price":
            f"${price:.2f}",

        "timestamp":
            random.choice([
                "Today",
                "Yesterday",
                "2 days ago",
                "Last week",
                "2 weeks ago",
            ]),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_community_market_data() -> dict:

    items = [
        generate_market_item()
        for _ in range(
            random.randint(
                16,
                28,
            )
        )
    ]

    selected_item = random.choice(
        items
    )

    sell_listings = [
        generate_sell_listing(
            selected_item[
                "price_value"
            ]
        )
        for _ in range(
            random.randint(
                5,
                9,
            )
        )
    ]

    buy_orders = [
        generate_buy_order(
            selected_item[
                "price_value"
            ]
        )
        for _ in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    return {

        "title":
            "Community Market",

        "subtitle":
            "Buy and sell items with community members",

        "search_placeholder":
            "Search for items",

        "filters":
            MARKET_FILTERS,

        "selected_filter":
            random.choice(
                MARKET_FILTERS
            ),

        "items":
            items,

        "selected_item":
            selected_item,

        "sell_listings":
            sell_listings,

        "buy_orders":
            buy_orders,

        "transactions": [
            generate_transaction()
            for _ in range(
                random.randint(
                    5,
                    9,
                )
            )
        ],

        "wallet_balance":
            f"${random.uniform(5, 250):.2f}",

        "active_listings":
            random.randint(
                2,
                35,
            ),

        "buy_order_count":
            random.randint(
                1,
                18,
            ),
    }