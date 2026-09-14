from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_game_cover,
    get_random_game_screenshot,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

RARITIES = [
    "Common",
    "Uncommon",
    "Rare",
    "Epic",
    "Legendary",
]


ITEM_TYPES = [
    "Trading Card",
    "Weapon Skin",
    "Profile Background",
    "Emoticon",
    "Sticker",
    "Badge",
    "Booster Pack",
    "Collectible",
]


CATEGORIES = [
    "All Items",
    "Recent",
    "Tradable",
    "Marketable",
    "Favorites",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_item_name() -> str:

    templates = [
        lambda: f"{fake.word().title()} Card",
        lambda: f"{fake.word().title()} Skin",
        lambda: f"{fake.word().title()} Badge",
        lambda: f"{fake.word().title()} Emoticon",
        lambda: f"{fake.word().title()} Collection",
        lambda: f"{fake.word().title()} Background",
    ]

    return random.choice(
        templates
    )()


# ==========================================================
# Inventory Item
# ==========================================================

def generate_inventory_item() -> dict:

    rarity = random.choice(
        RARITIES
    )

    quantity = random.choice([
        1,
        1,
        1,
        2,
        3,
        4,
        5,
    ])

    marketable = (
        random.random()
        < 0.62
    )

    tradable = (
        random.random()
        < 0.72
    )

    return {

        "name":
            generate_item_name(),

        "image":
            get_random_game_cover(),

        "preview":
            get_random_game_screenshot(),

        "rarity":
            rarity,

        "item_type":
            random.choice(
                ITEM_TYPES
            ),

        "game":
            fake.catch_phrase(),

        "quantity":
            quantity,

        "marketable":
            marketable,

        "tradable":
            tradable,

        "favorite":
            random.random() < 0.18,

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "market_price":
            (
                f"${random.uniform(0.10, 85):.2f}"
                if marketable
                else None
            ),

        "date_acquired":
            random.choice([
                "Today",
                "Yesterday",
                "3 days ago",
                "Last week",
                "2 weeks ago",
                "Last month",
            ]),
    }


# ==========================================================
# Inventory Collection
# ==========================================================

def generate_inventory_group(
    name: str,
) -> dict:

    item_count = random.randint(
        12,
        28,
    )

    return {

        "name":
            name,

        "icon":
            get_random_game_cover(),

        "count":
            item_count,

        "items": [
            generate_inventory_item()
            for _ in range(
                item_count
            )
        ],
    }


# ==========================================================
# Main
# ==========================================================

def generate_inventory_data() -> dict:

    inventory_names = [
        "Steam",
        "Community Items",
        "Trading Cards",
        "Game Items",
    ]

    inventories = [
        generate_inventory_group(
            name
        )
        for name
        in inventory_names
    ]

    selected_inventory = random.choice(
        inventories
    )

    selected_item = random.choice(
        selected_inventory["items"]
    )

    return {

        "title":
            "Inventory",

        "subtitle":
            random.choice([
                "Your Steam items",
                "Items, cards and collectibles",
                "Manage your inventory",
            ]),

        "search_placeholder":
            "Search inventory",

        "categories":
            CATEGORIES,

        "selected_category":
            random.choice(
                CATEGORIES
            ),

        "inventories":
            inventories,

        "selected_inventory":
            selected_inventory,

        "selected_item":
            selected_item,

        "total_items":
            sum(
                inventory["count"]
                for inventory
                in inventories
            ),
    }