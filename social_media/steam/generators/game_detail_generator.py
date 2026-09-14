from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
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
    "Horror",
    "Puzzle",
    "Open World",
    "Survival",
    "Multiplayer",
    "Co-op",
]


FEATURES = [
    "Single-player",
    "Online Co-op",
    "Online PvP",
    "Controller Support",
    "Cloud Saves",
    "Achievements",
    "Trading Cards",
    "Workshop",
]


LANGUAGES = [
    "English",
    "Korean",
    "Japanese",
    "French",
    "German",
    "Spanish",
    "Chinese",
]


# ==========================================================
# Title
# ==========================================================

def generate_game_title() -> str:

    templates = [
        lambda: f"{fake.word().title()} Horizon",
        lambda: f"Project {fake.word().title()}",
        lambda: f"{fake.word().title()} Protocol",
        lambda: f"The Last {fake.word().title()}",
        lambda: f"{fake.word().title()} Frontier",
        lambda: f"{fake.word().title()} Odyssey",
        lambda: f"{fake.word().title()} Chronicles",
    ]

    return random.choice(
        templates
    )()


# ==========================================================
# Price
# ==========================================================

def generate_price() -> dict:

    base_price = random.choice([
        9.99,
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
        < 0.55
    )

    if not has_discount:

        return {
            "has_discount": False,
            "discount_percent": None,
            "original": None,
            "current": f"${base_price:.2f}",
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
    ])

    discounted = (
        base_price
        * (
            1
            - discount / 100
        )
    )

    return {
        "has_discount": True,
        "discount_percent": discount,
        "original": f"${base_price:.2f}",
        "current": f"${discounted:.2f}",
    }


# ==========================================================
# Review Summary
# ==========================================================

def generate_review_summary() -> dict:

    score = random.randint(
        72,
        98,
    )

    if score >= 95:
        label = "Overwhelmingly Positive"

    elif score >= 85:
        label = "Very Positive"

    elif score >= 75:
        label = "Mostly Positive"

    else:
        label = "Positive"

    return {

        "score":
            score,

        "label":
            label,

        "count":
            random.randint(
                1200,
                85000,
            ),
    }


# ==========================================================
# DLC
# ==========================================================

def generate_dlc() -> dict:

    price = random.choice([
        2.99,
        4.99,
        5.99,
        7.99,
        9.99,
        14.99,
        19.99,
    ])

    return {

        "title":
            random.choice([
                "Expansion Pack",
                "Digital Artbook",
                "Soundtrack",
                "Season Pass",
                "Bonus Content",
                "Deluxe Upgrade",
                "New Horizons DLC",
            ]),

        "image":
            get_random_game_cover(),

        "price":
            f"${price:.2f}",

        "release":
            random.choice([
                "Available now",
                "Recently released",
                "Coming soon",
            ]),
    }


# ==========================================================
# Review
# ==========================================================

def generate_review() -> dict:

    recommended = (
        random.random()
        < 0.86
    )

    return {

        "recommended":
            recommended,

        "author":
            fake.user_name(),

        "playtime":
            f"{random.uniform(2, 800):.1f} hrs",

        "text":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    5,
                )
            ),

        "helpful":
            random.randint(
                5,
                2400,
            ),

        "timestamp":
            random.choice([
                "Posted today",
                "Posted yesterday",
                "Posted 3 days ago",
                "Posted last week",
            ]),
    }


# ==========================================================
# System Requirements
# ==========================================================

def generate_system_requirements() -> dict:

    return {

        "os":
            random.choice([
                "Windows 10 64-bit",
                "Windows 11 64-bit",
            ]),

        "processor":
            random.choice([
                "Intel Core i5-8400",
                "AMD Ryzen 5 2600",
                "Intel Core i7-9700",
            ]),

        "memory":
            random.choice([
                "8 GB RAM",
                "12 GB RAM",
                "16 GB RAM",
            ]),

        "graphics":
            random.choice([
                "GTX 1060 6GB",
                "RTX 2060",
                "RX 5700 XT",
            ]),

        "storage":
            random.choice([
                "45 GB available space",
                "70 GB available space",
                "95 GB available space",
            ]),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_game_detail_data() -> dict:

    title = (
        generate_game_title()
    )

    return {

        "title":
            title,

        "banner":
            get_random_game_banner(),

        "cover":
            get_random_game_cover(),

        "screenshots": [
            get_random_game_screenshot()
            for _ in range(
                6
            )
        ],

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    3,
                    6,
                )
            ),

        "short_description":
            fake.paragraph(
                nb_sentences=2
            ),

        "developer":
            fake.company(),

        "publisher":
            fake.company(),

        "release_date":
            fake.date_between(
                start_date="-5y",
                end_date="today",
            ).strftime(
                "%d %b, %Y"
            ),

        "genres":
            random.sample(
                GENRES,
                k=random.randint(
                    3,
                    5,
                ),
            ),

        "features":
            random.sample(
                FEATURES,
                k=random.randint(
                    4,
                    7,
                ),
            ),

        "languages":
            random.sample(
                LANGUAGES,
                k=random.randint(
                    3,
                    6,
                ),
            ),

        "price":
            generate_price(),

        "reviews":
            generate_review_summary(),

        "wishlist_count":
            random.randint(
                10000,
                500000,
            ),

        "dlc": [
            generate_dlc()
            for _ in range(
                random.randint(
                    3,
                    6,
                )
            )
        ],

        "user_reviews": [
            generate_review()
            for _ in range(
                random.randint(
                    4,
                    7,
                )
            )
        ],

        "requirements": {
            "minimum":
                generate_system_requirements(),

            "recommended":
                generate_system_requirements(),
        },
    }