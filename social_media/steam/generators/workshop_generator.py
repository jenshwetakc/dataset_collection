from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_avatar,
    get_random_game_cover,
    get_random_game_screenshot,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

WORKSHOP_TYPES = [
    "Map",
    "Mod",
    "Skin",
    "Weapon",
    "Campaign",
    "Level",
    "Collection",
    "Asset",
]


CATEGORIES = [
    "Most Popular",
    "Most Subscribed",
    "Most Recent",
    "Top Rated",
    "Friends",
]


SORT_OPTIONS = [
    "Popular",
    "Newest",
    "Updated",
    "Rating",
]


# ==========================================================
# Workshop Title
# ==========================================================

def generate_workshop_title() -> str:

    patterns = [
        lambda: f"{fake.word().title()} Expansion",
        lambda: f"{fake.word().title()} Collection",
        lambda: f"{fake.word().title()} Rework",
        lambda: f"{fake.word().title()} Arena",
        lambda: f"{fake.word().title()} Overhaul",
        lambda: f"{fake.word().title()} Pack",
        lambda: f"{fake.word().title()} Remastered",
    ]

    return random.choice(
        patterns
    )()


# ==========================================================
# Workshop Item
# ==========================================================

def generate_workshop_item() -> dict:

    rating = random.randint(
        65,
        99,
    )

    subscribers = random.randint(
        80,
        500000,
    )

    return {

        "title":
            generate_workshop_title(),

        "image":
            get_random_game_screenshot(),

        "thumbnail":
            get_random_game_cover(),

        "author": {
            "name":
                fake.user_name(),

            "avatar":
                get_random_avatar(),
        },

        "type":
            random.choice(
                WORKSHOP_TYPES
            ),

        "rating":
            rating,

        "subscribers":
            subscribers,

        "favorites":
            random.randint(
                10,
                max(
                    20,
                    subscribers // 3,
                ),
            ),

        "comments":
            random.randint(
                0,
                3500,
            ),

        "size":
            random.choice([
                "1.2 MB",
                "12.6 MB",
                "54.8 MB",
                "114 MB",
                "488 MB",
                "1.4 GB",
            ]),

        "updated":
            random.choice([
                "Updated today",
                "Updated yesterday",
                "Updated 3 days ago",
                "Updated last week",
                "Updated last month",
            ]),

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "subscribed":
            random.random() < 0.25,

        "favorite":
            random.random() < 0.20,
    }


# ==========================================================
# Collection
# ==========================================================

def generate_collection() -> dict:

    return {

        "title":
            random.choice([
                "Essential Mods",
                "Community Favorites",
                "Visual Overhaul Pack",
                "Multiplayer Collection",
                "Quality of Life Pack",
                "Creator's Picks",
            ]),

        "image":
            get_random_game_cover(),

        "item_count":
            random.randint(
                8,
                80,
            ),

        "subscribers":
            random.randint(
                500,
                200000,
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_workshop_data() -> dict:

    items = [
        generate_workshop_item()
        for _ in range(
            random.randint(
                14,
                24,
            )
        )
    ]

    selected_item = random.choice(
        items
    )

    featured_items = random.sample(
        items,
        k=min(
            3,
            len(items),
        ),
    )

    return {

        "title":
            "Steam Workshop",

        "subtitle":
            random.choice([
                "Create, discover and share content",
                "Community-created content",
                "Mods, maps and community items",
            ]),

        "game": {
            "title":
                fake.catch_phrase(),

            "cover":
                get_random_game_cover(),
        },

        "search_placeholder":
            "Search workshop",

        "categories":
            CATEGORIES,

        "selected_category":
            random.choice(
                CATEGORIES
            ),

        "sort_options":
            SORT_OPTIONS,

        "selected_sort":
            random.choice(
                SORT_OPTIONS
            ),

        "featured_items":
            featured_items,

        "items":
            items,

        "selected_item":
            selected_item,

        "collections": [
            generate_collection()
            for _ in range(
                random.randint(
                    3,
                    5,
                )
            )
        ],

        "total_items":
            random.randint(
                1200,
                98000,
            ),
    }