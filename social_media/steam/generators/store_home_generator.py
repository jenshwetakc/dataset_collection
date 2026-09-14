from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_avatar,
    get_random_game_banner,
    get_random_game_cover,
    get_random_game_screenshot,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

GENRES = [
    "Action",
    "Adventure",
    "RPG",
    "Strategy",
    "Simulation",
    "Indie",
    "Racing",
    "Sports",
    "Puzzle",
    "Horror",
    "Multiplayer",
    "Co-op",
    "Open World",
    "Survival",
]


NAVIGATION_ITEMS = [
    {
        "label": "Store",
        "icon": "storefront",
    },
    {
        "label": "Library",
        "icon": "video_library",
    },
    {
        "label": "Community",
        "icon": "groups",
    },
]


STORE_TABS = [
    "Your Store",
    "New & Noteworthy",
    "Categories",
    "Points Shop",
    "News",
    "Labs",
]


FEATURE_LABELS = [
    "Featured",
    "Top Seller",
    "New Release",
    "Popular",
    "Recommended",
]


# ==========================================================
# Price
# ==========================================================

def generate_price() -> dict:

    is_free = (
        random.random()
        < 0.10
    )

    if is_free:

        return {
            "is_free": True,
            "has_discount": False,
            "discount_percent": None,
            "original": None,
            "current": "Free to Play",
        }

    price = random.choice([
        4.99,
        6.99,
        9.99,
        12.99,
        14.99,
        19.99,
        24.99,
        29.99,
        39.99,
        49.99,
        59.99,
        69.99,
    ])

    has_discount = (
        random.random()
        < 0.48
    )

    if not has_discount:

        return {
            "is_free": False,
            "has_discount": False,
            "discount_percent": None,
            "original": None,
            "current": f"${price:.2f}",
        }

    discount = random.choice([
        10,
        15,
        20,
        25,
        30,
        40,
        50,
        60,
        70,
        75,
        80,
    ])

    discounted = (
        price
        * (
            1
            - discount / 100
        )
    )

    return {
        "is_free": False,
        "has_discount": True,
        "discount_percent": discount,
        "original": f"${price:.2f}",
        "current": f"${discounted:.2f}",
    }


# ==========================================================
# Game Title
# ==========================================================

def generate_game_title() -> str:

    patterns = [
        lambda: f"{fake.word().title()} Legends",
        lambda: f"Project {fake.word().title()}",
        lambda: f"{fake.word().title()} Frontier",
        lambda: f"Chronicles of {fake.word().title()}",
        lambda: f"{fake.word().title()} Protocol",
        lambda: f"The Last {fake.word().title()}",
        lambda: f"{fake.word().title()} Horizon",
        lambda: f"{fake.word().title()} Arena",
        lambda: f"{fake.word().title()} Valley",
    ]

    return random.choice(
        patterns
    )()


# ==========================================================
# Game
# ==========================================================

def generate_game() -> dict:

    genre_count = random.randint(
        2,
        4,
    )

    genres = random.sample(
        GENRES,
        k=genre_count,
    )

    review_score = random.randint(
        70,
        98,
    )

    return {

        "title":
            generate_game_title(),

        "cover":
            get_random_game_cover(),

        "banner":
            get_random_game_banner(),

        "genres":
            genres,

        "price":
            generate_price(),

        "review_score":
            review_score,

        "review_text":
            random.choice([
                "Mostly Positive",
                "Very Positive",
                "Overwhelmingly Positive",
                "Positive",
            ]),

        "release_text":
            random.choice([
                "Available now",
                "Recently released",
                "Coming soon",
                "Early Access",
            ]),
    }


# ==========================================================
# Featured Game
# ==========================================================

def generate_featured_game() -> dict:

    game = generate_game()

    game.update({

        "feature_label":
            random.choice(
                FEATURE_LABELS
            ),

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "screenshots": [
            get_random_game_screenshot()
            for _ in range(
                random.randint(
                    3,
                    5,
                )
            )
        ],
    })

    return game


# ==========================================================
# Store Section
# ==========================================================

def generate_store_section(
    title: str,
    game_count: int,
) -> dict:

    return {

        "title":
            title,

        "games": [
            generate_game()
            for _ in range(
                game_count
            )
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_store_home_data() -> dict:

    selected_nav = random.choice(
        NAVIGATION_ITEMS
    )

    section_titles = random.sample(
        [
            "Special Offers",
            "Trending Now",
            "Popular Releases",
            "Because You Played",
            "Top Sellers",
            "New & Trending",
            "Weekend Deals",
            "Recommended For You",
        ],
        k=4,
    )

    return {

        "brand":
            "STEAM",

        "navigation": [
            {
                **item,
                "selected":
                    item["label"]
                    == selected_nav["label"],
            }
            for item
            in NAVIGATION_ITEMS
        ],

        "store_tabs":
            STORE_TABS,

        "selected_store_tab":
            random.choice(
                STORE_TABS[:3]
            ),

        "search_placeholder":
            random.choice([
                "search the store",
                "Search games",
                "Search Steam",
            ]),

        "user": {

            "name":
                fake.user_name(),

            "avatar":
                get_random_avatar(),

            "wallet":
                f"${random.uniform(0, 150):.2f}",
        },

        "featured":
            generate_featured_game(),

        "quick_categories":
            random.sample(
                GENRES,
                k=6,
            ),

        "sections": [
            generate_store_section(
                title,
                random.randint(
                    6,
                    10,
                ),
            )
            for title
            in section_titles
        ],

        "footer_links": [
            "About",
            "Support",
            "News",
            "Privacy",
            "Legal",
        ],
    }